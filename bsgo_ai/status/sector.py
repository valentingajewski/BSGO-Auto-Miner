import json
import pyautogui
import time
from termcolor import colored
from rapidfuzz import process
import networkx as nx

from bsgo_ai.pyautogui_lib import moveToCursorCoords
from bsgo_ai.json_loader import sectors
from bsgo_ai.detectors.text_from_image import extract_text
from bsgo_ai.config import MAP_KEY, START_JUMP, FTL_JUMP_TIME, WING_PLAYER_LOCATION_ZONE, WING_WINDOW, PS_MINING

class Sector():

    def shortest_path(self, start_sector, end_sector, sectors):

        G = nx.Graph()

        for sector in sectors:
            src = sector["id"]
            for neighbor in sector["links"]:
                G.add_edge(src, neighbor)

        try:
            path = nx.shortest_path(G, source=start_sector, target=end_sector)
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

    def ocr_check_sector(self, ocr_result):
        sector_names = [s["name"].upper() for s in sectors]
        input_text = " ".join(ocr_result).upper().strip()

        # Supprimer les chiffres (ex: '82 Tenbnd' → 'Tenbnd')
        filtered_text = ''.join(filter(lambda c: not c.isdigit(), input_text)).strip()

        # Essayer une correspondance avec le texte brut
        match = process.extractOne(filtered_text, sector_names, score_cutoff=60)

        if match:
            name_matched = match[0]
            matched_sector = next(s for s in sectors if s["name"].upper() == name_matched)
            return matched_sector["id"]

        print(f"[ERREUR] Aucun secteur reconnu à partir de : '{filtered_text}'")
        return None


    def check_sector(self, current_sector, target_sector):
        if current_sector != target_sector:
            return False
        else:
            return True

    def extract_sector_from_wing(self):
        time.sleep(1)
        pyautogui.press(WING_WINDOW)
        time.sleep(1)
        sector_list = extract_text(WING_PLAYER_LOCATION_ZONE)
        pyautogui.press(WING_WINDOW)
        return sector_list

    def jump_shortest_path(self, sector_list, target_sector_id):
        current_player_sector = self.ocr_check_sector(sector_list)
        sectors_path = self.shortest_path(current_player_sector, target_sector_id, sectors)
        for i in range (0, len(sectors_path)):
            self.jump(sectors_path[i])
        self.extract_sector_from_wing()    
        return PS_MINING

    def jump(self, id_sector):

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
        print(colored(f"[ACTION] Jumping to {sector['name']}", "yellow"))

        time.sleep(FTL_JUMP_TIME)
        time.sleep(10)

        return None