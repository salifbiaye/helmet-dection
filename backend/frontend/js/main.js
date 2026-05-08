// ── LANGUAGES ──────────────────────────────────────────────────────────────
let currentLang = 'EN';
const translations = {
  EN: {
    'With Helmet': 'With Helmet',
    'Without Helmet': 'Without Helmet',
    'image': 'Image', 'url': 'Image URL', 'video': 'Video', 'webcam': 'Webcam',
    'img-title': 'Image Detection', 'img-desc': 'Upload an image to run helmet detection inference.',
    'url-title': 'URL Detection', 'url-desc': 'Provide a direct image URL for remote inference.',
    'vid-title': 'Video AI Player', 'vid-desc': 'Play a video and see AI detections overlaid in real-time.',
    'cam-title': 'Live Webcam', 'cam-desc': 'Real-time detection via WebSocket stream.',
    'run': 'Run detection', 'analyze': 'Analyze video', 'start-cam': 'Start webcam', 'stop': 'Stop',
    'empty': 'No detections', 'wait': 'Waiting for frames…', 'click': 'Click to upload', 'or': 'or drag and drop',
    'inference': 'Inference', 'detections': 'Detections', 'frames': 'Frames', 'duration': 'Duration',
    'download': 'Download Report', 'pending': 'Pending', 'batch-title': 'Batch Results', 'inf': 'Inf.'
  },
  FR: {
    'With Helmet': 'Avec Casque',
    'Without Helmet': 'Sans Casque',
    'image': 'Image', 'url': 'URL Image', 'video': 'Vidéo', 'webcam': 'Webcam',
    'img-title': 'Détection sur Image', 'img-desc': 'Téléchargez une image pour lancer la détection de casques.',
    'url-title': 'Détection via URL', 'url-desc': 'Fournissez une URL directe d\'image pour une analyse à distance.',
    'vid-title': 'Lecteur Vidéo IA', 'vid-desc': 'Lisez une vidéo et voyez les détections IA en temps réel.',
    'cam-title': 'Webcam en Direct', 'cam-desc': 'Détection en temps réel via un flux WebSocket.',
    'run': 'Lancer la détection', 'analyze': 'Analyser la vidéo', 'start-cam': 'Démarrer webcam', 'stop': 'Arrêter',
    'empty': 'Aucune détection', 'wait': 'En attente d\'images…', 'click': 'Cliquez pour uploader', 'or': 'ou glissez-déposez',
    'inference': 'Inférence', 'detections': 'Détections', 'frames': 'Images', 'duration': 'Durée',
    'download': 'Télécharger Rapport', 'pending': 'En attente', 'batch-title': 'Résultats du Lot', 'inf': 'Inf.'
  }
};

function toggleLang() {
  currentLang = currentLang === 'EN' ? 'FR' : 'EN';
  document.getElementById('lang-label').textContent = currentLang;
  applyTranslations();
}

function t(key) { return translations[currentLang][key] || key; }

function applyTranslations() {
  const tr = translations[currentLang];
  const navs = document.querySelectorAll('.nav-item');
  if (navs.length >= 4) {
    navs[0].childNodes[2].textContent = ' ' + tr['image'];
    navs[1].childNodes[2].textContent = ' ' + tr['url'];
    navs[2].childNodes[2].textContent = ' ' + tr['video'];
    navs[3].childNodes[2].textContent = ' ' + tr['webcam'];
  }
  document.querySelector('#panel-image .page-title').textContent = tr['img-title'];
  document.querySelector('#panel-image .page-desc').textContent = tr['img-desc'];
  document.querySelector('#panel-url .page-title').textContent = tr['url-title'];
  document.querySelector('#panel-url .page-desc').textContent = tr['url-desc'];
  document.querySelector('#panel-video .page-title').textContent = tr['vid-title'];
  document.querySelector('#panel-video .page-desc').textContent = tr['vid-desc'];
  document.querySelector('#panel-webcam .page-title').textContent = tr['cam-title'];
  document.querySelector('#panel-webcam .page-desc').textContent = tr['cam-desc'];

  document.getElementById('img-btn').textContent = tr['run'];
  document.querySelector('#panel-url .btn').textContent = tr['run'];
  document.getElementById('cam-start-btn').childNodes[1].textContent = ' ' + tr['start-cam'];
  document.getElementById('cam-stop-btn').childNodes[1].textContent = ' ' + tr['stop'];

  document.querySelectorAll('.drop-text strong').forEach(el => el.textContent = tr['click']);
  document.querySelectorAll('.drop-text').forEach(el => {
    if (el.textContent.includes('drag') || el.textContent.includes('glissez'))
      el.childNodes[1].textContent = ' ' + tr['or'];
  });

  const headerBtn = document.getElementById('header-download-btn');
  if (headerBtn) {
    const span = headerBtn.querySelector('.d-hide-mobile');
    if (span) span.textContent = tr['download'];
  }
  const batchTitle = document.querySelector('#img-batch-wrap .sidebar-label');
  if (batchTitle) batchTitle.textContent = tr['batch-title'];

  const activeBatchIdx = Array.from(document.querySelectorAll('.batch-item')).findIndex(el => el.classList.contains('active'));
  if (activeBatchIdx >= 0) showBatchResult('img', activeBatchIdx);
  renderBatchGallery('img');
}

