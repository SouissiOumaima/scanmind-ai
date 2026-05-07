🧠 Brain Tumor Detection & Anomaly Diagnosis API
📝 Présentation du Projet
Ce projet, développé dans le cadre de ma spécialisation en Data Science et Intelligence Artificielle, propose une solution de diagnostic médical assisté par ordinateur. L'objectif est de détecter et de classifier les tumeurs cérébrales à partir d'images IRM (MRI) tout en identifiant les cas atypiques grâce à une approche hybride.

🚀 Architecture Technique
Le système repose sur deux modèles de Deep Learning complémentaires travaillant en parallèle :

Classifieur CNN (EfficientNet/Custom) : Entraîné pour identifier quatre catégories spécifiques : glioma, meningioma, notumor, et pituitary.

Autoencodeur (Détection d'Anomalies) : Analyse la fidélité de l'image en calculant une erreur de reconstruction. Une erreur élevée signale une anomalie structurelle que le classifieur pourrait avoir manqué.

📂 Organisation des Données & Entraînement
Le modèle suit un ordre alphabétique strict pour les classes, garantissant la fiabilité des prédictions :

Index 0 : Glioma

Index 1 : Meningioma

Index 2 : Notumor (Sain)

Index 3 : Pituitary

📊 Performances
La précision du système est validée par une Matrice de Confusion montrant une excellente séparation entre les tissus sains et les différentes pathologies, avec une robustesse particulière sur la classe "Notumor".

Les tests finaux sur l'ensemble de validation montrent une robustesse exceptionnelle du système :

Précision Moyenne : > 95% sur les 4 classes.

Fiabilité du Diagnostic : Le score de confiance élevé (> 95%) réduit drastiquement les risques de faux diagnostics.

Stabilité : L'erreur de reconstruction reste stable (autour de 0.002), confirmant que le modèle ne sur-réagit pas au bruit visuel des IRM.