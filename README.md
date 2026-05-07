# 🔬 ScanMind AI — Brain Tumor Detection & Classification

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

**Système de détection et classification des tumeurs cérébrales par IRM**  
*Développé dans le cadre d'une spécialisation en Data Science & Intelligence Artificielle*

</div>

---

## 📌 Présentation

ScanMind AI est un système d'aide au diagnostic médical basé sur le Deep Learning. Il analyse des images IRM cérébrales pour détecter et classifier automatiquement les tumeurs, tout en identifiant les cas atypiques grâce à une approche hybride CNN + Autoencodeur.

> ⚠️ **Usage académique uniquement** — Ce système ne remplace pas un avis médical professionnel.

---

## 🚀 Architecture Technique

Le système repose sur deux modèles complémentaires travaillant en parallèle :

```
Image IRM
    │
    ├──► Classifier CNN (EfficientNetB0)
    │         └── Transfer Learning (ImageNet)
    │         └── Fine-Tuning (30 dernières couches)
    │         └── Sortie : 4 probabilités (Softmax)
    │
    └──► Autoencodeur (Détection d'Anomalies)
              └── Encodeur : 224x224 → espace latent 28x28
              └── Décodeur : 28x28 → 224x224
              └── Sortie : Erreur de reconstruction (MSE)
```

### Logique de décision finale

| Condition | Résultat |
|-----------|----------|
| MSE > seuil (0.013) | 🔴 Cas atypique — expertise humaine requise |
| Confiance < 70% | 🟡 Résultat incertain — révision manuelle |
| Notumor détecté | 🟢 Tissu sain confirmé |
| Tumeur + confiance ≥ 70% | 🔴 Anomalie détectée |

---

## 🧠 Classes Détectées

| Index | Classe | Pathologie | Nature |
|-------|--------|-----------|--------|
| 0 | `glioma` | Gliome cérébral | Maligne |
| 1 | `meningioma` | Méningiome | Bénigne |
| 2 | `notumor` | Tissu sain | Sain ✅ |
| 3 | `pituitary` | Adénome hypophysaire | Bénigne |

---

## 📊 Performances

| Métrique | Valeur |
|----------|--------|
| Précision moyenne | > 95% sur les 4 classes |
| Score de confiance | > 95% |
| Erreur de reconstruction (MSE) | ~0.002 (stable) |
| ROC-AUC moyen | > 0.95 |

---

## 🗂️ Structure du Projet

```
scanmind-ai/
├── api.py                     # API FastAPI — endpoints /health et /predict
├── app.py                     # Interface Streamlit — ScanMind AI
├── class_names.json           # Ordre alphabétique des classes
├── classifier_final.keras/    # Modèle classifier (config + poids)
├── autoencoder_final.keras/   # Modèle autoencodeur (config + poids)
└── README.md
```

---

## ⚙️ Installation

```bash
# Cloner le repo
git clone https://github.com/SouissiOumaima/scanmind-ai.git
cd scanmind-ai

# Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux / macOS

# Installer les dépendances
pip install fastapi uvicorn tensorflow pillow numpy streamlit requests
```

---

## ▶️ Lancement

```bash
# Terminal 1 — Lancer l'API FastAPI
uvicorn api:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 — Lancer l'interface Streamlit
streamlit run app.py
```

Vérifier que l'API fonctionne :
```
http://127.0.0.1:8000/health
```

Interface disponible sur :
```
http://localhost:8501
```

---

## 🔌 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Statut de l'API et des modèles |
| `POST` | `/predict` | Analyse d'une image IRM |

### Exemple de réponse `/predict`

```json
{
  "prediction": "GLIOMA",
  "confidence": 97.34,
  "reconstruction_error": 0.002341,
  "status": "Anomalie détectée",
  "probabilities": {
    "glioma": 97.34,
    "meningioma": 1.20,
    "notumor": 0.80,
    "pituitary": 0.66
  }
}
```

---

## 📦 Dataset

- **Source** : [Brain Tumor MRI Dataset — Kaggle](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
- **Training** : ~2 700 images
- **Testing** : ~1 300 images
- **Augmentation** : rotation, flip, zoom, décalage

---

## 🛠️ Stack Technologique

| Composant | Technologie |
|-----------|------------|
| Modèles DL | TensorFlow / Keras 3.10 |
| Base CNN | EfficientNetB0 (ImageNet) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Traitement image | Pillow + NumPy + OpenCV |
| Langage | Python 3.12 |

---

## 👩‍💻 Auteur

**Souissi Oumaima**  
Spécialisation Data Science & Intelligence Artificielle  
Année académique 2025 – 2026

---

<div align="center">
<i>Usage académique uniquement — Non destiné à un usage clinique réel</i>
</div>