// ── NAVIGATION ──────────────────────────────────────────────────────────────
function switchPanel(id, el) {
  // Stop video AI if leaving video panel
  if (id !== 'video') stopVidAI();
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  el.classList.add('active');
}

// ── HELPERS ─────────────────────────────────────────────────────────────────
function confColor(c) {
  if (c >= .75) return '#4ade80';
  if (c >= .5) return '#facc15';
  return '#f87171';
}

function renderDetections(prefix, detections) {
  const container = document.getElementById(prefix + '-detections');
  if (!detections || detections.length === 0) {
    container.innerHTML = `<div class="empty">${t('empty')}</div>`;
    return;
  }
  const items = detections.map(d => {
    const pct = (d.confidence * 100).toFixed(1);
    const col = confColor(d.confidence);
    const translatedName = t(d.class_name);
    return `<div class="det-item">
      <span class="det-class">${translatedName}</span>
      <div class="det-conf-wrap">
        <div class="det-bar-bg"><div class="det-bar" style="width:${pct}%;background:${col}"></div></div>
        <span class="det-conf" style="color:${col}">${pct}%</span>
      </div>
    </div>`;
  }).join('');
  container.innerHTML = `<div class="det-list">${items}</div>`;
}

function showResult(prefix, data) {
  const preview = document.getElementById(prefix + '-preview');
  if (data.annotated_image) {
    preview.style.display = 'flex';
    preview.innerHTML = `<img src="data:image/jpeg;base64,${data.annotated_image}">`;
  }
  document.getElementById(prefix + '-stats').innerHTML = `
    <div class="stat-chip"><span class="stat-label">${t('detections')}</span><span class="stat-val">${data.count}</span></div>
    <div class="stat-chip"><span class="stat-label">${t('inference')}</span><span class="stat-val">${data.inference_time_ms || 0} ms</span></div>
    <button class="btn" style="margin-left:auto; font-size:11px; padding:4px 8px;" onclick="downloadExcel('${prefix}')">
      <i data-lucide="download" style="width:12px;height:12px"></i> <span class="d-hide-mobile">${t('download')}</span>
    </button>
  `;
  lucide.createIcons();
  renderDetections(prefix, data.detections);
}

function renderBatchGallery(prefix) {
  const wrap = document.getElementById(prefix + '-batch-wrap');
  const list = document.getElementById(prefix + '-batch-list');
  if (imageQueue.length <= 0) { wrap.style.display = 'none'; return; }
  wrap.style.display = 'block';
  list.innerHTML = imageQueue.map((item, idx) => {
    let badgeClass = 'ok', badgeText = t('pending');
    if (item.status === 'processing') { badgeClass = 'ok'; badgeText = '...'; }
    else if (item.status === 'done' && item.result) {
      const infractions = item.result.detections.filter(d => d.class_name.toLowerCase().includes('without')).length;
      badgeClass = infractions > 0 ? 'warn' : 'ok';
      badgeText = infractions > 0 ? `${infractions} Inf.` : 'OK';
    }
    return `
      <div class="batch-item" id="${prefix}-batch-${idx}" onclick="showBatchResult('${prefix}', ${idx})">
        <div class="batch-item-remove" onclick="removeFromQueue(${idx}, event)">
          <i data-lucide="x" style="width:10px;height:10px"></i>
        </div>
        <div class="batch-item-name">${item.file.name}</div>
        <div class="batch-item-stats">
          <span class="stat-val" style="font-size:10px">${item.result ? item.result.count : 0} Det.</span>
          <span class="batch-badge ${badgeClass}">${badgeText}</span>
        </div>
      </div>`;
  }).join('');
  lucide.createIcons();
}

function removeFromQueue(idx, event) {
  if (event) event.stopPropagation();
  imageQueue.splice(idx, 1);
  lastResults['img'] = imageQueue.filter(iq => iq.status === 'done').map(iq => iq.result);
  renderBatchGallery('img');
  if (imageQueue.length === 0) clearQueue();
  else document.getElementById('img-preview').innerHTML = '';
}

