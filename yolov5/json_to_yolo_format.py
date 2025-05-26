import os
import json
from PIL import Image

# Dossiers
json_dir = 'data/labels/train'
output_dir = 'data/labels_yolo/train'
image_dir = 'data/images/train'

# Créer le dossier de sortie s’il n’existe pas
os.makedirs(output_dir, exist_ok=True)

# Boucle sur chaque fichier JSON
for json_file in os.listdir(json_dir):
    if not json_file.endswith(".json"):
        continue

    base_name = os.path.splitext(json_file)[0]
    image_path = None
    possible_exts = ['.jpg', '.jpeg', '.png']

    # Recherche de l’image correspondante
    for ext in possible_exts:
        test_path = os.path.join(image_dir, base_name + ext)
        if os.path.exists(test_path):
            image_path = test_path
            break

    if image_path is None:
        print(f"Image non trouvée pour {json_file}")
        continue

    # Chargement image pour récupérer largeur et hauteur
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Chargement du JSON
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Conversion en format YOLO
    lines = []
    for pred in data.get("predictions", []):
        class_id = pred["class_id"]
        x_center = pred["x"] / img_width
        y_center = pred["y"] / img_height
        width = pred["width"] / img_width
        height = pred["height"] / img_height

        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # Écriture du fichier .txt au format YOLO
    output_path = os.path.join(output_dir, base_name + ".txt")
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))

    print(f"[OK] Converti {json_file} → {output_path}")
