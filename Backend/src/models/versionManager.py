import json
import os
from datetime import datetime

class VersionManager:
# Manages saving and restoring named versions of the tree's state. Item #2
    # versions_dir: directory where version files and the index will be stored
    def __init__(self, versions_dir="versions"):
        self.versions_dir = versions_dir
        self.index_file = os.path.join(versions_dir, "index.json")
        # In-memory index: name -> {filename, timestamp, limite}
        self._index = {}
        self._ensure_dir()
        self._load_index()

    # Creates the versions directory if it does not exist yet
    def _ensure_dir(self):
        os.makedirs(self.versions_dir, exist_ok=True)

    # Loads the index from disk so versions persist across program restarts
    def _load_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r", encoding="utf-8") as f:
                self._index = json.load(f)

    # Writes the current in-memory index back to disk
    def _save_index(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self._index, f, indent=4, ensure_ascii=False)

    # Saves the current state of the tree as a named version.
    # If a version with that name already exists, it is overwritten.
    def save(self, name: str, tree) -> bool:
        if tree.root is None:
            print("The tree is empty, cannot save version.")
            return False

        # Build a safe filename (no spaces or special characters)
        safe_name = name.strip().replace(" ", "_").replace("/", "-").replace("\\", "-")
        filename = f"{safe_name}.json"
        filepath = os.path.join(self.versions_dir, filename)

        # Serialize the tree using the toJSON method already defined in Tree
        data = tree.toJSON(tree.root)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Register entry in the index with name, file, timestamp and depth limit
        self._index[name] = {
            "filename": filename,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "limite": tree.limite,
        }
        self._save_index()

        print(f"Version '{name}' saved successfully.")
        return True

    # Restores the tree to the state of the given named version.
    # Rebuilds the exact topology using buildByTopology() from loader.
    def restore(self, name: str, tree) -> bool:
        if name not in self._index:
            print(f"Version '{name}' not found.")
            return False

        entry = self._index[name]
        filepath = os.path.join(self.versions_dir, entry["filename"])

        if not os.path.exists(filepath):
            print(f"Version file not found: {filepath}")
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # buildByTopology reconstructs the tree node by node preserving its structure
        try:
            from loader import buildByTopology
        except ImportError:
            from .loader import buildByTopology

        tree.root = buildByTopology(data)
        tree.limite = entry.get("limite", 3)
        # Recalculate prices and critical flags using the restored depth limit
        tree.recalculatePrices()

        print(f"Version '{name}' restored successfully.")
        return True

    # Returns the list of saved versions with their metadata
    def list_versions(self) -> list:
        if not self._index:
            return []

        result = []
        for name, entry in self._index.items():
            result.append({
                "name": name,
                "timestamp": entry["timestamp"],
                "limite": entry.get("limite", 3),
            })
        return result

    # Removes a version from the index and deletes its associated JSON file
    def delete_version(self, name: str) -> bool:
        if name not in self._index:
            print(f"Version '{name}' not found.")
            return False

        filepath = os.path.join(self.versions_dir, self._index[name]["filename"])
        if os.path.exists(filepath):
            os.remove(filepath)

        del self._index[name]
        self._save_index()

        print(f"Version '{name}' deleted.")
        return True

# End Item 2.