function showBatchResult(prefix, idx) {
  const item = imageQueue[idx];
  if (!item) return;
  document.querySelectorAll('.batch-item').forEach(el => el.classList.remove('active'));
  const target = document.getElementById(`${prefix}-batch-${idx}`);
  if (target) target.classList.add('active');
  if (item.result) {
    showResult(prefix, item.result);
  } else {
    const reader = new FileReader();
    reader.onload = ev => {
      const preview = document.getElementById(prefix + '-preview');
      preview.style.display = 'flex';
      preview.innerHTML = `<img src="${ev.target.result}">`;
      document.getElementById(prefix + '-stats').innerHTML = '';
      document.getElementById(prefix + '-detections').innerHTML = `<div class="empty">${t('pending')}...</div>`;
    };
    reader.readAsDataURL(item.file);
  }
}

let lastResults = {};

function downloadExcel(prefix) {
  if (typeof XLSX === 'undefined') {
    alert("Excel library is still loading, please try again.");
    return;
  }

  const results = lastResults[prefix];
  if (!results) return;
  const resArray = Array.isArray(results) ? results : [results];
  if (resArray.length === 0) return;

  // ── Palette ──────────────────────────────────────────────────────────────
  const C = {
    blue: "2563EB",
    blueDark: "1E40AF",
    blueLight: "DBEAFE",
    green: "16A34A",
    greenLight: "DCFCE7",
    red: "DC2626",
    redLight: "FEE2E2",
    gray: "6B7280",
    grayLight: "F9FAFB",
    grayMid: "E5E7EB",
    dark: "111827",
    white: "FFFFFF",
    yellow: "D97706",
    yellowLight: "FEF3C7",
  };

  // ── Cell factory helpers ─────────────────────────────────────────────────
  const cell = (v, type = "s", style = {}) => ({ v, t: type, s: style });
  const empty = () => ({ v: "", t: "s", s: {} });

  const hdr = (v, bg = C.blue, fg = C.white, sz = 11) => cell(v, "s", {
    font: { bold: true, sz, color: { rgb: fg }, name: "Calibri" },
    fill: { fgColor: { rgb: bg } },
    alignment: { horizontal: "center", vertical: "center", wrapText: true },
    border: {
      top: { style: "thin", color: { rgb: C.grayMid } },
      bottom: { style: "thin", color: { rgb: C.grayMid } },
      left: { style: "thin", color: { rgb: C.grayMid } },
      right: { style: "thin", color: { rgb: C.grayMid } },
    }
  });

  const metaCell = (v, bold = false, color = C.gray) => cell(v, "s", {
    font: { bold, sz: 10, color: { rgb: color }, name: "Calibri" },
    alignment: { vertical: "center" }
  });

  const kpiCell = (v, type = "n", bg = C.blueLight, fg = C.blueDark) => cell(v, type, {
    font: { bold: true, sz: 20, color: { rgb: fg }, name: "Calibri" },
    fill: { fgColor: { rgb: bg } },
    alignment: { horizontal: "center", vertical: "center" },
    border: {
      top: { style: "medium", color: { rgb: fg } },
      bottom: { style: "medium", color: { rgb: fg } },
      left: { style: "medium", color: { rgb: fg } },
      right: { style: "medium", color: { rgb: fg } },
    }
  });

  const kpiLabel = (v, bg = C.blueLight, fg = C.blueDark) => cell(v, "s", {
    font: { bold: true, sz: 9, color: { rgb: fg }, name: "Calibri" },
    fill: { fgColor: { rgb: bg } },
    alignment: { horizontal: "center", vertical: "center", wrapText: true },
    border: {
      top: { style: "medium", color: { rgb: fg } },
      bottom: { style: "medium", color: { rgb: fg } },
      left: { style: "medium", color: { rgb: fg } },
      right: { style: "medium", color: { rgb: fg } },
    }
  });

  const dataCell = (v, type = "s", style = {}) => cell(v, type, {
    font: { sz: 10, name: "Calibri", ...style.font },
    alignment: { vertical: "center", horizontal: "left", ...style.alignment },
    border: {
      top: { style: "thin", color: { rgb: C.grayMid } },
      bottom: { style: "thin", color: { rgb: C.grayMid } },
      left: { style: "thin", color: { rgb: C.grayMid } },
      right: { style: "thin", color: { rgb: C.grayMid } },
    },
    fill: style.fill || undefined,
  });

  const confBar = (pct) => {
    // Returns a text "progress bar" using Unicode blocks
    const filled = Math.round(pct / 10);
    return "█".repeat(filled) + "░".repeat(10 - filled) + `  ${pct.toFixed(1)}%`;
  };

  // ── Compute stats (1 row per image) ─────────────────────────────────────
  let totalWith = 0, totalWithout = 0;
  const rows = [];

  resArray.forEach(res => {
    const fname = res.filename || "N/A";
    if (!res.detections || res.detections.length === 0) {
      rows.push({ fname, withCount: 0, withoutCount: 0, dominant: t("empty"), conf: 0, isViolation: false });
      return;
    }
    const withDets = res.detections.filter(d => !d.class_name.toLowerCase().includes("without"));
    const withoutDets = res.detections.filter(d => d.class_name.toLowerCase().includes("without"));
    const dominant = res.detections.sort((a, b) => b.confidence - a.confidence)[0];
    const isViolation = dominant.class_name.toLowerCase().includes("without");

    if (isViolation) totalWithout++; else totalWith++;

    rows.push({
      fname,
      withCount: withDets.length,
      withoutCount: withoutDets.length,
      dominant: t(dominant.class_name),
      conf: dominant.confidence * 100,
      isViolation,
    });
  });

  const complianceRate = rows.length > 0 ? ((totalWith / rows.length) * 100).toFixed(1) : "0.0";
  const ts = new Date().toLocaleString();

  // ── Build worksheet data (AOA) ───────────────────────────────────────────
  // Row 1 — Title banner (merged A1:F1)
  const titleStyle = {
    font: { bold: true, sz: 18, color: { rgb: C.white }, name: "Calibri" },
    fill: { fgColor: { rgb: C.blueDark } },
    alignment: { horizontal: "center", vertical: "center" },
  };

  const subtitleStyle = {
    font: { sz: 10, italic: true, color: { rgb: C.white }, name: "Calibri" },
    fill: { fgColor: { rgb: C.blue } },
    alignment: { horizontal: "center", vertical: "center" },
  };

  const sectionHdr = (label) => cell(label, "s", {
    font: { bold: true, sz: 11, color: { rgb: C.blueDark }, name: "Calibri" },
    fill: { fgColor: { rgb: C.blueLight } },
    alignment: { vertical: "center" },
    border: {
      bottom: { style: "medium", color: { rgb: C.blue } },
    }
  });

  const wsData = [
    // R1 — banner
    [cell("🛡️  Helmet Detection Report", "s", titleStyle), empty(), empty(), empty(), empty(), empty()],
    // R2 — subtitle
    [cell(`Generated: ${ts}  |  Source: YOLOv8  |  Mode: ${prefix.toUpperCase()}`, "s", subtitleStyle), empty(), empty(), empty(), empty(), empty()],
    // R3 — spacer
    [empty(), empty(), empty(), empty(), empty(), empty()],

    // R4 — KPI header labels
    [
      kpiLabel("📷 Images\nAnalyzed", C.blueLight, C.blueDark),
      kpiLabel("🔍 Total\nDetections", C.blueLight, C.blueDark),
      kpiLabel("✅ With\nHelmet", C.greenLight, C.green),
      kpiLabel("❌ Without\nHelmet", C.redLight, C.red),
      kpiLabel("📊 Compliance\nRate", C.yellowLight, C.yellow),
      empty(),
    ],
    // R5 — KPI values
    [
      kpiCell(rows.length, "n", C.blueLight, C.blueDark),
      kpiCell(rows.reduce((s, r) => s + r.withCount + r.withoutCount, 0), "n", C.blueLight, C.blueDark),
      kpiCell(totalWith, "n", C.greenLight, C.green),
      kpiCell(totalWithout, "n", C.redLight, C.red),
      kpiCell(complianceRate + "%", "s", C.yellowLight, C.yellow),
      empty(),
    ],

    // R6 — spacer
    [empty(), empty(), empty(), empty(), empty(), empty()],

    // R7 — section header
    [sectionHdr("  DETECTION DETAILS"), empty(), empty(), empty(), empty(), empty()],

    // R8 — table column headers
    [
      hdr("Filename", C.dark, C.white),
      hdr("✅ With", C.dark, C.white),
      hdr("❌ Without", C.dark, C.white),
      hdr("Dominant", C.dark, C.white),
      hdr("Conf.", C.dark, C.white),
      hdr("Status", C.dark, C.white),
    ],
  ];

  // R9+ — data rows (1 per image, zebra striping)
  rows.forEach((r, i) => {
    const isEven = i % 2 === 0;
    const rowBg = isEven ? C.white : C.grayLight;
    const domColor = r.isViolation ? C.red : C.green;
    const statusText = r.dominant === t("empty") ? "—" : r.isViolation ? "❌ Violation" : "✅ Compliant";
    const statusBg = r.isViolation ? C.redLight : C.greenLight;
    const statusFg = r.isViolation ? C.red : C.green;

    const baseBorder = {
      top: { style: "thin", color: { rgb: C.grayMid } },
      bottom: { style: "thin", color: { rgb: C.grayMid } },
      left: { style: "thin", color: { rgb: C.grayMid } },
      right: { style: "thin", color: { rgb: C.grayMid } },
    };

    wsData.push([
      // Filename
      cell(r.fname, "s", {
        font: { sz: 10, name: "Calibri", color: { rgb: C.dark } },
        fill: { fgColor: { rgb: rowBg } },
        alignment: { vertical: "center" },
        border: baseBorder,
      }),
      // With count
      cell(r.withCount, "n", {
        font: { bold: true, sz: 11, name: "Calibri", color: { rgb: C.green } },
        fill: { fgColor: { rgb: rowBg } },
        alignment: { vertical: "center", horizontal: "center" },
        border: baseBorder,
      }),
      // Without count
      cell(r.withoutCount, "n", {
        font: { bold: true, sz: 11, name: "Calibri", color: { rgb: r.withoutCount > 0 ? C.red : C.gray } },
        fill: { fgColor: { rgb: rowBg } },
        alignment: { vertical: "center", horizontal: "center" },
        border: baseBorder,
      }),
      // Dominant class
      cell(r.dominant, "s", {
        font: { bold: true, sz: 10, name: "Calibri", color: { rgb: domColor } },
        fill: { fgColor: { rgb: rowBg } },
        alignment: { vertical: "center", horizontal: "center" },
        border: baseBorder,
      }),
      // Confidence of dominant (visual bar)
      cell(r.conf > 0 ? confBar(r.conf) : "—", "s", {
        font: { sz: 9, name: "Courier New", color: { rgb: domColor } },
        fill: { fgColor: { rgb: rowBg } },
        alignment: { vertical: "center" },
        border: baseBorder,
      }),
      // Status
      cell(statusText, "s", {
        font: { bold: true, sz: 10, name: "Calibri", color: { rgb: statusFg } },
        fill: { fgColor: { rgb: statusBg } },
        alignment: { vertical: "center", horizontal: "center" },
        border: baseBorder,
      }),
    ]);
  });

  // ── Build sheet ──────────────────────────────────────────────────────────
  const ws = XLSX.utils.aoa_to_sheet(wsData);

  // Column widths
  ws["!cols"] = [
    { wch: 34 }, // Filename
    { wch: 10 }, // With count
    { wch: 12 }, // Without count
    { wch: 18 }, // Dominant
    { wch: 22 }, // Conf bar
    { wch: 16 }, // Status
  ];

  // Row heights
  ws["!rows"] = [
    { hpt: 36 }, // R1 title
    { hpt: 18 }, // R2 subtitle
    { hpt: 8 }, // R3 spacer
    { hpt: 32 }, // R4 KPI labels
    { hpt: 42 }, // R5 KPI values
    { hpt: 8 }, // R6 spacer
    { hpt: 22 }, // R7 section header
    { hpt: 26 }, // R8 table header
    ...rows.map(() => ({ hpt: 20 })),
  ];

  // Merges: title, subtitle, section header span full width (A:F)
  ws["!merges"] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: 5 } }, // title
    { s: { r: 1, c: 0 }, e: { r: 1, c: 5 } }, // subtitle
    { s: { r: 6, c: 0 }, e: { r: 6, c: 5 } }, // section header
  ];

  // ── Chart sheet (summary bar chart data) ────────────────────────────────
  const wsChart = XLSX.utils.aoa_to_sheet([
    [hdr("Category", C.dark, C.white), hdr("Count", C.dark, C.white)],
    [
      cell(t("With Helmet"), "s", { font: { bold: true, color: { rgb: C.green }, name: "Calibri" } }),
      cell(totalWith, "n", { font: { bold: true, name: "Calibri" }, alignment: { horizontal: "center" } }),
    ],
    [
      cell(t("Without Helmet"), "s", { font: { bold: true, color: { rgb: C.red }, name: "Calibri" } }),
      cell(totalWithout, "n", { font: { bold: true, name: "Calibri" }, alignment: { horizontal: "center" } }),
    ],
    [
      cell("Compliance Rate", "s", { font: { bold: true, color: { rgb: C.yellow }, name: "Calibri" } }),
      cell(parseFloat(complianceRate) / 100, "n", {
        font: { bold: true, name: "Calibri" },
        numFmt: "0.0%",
        alignment: { horizontal: "center" },
      }),
    ],
  ]);
  wsChart["!cols"] = [{ wch: 22 }, { wch: 14 }];

  // ── Workbook ─────────────────────────────────────────────────────────────
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "📋 Report");
  XLSX.utils.book_append_sheet(wb, wsChart, "📊 Summary Data");

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  XLSX.writeFile(wb, `helmet_report_${timestamp}.xlsx`);
}



