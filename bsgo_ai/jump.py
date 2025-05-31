import json
import pyautogui
import time
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

def main(start_sector):
    id_sector_list = shortest_path(start_sector,end_sector)
    for id_sector in id_sector_list:
        jump(id_sector)

#if __name__ == "__main__":
    