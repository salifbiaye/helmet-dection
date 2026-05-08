# 👷 Helmet Detection System — YOLOv8 & MLOps

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Airflow](https://img.shields.io/badge/Airflow-MLOps-red?style=for-the-badge&logo=apacheairflow)

Un système complet de détection d'équipements de protection individuelle (Casques EPI) utilisant **YOLOv8**, déployé via **FastAPI** et orchestré par **Apache Airflow** pour le re-entraînement automatique.

---

## 🚀 Fonctionnalités

- **Détection Multi-sources** : Supporte les images (Upload/URL), les vidéos (MP4) et le flux Webcam en temps réel (WebSocket).
- **Inférence Optimisée** : Backend FastAPI asynchrone avec fusion de couches pour une performance accrue sur CPU.
- **Pipeline MLOps** : Orchestration Airflow pour surveiller les nouvelles données et automatiser le fine-tuning.
- **Reporting Analytique** : Export des résultats de détection au format Excel.
- **Documentation Interactive** : API entièrement documentée via Swagger UI et ReDoc.

---

## 🖥️ Interface Utilisateur

L'application web offre une interface intuitive pour la détection sur divers médias :

**Détection sur Flux Vidéo (Live / Fichier)**
![Live Video Detection](parti3-img/video-live-detection.png)

**Détection sur Image (Casque Détecté)**
![Image with Helmet](parti3-img/salif-image-withhelemt.png)

**Détection sur Image (Pas de Casque Détecté)**
![Image without Helmet](parti3-img/salif-imagewithout-helmet.png)

---

## 🛠️ Architecture Technique

- **Modèle** : YOLOv8n (Ultralytics) fine-tuné sur un dataset spécifique de casques de chantier.
- **Backend** : FastAPI (Python 3.11).
- **Frontend** : Vanilla JS / CSS3 (Interface réactive et légère).
- **Orchestration** : Apache Airflow (SequentialExecutor + SQLite).
- **Conteneurisation** : Docker & Docker Compose.

---

## 📦 Installation et Lancement

### Pré-requis
- Docker et Docker Compose installés sur votre machine.

### Démarrage Rapide
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/salifbiaye/helmet-dection.git
   cd helmet-dection
   ```

2. Lancez les services :
   ```bash
   docker-compose up --build
   ```

3. Accédez aux interfaces :
   - **Frontend App** : [http://localhost:8081](http://localhost:8081)
   - **Airflow UI** : [http://localhost:8082](http://localhost:8082) (admin / admin)
   - **API Swagger** : [http://localhost:8081/docs](http://localhost:8081/docs)

---

## 📁 Structure du Projet

```text
├── airflow/              # DAGs et configuration Airflow
├── backend/              # Code source FastAPI
│   ├── frontend/         # Interface Web (HTML/JS/CSS)
│   ├── models/           # Modèles YOLO (.pt, .onnx)
│   └── main.py           # Point d'entrée API
├── data/                 # Dossier local pour le re-entraînement (ignoré git)
└── docker-compose.yml    # Orchestration des services
```

---

## 🎓 Projet Académique
Ce projet a été réalisé dans le cadre du module **Computer Vision & Deep Learning** au sein du **DIC3 Informatique & Télécommunications** — **ESP/UCAD**.

**Auteurs** : Salif Biaye, Ndeye Astou Diagouraga & Moussa Ndoye