// ── IMAGE QUEUE ──────────────────────────────────────────────────────────────
let imageQueue = [];

function handleDrop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.remove('drag');
  addFilesToQueue(e.dataTransfer.files);
}

function previewImage(input) {
  addFilesToQueue(input.files);
  input.value = '';
}

function addFilesToQueue(files) {
  if (!files || files.length === 0) return;
  for (let f of files) {
    if (f.type.startsWith('image/')) imageQueue.push({ file: f, result: null, status: 'pending' });
  }
  renderBatchGallery('img');
  document.getElementById('img-btn').disabled = false;
  const last = imageQueue[imageQueue.length - 1];
  if (last) {
    const reader = new FileReader();
    reader.onload = ev => {
      const preview = document.getElementById('img-preview');
      preview.style.display = 'flex';
      preview.innerHTML = `<img src="${ev.target.result}">`;
    };
    reader.readAsDataURL(last.file);
  }
}

function clearQueue() {
  imageQueue = [];
  lastResults['img'] = [];
  document.getElementById('img-batch-wrap').style.display = 'none';
  document.getElementById('img-preview').style.display = 'none';
  document.getElementById('img-stats').innerHTML = '';
  document.getElementById('img-detections').innerHTML = '';
  document.getElementById('img-btn').disabled = true;
}

