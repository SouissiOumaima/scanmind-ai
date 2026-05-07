import os
import io
import json
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# --- Configuration des Chemins ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

classifier = None
autoencoder = None

# ORDRE CORRIGÉ : L'ordre alphabétique standard utilisé par Keras
# --- ORDRE ALPHABÉTIQUE DÉDUIT DE TON IMAGE ---
# 0: glioma, 1: meningioma, 2: notumor, 3: pituitary
class_names = ["glioma", "meningioma", "notumor", "pituitary"]

def load_safe_model(model_folder_name):
    """Charge le modèle en gérant les chemins relatifs et les objets personnalisés."""
    model_folder = os.path.join(BASE_DIR, model_folder_name)
    config_path = os.path.join(model_folder, "config.json")
    
    # Détection des poids (dans le dossier ou à la racine)
    weights_path = os.path.join(model_folder, "model.weights.h5")
    if not os.path.exists(weights_path):
        prefix = model_folder_name.split('_')[0]
        weights_path = os.path.join(BASE_DIR, f"{prefix}.model.weights.h5")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config manquante : {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)
    
    # Reconstruction avec bypass de la fonction de perte pour l'inférence
    model = tf.keras.models.model_from_json(
        json.dumps(config), 
        custom_objects={"loss_fn": lambda x, y: 0}
    )
    model.load_weights(weights_path)
    return model

# --- Chargement au Démarrage ---
try:
    classifier = load_safe_model("classifier_final.keras")
    autoencoder = load_safe_model("autoencoder_final.keras")
    print(f"✅ Système prêt. Ordre des classes : {class_names}")
except Exception as e:
    print(f"❌ Erreur de chargement : {e}")

@app.get("/health")
async def health():
    return {
        "status": "online", 
        "classifier_ready": classifier is not None,
        "autoencoder_ready": autoencoder is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # --- PRÉTRAITEMENT CLASSIFIER ---
        # On essaie SANS division par 255 d'abord, car beaucoup de modèles 
        # Keras intègrent déjà une couche de Rescaling.
        img_380 = pil_image.resize((380, 380))
        img_array = np.array(img_380, dtype=np.float32)
        batch_380 = np.expand_dims(img_array, axis=0) 

        # --- INFÉRENCE ---
        cls_preds = classifier.predict(batch_380, verbose=0)
        cls_idx = np.argmax(cls_preds[0])
        confidence = float(np.max(cls_preds[0]) * 100)

        # --- AUTOENCODER (Double vérification) ---
        img_224 = pil_image.resize((224, 224))
        batch_224 = np.expand_dims(np.array(img_224, dtype=np.float32) / 255.0, axis=0)
        recon = autoencoder.predict(batch_224, verbose=0)
        recon_error = float(np.mean(np.square(batch_224 - recon)))

        prediction_label = class_names[cls_idx]

        # LOGIQUE DE SÉCURITÉ : 
        # Si l'erreur de reconstruction est très faible, c'est probablement sain
        # même si le classifier se trompe.
        if recon_error < 0.0015:
            final_label = "NOTUMOR"
            status = "Sain (Vérifié par AE)"
        else:
            final_label = prediction_label.upper()
            status = "Anomalie détectée"

        return {
            "prediction": final_label,
            "confidence": round(confidence, 2),
            "reconstruction_error": round(recon_error, 6),
            "status": status,
            "probabilities": {class_names[i]: round(float(cls_preds[0][i] * 100), 2) for i in range(len(class_names))}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Lancement local sur le port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)