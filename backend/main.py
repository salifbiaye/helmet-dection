from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import base64
import io
import time
import asyncio
import tempfile
import os
import httpx
from pathlib import Path
from PIL import Image
import numpy as np
from ultralytics import YOLO
import cv2

app = FastAPI(
    title="Helmet Detection API",
    description="YOLOv8 object detection — image, video & webcam",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model ──────────────────────────────────────────────────────────────────────

class ObjectDetector:
    def __init__(self, model_path: str = "models/helmet_model_best.pt"):
        self.model = YOLO(model_path)
        # Optimisation pour CPU : fusion des couches du modèle
        try:
            self.model.fuse()
        except Exception:
            pass
        self.classes = self.model.names
        print(f"✅ Modèle chargé et optimisé : {model_path} ({len(self.classes)} classes)")

    def _run(self, image: Image.Image, conf: float, iou: float) -> dict:
        start = time.time()
        
        # Optimisation : redimensionnement à 640px max pour accélérer l'inférence CPU
        if max(image.size) > 640:
            image.thumbnail((640, 640))
            
        results = self.model(image, conf=conf, iou=iou, verbose=False, imgsz=640)[0]
        ms = round((time.time() - start) * 1000, 2)

        detections = [
            {
                "bbox": box.xyxy[0].tolist(),
                "confidence": round(float(box.conf[0]), 4),
                "class_id": int(box.cls[0]),
                "class_name": self.classes[int(box.cls[0])],
            }
            for box in results.boxes
        ]

        annotated = results.plot()
        buf = io.BytesIO()
        Image.fromarray(annotated[:, :, ::-1]).save(buf, format="JPEG", quality=85)
        img_b64 = base64.b64encode(buf.getvalue()).decode()

        return {"detections": detections, "count": len(detections),
                "inference_time_ms": ms, "annotated_image": img_b64}

    def detect_image(self, image: Image.Image, conf=0.25, iou=0.45) -> dict:
        return self._run(image, conf, iou)

    def detect_frame(self, frame_bgr: np.ndarray, conf=0.25, iou=0.45) -> dict:
        img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
        return self._run(img, conf, iou)


detector: ObjectDetector | None = None


@app.on_event("startup")
async def startup():
    global detector
    # Priorité absolue au modèle de casque spécialisé
    paths = ["models/helmet_model_best.pt", "models/best.pt", "yolov8n.pt"]
    for path in paths:
        try:
            detector = ObjectDetector(path)
            break
        except Exception:
            continue


# ── FRONTEND MOUNTING ──────────────────────────────────────────────────────────




# ── REST Endpoints ────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": detector is not None,
            "classes": len(detector.classes) if detector else 0}


@app.post("/detect")
async def detect_image_endpoint(
    file: UploadFile = File(...),
    conf: float = Query(0.25, ge=0.01, le=0.99),
    iou:  float = Query(0.45, ge=0.01, le=0.99),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Fichier image requis (jpg, png, webp…)")
    data = await file.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    return JSONResponse(detector.detect_image(img, conf, iou))


@app.post("/detect/url")
async def detect_from_url(
    url: str = Query(..., description="URL publique d'une image"),
    conf: float = Query(0.25, ge=0.01, le=0.99),
    iou:  float = Query(0.45, ge=0.01, le=0.99),
):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(400, f"Impossible de télécharger l'image: {e}")
    if not resp.headers.get("content-type", "").startswith("image/"):
        raise HTTPException(400, "L'URL ne pointe pas vers une image")
    img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    return JSONResponse(detector.detect_image(img, conf, iou))


@app.post("/detect/video")
async def detect_video_endpoint(
    file: UploadFile = File(...),
    conf:       float = Query(0.25, ge=0.01, le=0.99),
    iou:        float = Query(0.45, ge=0.01, le=0.99),
    frame_skip: int   = Query(5, ge=1, le=60, description="Analyser 1 frame sur N"),
):
    if not file.content_type.startswith("video/"):
        raise HTTPException(400, "Fichier vidéo requis")

    data = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise HTTPException(400, "Vidéo illisible")

        fps_vid    = cap.get(cv2.CAP_PROP_FPS) or 25
        total_frm  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_s = round(total_frm / fps_vid, 2)

        all_detections, frames_done, start = [], 0, time.time()
        class_summary: dict[str, int] = {}
        preview_frame_b64 = None

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % frame_skip == 0:
                result = detector.detect_frame(frame, conf, iou)
                frames_done += 1
                for det in result["detections"]:
                    all_detections.append(det)
                    class_summary[det["class_name"]] = class_summary.get(det["class_name"], 0) + 1
                if preview_frame_b64 is None and result["count"] > 0:
                    preview_frame_b64 = result["annotated_image"]
            frame_idx += 1

        cap.release()
        # fallback preview: first analyzed frame
        if preview_frame_b64 is None and frames_done > 0:
            cap2 = cv2.VideoCapture(tmp_path)
            ret, frame = cap2.read()
            cap2.release()
            if ret:
                r = detector.detect_frame(frame, conf, iou)
                preview_frame_b64 = r["annotated_image"]

        return JSONResponse({
            "frames_total":     total_frm,
            "frames_analyzed":  frames_done,
            "total_detections": len(all_detections),
            "class_summary":    class_summary,
            "duration_s":       duration_s,
            "fps":              round(fps_vid, 2),
            "inference_time_ms": round((time.time() - start) * 1000, 2),
            "preview_frame":    preview_frame_b64,
        })
    finally:
        os.unlink(tmp_path)


@app.post("/detect/batch")
async def detect_batch(
    files: list[UploadFile] = File(...),
    conf: float = Query(0.25),
    iou:  float = Query(0.45),
):
    results = []
    for f in files:
        data = await f.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        results.append({**detector.detect_image(img, conf, iou), "filename": f.filename})
    return JSONResponse({"results": results, "count": len(results)})


# ── WebSocket — Webcam temps réel ─────────────────────────────────────────────

@app.websocket("/ws/detect")
async def websocket_detect(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            payload = await ws.receive_json()
            b64    = payload.get("image", "")
            conf   = float(payload.get("conf", 0.25))
            img_bytes = base64.b64decode(b64)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            result = detector.detect_image(img, conf)
            await ws.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await ws.send_json({"error": str(e)})
        except Exception:
            pass




 

# ── FRONTEND MOUNTING ──────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Chemins potentiels pour index.html
    base_path = Path(__file__).parent
    paths_to_check = [
        base_path / "frontend" / "index.html",
        base_path / "index.html",
        Path("/app/frontend/index.html"),
        Path("frontend/index.html")
    ]
    
    for path in paths_to_check:
        if path.exists():
            return path.read_text(encoding="utf-8")
    
    # Debug si non trouvé
    error_msg = f"Fichier index.html non trouvé. Chemins testés: {[str(p) for p in paths_to_check]}. "
    error_msg += f"Contenu de {base_path}: {os.listdir(base_path)}"
    print(f"❌ ERROR: {error_msg}")
    raise HTTPException(status_code=404, detail=error_msg)

# Note: Mount "/css", "/js", etc. or keep the catch-all mount at the end
base_path = Path(__file__).parent
app.mount("/css", StaticFiles(directory=base_path / "frontend" / "css"), name="css")
app.mount("/js", StaticFiles(directory=base_path / "frontend" / "js"), name="js")
app.mount("/", StaticFiles(directory=base_path / "frontend", html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