async function detectImage() {
  const btn = document.getElementById('img-btn');
  btn.disabled = true;
  const conf = document.getElementById('img-conf').value / 100;
  const iou = document.getElementById('img-iou').value / 100;
  lastResults['img'] = lastResults['img'] || [];
  for (let i = 0; i < imageQueue.length; i++) {
    const item = imageQueue[i];
    if (item.status !== 'pending') continue;
    item.status = 'processing';
    renderBatchGallery('img');
    btn.innerHTML = `<div class="loader"></div> Analyzing…`;
    try {
      const fd = new FormData();
      fd.append('file', item.file);
      const res = await fetch(`/detect?conf=${conf}&iou=${iou}`, { method: 'POST', body: fd });
      const data = await res.json();
      data.filename = item.file.name;
      item.result = data;
      item.status = 'done';
      lastResults['img'].push(data);
      showResult('img', data);
      renderBatchGallery('img');
      document.getElementById(`img-batch-${i}`).classList.add('active');
    } catch (e) {
      console.error('Error on file', item.file.name, e);
      item.status = 'error';
    }
  }
  btn.disabled = false;
  btn.innerHTML = t('run');
}

// ── URL ──────────────────────────────────────────────────────────────────────
async function detectUrl() {
  const url = document.getElementById('img-url').value;
  if (!url) return;
  const btn = document.getElementById('url-btn');
  btn.disabled = true;
  btn.innerHTML = `<div class="loader"></div> Analyzing…`;
  try {
    const conf = document.getElementById('url-conf').value / 100;
    const res = await fetch(`/detect/url?url=${encodeURIComponent(url)}&conf=${conf}`, { method: 'POST' });
    const data = await res.json();
    lastResults['url'] = data;
    document.getElementById('url-preview').style.display = 'flex';
    showResult('url', data);
  } finally {
    btn.disabled = false;
    btn.innerHTML = t('run');
  }
}

