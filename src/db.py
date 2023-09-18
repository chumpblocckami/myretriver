import time

import chromadb
import requests
from tqdm import tqdm

from .utils import hf_embedding_functions


class Embedder():
    def __init__(self, query="f:pauper"):
        self.query = query
        self.url = "https://api.scryfall.com/cards/search?q="
        self.embedding_function = hf_embedding_functions
        self.client = chromadb.PersistentClient(
            path="./cards",
        )
        self.data = []
        self.documents = []

    def get_cards(self):
        has_more = True
        page = 1
        url = self.url + self.query
        while has_more:
            response = requests.get(url)
            has_more = response.json()["has_more"]
            url = response.json()["next_page"] if "next_page" in response.json() else ""
            remaining_pages = int(response.json()["total_cards"] / 175)
            for card in tqdm(response.json()["data"], desc=f"Page {page}/{remaining_pages + 1}"):
                # skipping double sided, transform and other strange cards
                if "oracle_text" in card:
                    self.data.append(card)
                else:
                    print(card["name"])
            page = page + 1
        time.sleep(1)

    def generate_vectorstore(self):
        self.documents = [(d["oracle_text"].replace("{", "").replace("}", "").replace("\n", ""),
                           {"name": d["name"],
                            "cmc": int(d["cmc"]),
                            "price": float(d["prices"]["eur"]) if d["prices"]["eur"] else 0.0,
                            "type": d["type_line"].split("—")[0].strip(),
                            "subtype": d["type_line"].split("—")[1].strip() if len(d["type_line"].split("—")) > 1 else "",
                            "img": d["image_uris"]["art_crop"] if "image_uris" in d else None}) for d in self.data]

    def save(self):
        if "cards" not in [x.name for x in self.client.list_collections()]:
            self.client.create_collection(name="cards",
                                          embedding_function=self.embedding_function)
        collection = self.client.get_collection("cards")
        collection.add(documents=[x[0] for x in self.documents],
                       metadatas=[x[1] for x in self.documents],
                       ids=[f"{x}" for x in range(len(self.documents))])

    def generate_dataset(self):
        self.get_cards()
        self.generate_vectorstore()
        self.save()
