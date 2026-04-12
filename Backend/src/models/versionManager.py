# Item 2 — Saves and restores named versions of the tree
import json
import os
from models.loader import buildByTopology

class VersionManager:

    def __init__(self):
        # Dictionary that holds all saved versions in memory
        self.versions = {}
        # If a versions file already exists on disk, load it into memory
        if os.path.exists("versions.json"):
            with open("versions.json", "r", encoding="utf-8") as f:
                self.versions = json.load(f)

    def _persist(self):
        # Write the current versions dictionary to disk
        # Called after every save or delete so changes are not lost
        with open("versions.json", "w", encoding="utf-8") as f:
            json.dump(self.versions, f, indent=4, ensure_ascii=False)

    def save(self, name: str, tree, bst=None):
        # Takes a snapshot of the AVL tree and optionally the BST
        # If a version with that name already exists, it is overwritten
        # Convert both trees to JSON so they can be stored as plain text
        self.versions[name] = {
            "avl_copy": tree.toJSON(tree.root),
            "bst_copy": tree.toJSON(bst.root) if bst and bst.root else None,
            "limite": tree.limite  # Save the depth limit active at this moment
        }
        # Write the updated versions to disk right away
        self._persist()
        print(f"Version '{name}' saved.")

    def restore(self, name: str, tree, bst=None):
        # Loads a saved version back into the tree objects
        # The tree is rebuilt from JSON using topology so structure is preserved
        # Check that the requested version actually exists
        if name not in self.versions:
            print(f"Version '{name}' not found.")
            return

        from models.loader import buildByTopology
        entry = self.versions[name]

        # Rebuild the AVL tree from the saved JSON
        tree.root = buildByTopology(entry["avl_copy"])
        # Restore the depth limit that was active when the version was saved
        tree.limite = entry["limite"]
        # Recalculate critical flags and final prices since depths are now set
        tree.recalculatePrices()

        # Rebuild the BST only if it was saved and a bst object was provided
        if bst and entry.get("bst_copy"):
            bst.root = buildByTopology(entry["bst_copy"])

        print(f"Version '{name}' restored.")

    def list_versions(self):
        # Returns the names of all saved versions as a list
        return list(self.versions.keys())

    def delete_version(self, name: str):
        # Removes a version by name from memory and from disk
        # Check that the version exists before trying to delete it
        if name not in self.versions:
            print(f"Version '{name}' not found.")
            return

        # Remove from memory
        del self.versions[name]
        # Update the file on disk to reflect the deletion
        self._persist()
        print(f"Version '{name}' deleted.")

# End Item 2