// ── VIDEO AI PLAYER ──────────────────────────────────────────────────────────
let vidWS = null;
let vidInterval = null;
let vidRunning = false;

function loadVideoIntoPlayer(input) {
  const file = input.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  const player = document.getElementById('vid-player');
  const wrap = document.getElementById('vid-preview-wrap');
  const drop = document.getElementById('vid-drop-zone');

  player.src = url;
  wrap.style.display = 'block';
  drop.style.display = 'none';

  // Size the overlay canvas once metadata is ready
  player.onloadedmetadata = () => {
    syncOverlaySize();
    updateVidProgress();
  };

  player.onplay = () => { startVidAI(); updateVidIcons(true); };
  player.onpause = () => { stopVidAI(); updateVidIcons(false); };
  player.onended = () => { stopVidAI(); updateVidIcons(false); };
  player.ontimeupdate = updateVidProgress;
}

function removeVideo() {
  stopVidAI();
  const player = document.getElementById('vid-player');
  const wrap = document.getElementById('vid-preview-wrap');
  const drop = document.getElementById('vid-drop-zone');
  const fileInput = document.getElementById('vid-file');

  player.pause();
  player.src = "";
  fileInput.value = "";
  wrap.style.display = 'none';
  drop.style.display = 'flex';
  
  // Clear any stats/detections
  document.getElementById('vid-stats').innerHTML = '';
  document.getElementById('vid-detections').innerHTML = '';
}

