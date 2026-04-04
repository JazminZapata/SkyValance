# Item 2 — Saves and restores named versions of the tree
import json
import os
from models.loader import buildByTopology

class VersionManager:

    def __init__(self):
        self.versions = {}
        # Load versions from disk if the file already exists
        if os.path.exists("versions.json"):
            with open("versions.json", "r", encoding="utf-8") as f:
                self.versions = json.load(f)

    def _persist(self):
        # Write the versions dictionary to disk
        with open("versions.json", "w", encoding="utf-8") as f:
            json.dump(self.versions, f, indent=4, ensure_ascii=False)

    def save(self, name: str, tree, bst=None):
        # Save current AVL and BST state under the given name
        self.versions[name] = {
            "avl_copy": tree.toJSON(tree.root),
            "bst_copy": tree.toJSON(bst.root) if bst and bst.root else None,
            "limite": tree.limite
        }
        self._persist()
        print(f"Version '{name}' saved.")

    def restore(self, name: str, tree, bst=None):
        if name not in self.versions:
            print(f"Version '{name}' not found.")
            return
        from models.loader import buildByTopology
        entry = self.versions[name]
        # Restore AVL
        tree.root = buildByTopology(entry["avl_copy"])
        tree.limite = entry["limite"]
        tree.recalculatePrices()
        # Restore BST if it was saved
        if bst and entry.get("bst_copy"):
            bst.root = buildByTopology(entry["bst_copy"])
        print(f"Version '{name}' restored.")

    def list_versions(self):
        # Returns list of version names
        return list(self.versions.keys())

    def delete_version(self, name: str):
        if name not in self.versions:
            print(f"Version '{name}' not found.")
            return
        del self.versions[name]
        self._persist()
        print(f"Version '{name}' deleted.")

# End Item 2