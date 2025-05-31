import json
import networkx as nx

# Charger les secteurs avec leurs connexions
with open("bsgo_ai/sectors_links/secteurs.json", "r") as f:
    sectors = json.load(f)

def test(start, end):
    # Créer un graphe non orienté
    G = nx.Graph()

    # Ajouter les arêtes
    for sector in sectors:
        src = sector["id"]
        for neighbor in sector["links"]:
            G.add_edge(src, neighbor)

    # Demander les points de départ et d'arrivée
    #start = int(input("\nEntrez l'ID du secteur de départ : "))
    #end = int(input("Entrez l'ID du secteur d'arrivée : "))

    # Trouver le chemin le plus court
    try:
        path = nx.shortest_path(G, source=start, target=end)
        print("\nChemin le plus court :")
        for sid in path:
            name = next(s["name"] for s in sectors if s["id"] == sid)
            print(f"{sid}: {name}")
    except nx.NetworkXNoPath:
        print("Aucun chemin disponible entre ces deux secteurs.")
    except nx.NodeNotFound:
        print("Secteur invalide fourni.")

if __name__ == "__main__":
    test(4,10)