/** Keep the canvas pixel-size in sync with the video element's rendered size */
function syncOverlaySize() {
  const player = document.getElementById('vid-player');
  const canvas = document.getElementById('vid-overlay');
  // Use the video's natural resolution so coordinates match 1:1
  canvas.width = player.videoWidth || player.clientWidth;
  canvas.height = player.videoHeight || player.clientHeight;
}

function toggleVidPlay() {
  const player = document.getElementById('vid-player');
  if (player.paused) player.play();
  else player.pause();
}

function updateVidIcons(isPlaying) {
  const icon = document.getElementById('vid-play-icon');
  icon.setAttribute('data-lucide', isPlaying ? 'pause' : 'play');
  lucide.createIcons();
}

function updateVidProgress() {
  const player = document.getElementById('vid-player');
  const progress = document.getElementById('vid-progress');
  const timeDisp = document.getElementById('vid-time-display');
  if (!player.duration) return;
  const pct = (player.currentTime / player.duration) * 100;
  progress.style.width = pct + '%';
  const fmt = s => `${Math.floor(s / 60).toString().padStart(2, '0')}:${Math.floor(s % 60).toString().padStart(2, '0')}`;
  timeDisp.textContent = `${fmt(player.currentTime)} / ${fmt(player.duration)}`;
}

function seekVid(e) {
  const player = document.getElementById('vid-player');
  const rect = e.currentTarget.getBoundingClientRect();
  player.currentTime = ((e.clientX - rect.left) / rect.width) * player.duration;
  setTimeout(() => syncVidFrame(true), 50);
}

function startVidAI() {
  if (vidRunning) return;
  vidRunning = true;

  const conf = document.getElementById('vid-conf').value / 100;
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  vidWS = new WebSocket(`${proto}://${location.host}/ws/detect`);

  vidWS.onopen = () => {
    console.log('Video WS connected');
    // Send frames at ~10 fps (every 100 ms)
    vidInterval = setInterval(() => syncVidFrame(false), 100);
  };

  vidWS.onmessage = e => {
    const data = JSON.parse(e.data);
    drawVidOverlay(data);

    document.getElementById('vid-stats').innerHTML = `
      <div class="stat-chip">
        <span class="stat-label">${t('detections')}</span>
        <span class="stat-val">${data.count || 0}</span>
      </div>
      <div class="stat-chip">
        <span class="stat-label">${t('inference')}</span>
        <span class="stat-val">${data.inference_time_ms || 0}ms</span>
      </div>`;

    if (data.detections) renderDetections('vid', data.detections);
  };

  vidWS.onerror = err => console.error('Video WS error', err);
  vidWS.onclose = () => { vidRunning = false; };
}

function stopVidAI() {
  if (vidInterval) clearInterval(vidInterval);
  vidInterval = null;
  if (vidWS) { vidWS.close(); vidWS = null; }
  vidRunning = false;

  // Clear overlay
  const canvas = document.getElementById('vid-overlay');
  if (canvas) canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
  const stats = document.getElementById('vid-stats');
  if (stats) stats.innerHTML = '';
}

function syncVidFrame(force = false) {
  const video = document.getElementById('vid-player');
  const canvas = document.getElementById('cam-canvas'); // hidden scratch canvas
  if (!video || !video.videoWidth) return;
  if (!force && (video.paused || video.ended)) return;
  if (!vidWS || vidWS.readyState !== WebSocket.OPEN) return;

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  const conf = document.getElementById('vid-conf').value / 100;
  const b64 = canvas.toDataURL('image/jpeg', 0.6).split(',')[1];
  vidWS.send(JSON.stringify({ image: b64, conf }));
}

/**
 * Draw bounding boxes onto the transparent overlay canvas.
 * The backend returns detections with `bbox: [x1, y1, x2, y2]`  ← fix was here
 */
