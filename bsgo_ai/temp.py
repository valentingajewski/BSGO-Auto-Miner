import json
import networkx as nx
from rapidfuzz import process
from detectors.text_from_image import extract_text
from config import SECTOR_TEXT_POSITION

# Charger les secteurs avec leurs connexions
with open("bsgo_ai/sectors_links/secteurs.json", "r") as f:
    sectors = json.load(f)

def check_sector(ocr_result):

    # Charger les secteurs
    with open("bsgo_ai/sectors_links/secteurs.json", "r") as f:
        sectors = json.load(f)

    sector_names = [s["name"].upper() for s in sectors]

    # Fusionner texte OCR en une seule string
    input_text = " ".join(ocr_result).upper().strip()

    # Trouver la meilleure correspondance
    match = process.extractOne(input_text, sector_names, score_cutoff=75)
    
    if match:
        name_matched = match[0]
        matched_sector = next(s for s in sectors if s["name"].upper() == name_matched)
        return matched_sector["id"]
    
    print("[ERREUR] Aucun secteur reconnu.")
    return None

if __name__ == "__main__":
    sector = extract_text(SECTOR_TEXT_POSITION)
    print(check_sector(sector))
