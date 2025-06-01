import json
import pyautogui
import time
from rapidfuzz import process
import networkx as nx

from mining import moveToCursorCoords
from config import MAP_KEY, START_JUMP, FTL_JUMPT_TIME

with open("bsgo_ai/sectors_links/secteurs.json", "r") as f:
    sectors = json.load(f)

def shortest_path(start_sector, end_sector):

    G = nx.Graph()

    for sector in sectors:
        src = sector["id"]
        for neighbor in sector["links"]:
            G.add_edge(src, neighbor)

    try:
        path = nx.shortest_path(G, source=start_sector, target=end_sector)
        print("\n[INFO] Shortest route:")
        for sid in path[1:]:
            name = next(s["name"] for s in sectors if s["id"] == sid)
            print(f"{sid}: {name}")
        return path[1:]
    except nx.NetworkXNoPath:
        print("[ERREUR] Aucun chemin disponible entre ces deux secteurs.")
        return []
    except nx.NodeNotFound:
        print("[ERREUR] Secteur invalide fourni.")
        return []

def ocr_check_sector(ocr_result):

    # Charger les secteurs
    with open("secteurs.json", "r") as f:
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

def check_sector(current_sector, target_sector):
    if current_sector != target_sector:
        return False
    else:
        return True

def jump(id_sector):

    sector = next((s for s in sectors if s["id"] == id_sector), None)

    if sector is None:
        print(f"[ERREUR] Secteur ID {id_sector} introuvable.")
        return None

    x, y = sector["x"], sector["y"]

    pyautogui.press(MAP_KEY)
    time.sleep(0.5)
    moveToCursorCoords((x,y), 'left')
    pyautogui.press(START_JUMP)
    pyautogui.press(MAP_KEY)
    print(f"[ACTION] Jumping to {sector['name']}")

    time.sleep(FTL_JUMPT_TIME)
    time.sleep(10)

    return None