function drawVidOverlay(data) {
  const video = document.getElementById('vid-player');
  const canvas = document.getElementById('vid-overlay');
  if (!video || !video.videoWidth) return;

  // Keep canvas resolution in sync
  if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
  }

  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!data.detections || data.detections.length === 0) return;

  data.detections.forEach(det => {
    // ✅ backend sends `bbox`, not `box`
    const [x1, y1, x2, y2] = det.bbox;
    const color = det.class_name.toLowerCase().includes('without') ? '#f87171' : '#4ade80';
    const w = x2 - x1, h = y2 - y1;

    // Box
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.strokeRect(x1, y1, w, h);

    // Label background
    const label = `${t(det.class_name)} ${(det.confidence * 100).toFixed(0)}%`;
    ctx.font = 'bold 15px sans-serif';
    const tw = ctx.measureText(label).width;
    const lh = 22;
    const ly = y1 >= lh ? y1 - lh : y1 + lh;   // flip below if too close to top

    ctx.fillStyle = color;
    ctx.fillRect(x1 - 1, ly - lh + 4, tw + 10, lh);

    // Label text
    ctx.fillStyle = '#000';
    ctx.fillText(label, x1 + 4, ly - 2);
  });
}

// ── WEBCAM ───────────────────────────────────────────────────────────────────
let ws = null, camStream = null, camInterval = null;

async function startWebcam() {
  try {
    camStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
    const videoEl = document.getElementById('webcam-video');
    videoEl.srcObject = camStream;

    const preview = document.getElementById('cam-preview');
    preview.innerHTML = `<video autoplay muted playsinline id="cam-live-mirror" style="width:100%;height:100%;object-fit:contain;"></video>`;
    document.getElementById('cam-live-mirror').srcObject = camStream;
  } catch (e) { alert('Webcam unavailable: ' + e.message); return; }

  document.getElementById('cam-start-btn').style.display = 'none';
  document.getElementById('cam-stop-btn').style.display = 'inline-flex';

  const conf = document.getElementById('cam-conf').value / 100;
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  ws = new WebSocket(`${proto}://${location.host}/ws/detect`);

  ws.onopen = () => {
    const dot = document.getElementById('ws-dot');
    const lbl = document.getElementById('ws-label');
    dot.style.background = '#4ade80';
    lbl.textContent = 'Live';
    const fps = parseInt(document.getElementById('cam-fps').value);
    camInterval = setInterval(sendFrame, 1000 / fps);
  };

  ws.onmessage = e => {
    const data = JSON.parse(e.data);
    const preview = document.getElementById('cam-preview');

    if (data.annotated_image) {
      let canvas = preview.querySelector('#cam-render-canvas');
      if (!canvas) {
        preview.innerHTML = '<canvas id="cam-render-canvas" style="width:100%;height:100%;object-fit:contain;"></canvas>';
        canvas = preview.querySelector('#cam-render-canvas');
      }
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.onload = () => { canvas.width = img.width; canvas.height = img.height; ctx.drawImage(img, 0, 0); };
      img.src = `data:image/jpeg;base64,${data.annotated_image}`;
    }

    document.getElementById('cam-stats').innerHTML = `
      <div class="stat-chip" style="background:rgba(0,0,0,0.5);backdrop-filter:blur(4px)">
        <span class="stat-label">${t('detections')}</span><span class="stat-val">${data.count || 0}</span>
      </div>
      <div class="stat-chip" style="background:rgba(0,0,0,0.5);backdrop-filter:blur(4px)">
        <span class="stat-label">${t('inference')}</span><span class="stat-val">${data.inference_time_ms || 0}ms</span>
      </div>`;

    if (data.detections) renderDetections('cam', data.detections);
  };

  ws.onerror = err => { console.error('WebSocket error:', err); alert('WebSocket connection failed.'); stopWebcam(); };
  ws.onclose = () => {
    const dot = document.getElementById('ws-dot');
    const lbl = document.getElementById('ws-label');
    if (dot) dot.style.background = '#f87171';
    if (lbl) lbl.textContent = 'Offline';
  };

  const video = document.getElementById('webcam-video');
  video.style.cssText = "position:fixed;bottom:20px;right:20px;width:160px;height:120px;z-index:9999;border:2px solid var(--blue);border-radius:8px;display:block;object-fit:cover;background:black;box-shadow:0 10px 25px rgba(0,0,0,.5);";
}

function sendFrame() {
  const video = document.getElementById('webcam-video');
  const canvas = document.getElementById('cam-canvas');
  if (!video || !video.videoWidth) return;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const conf = document.getElementById('cam-conf').value / 100;
  const b64 = canvas.toDataURL('image/jpeg', 0.6).split(',')[1];
  if (ws?.readyState === WebSocket.OPEN) ws.send(JSON.stringify({ image: b64, conf }));
}

function stopWebcam() {
  clearInterval(camInterval);
  if (ws) ws.close();
  if (camStream) camStream.getTracks().forEach(t => t.stop());
  const video = document.getElementById('webcam-video');
  video.srcObject = null;
  video.style.display = 'none';
  document.getElementById('cam-start-btn').style.display = 'inline-flex';
  document.getElementById('cam-stop-btn').style.display = 'none';
}

applyTranslations();