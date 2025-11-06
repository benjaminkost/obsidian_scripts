import logging
from pathlib import Path
import os
import re
import shutil

from src.findAllReferences import check_str_in_mytags

def export_notes_with_mytag(path_to_vault, export_path, mytag:str):
    proceed = True

    count_of_file = sum([len(files) for r, d, files in os.walk(path_to_vault)])
    logging.info(f"Count of files in vault: {count_of_file}")

    # Make export directory and asset as subfolder
    Path(export_path).mkdir(parents=True, exist_ok=True)
    Path(f"{export_path}/assets").mkdir(parents=True, exist_ok=True)

    # Search every file with .md extension
    for dirpath, dirname, filenames in os.walk(path_to_vault):
        only_md_filenames = [f for f in filenames if f.endswith(".md")]
        for filename in only_md_filenames:
            path_to_file = f"{dirpath}/{filename}"
            with open(path_to_file, "r") as f:
                file_str = f.read()
                f.close()
            if check_str_in_mytags(file_str, mytag):
                # Copy path
                shutil.copyfile(path_to_file, f"{export_path}/{filename}")

                # Copy assets
                export_obsidian_media(file_str, path_to_vault, f"{export_path}/assets")

                count_of_file = sum([len(files) for r, d, files in os.walk(path_to_vault)])

                # if proceed:
                #    var = input(f"Count of files in vault: {count_of_file}\n\nIs that okay (y/n): ")

                #     if var == "n":
                #        print("\nNothing changed in vault")
                #        exit()

                #    proceed = True


def export_obsidian_media(file_string: str, vault_path: str, export_path: str):
    """
    Findet alle referenzierten Medien-Dateien in einem Obsidian-Markdown-Text
    und kopiert sie aus dem Vault in einen Export-Ordner.
    """
    # Erstelle Export-Verzeichnis falls nicht vorhanden
    os.makedirs(export_path, exist_ok=True)

    # Unterstützte Medien-Typen
    exts = r"(?:png|jpg|jpeg|gif|pdf|svg|webp)"

    pattern = re.compile(
        rf"!?\[\[([^\]|]+\.{exts})(?:\|[^\]]+)?\]\]|!\[.*?\]\(([^)]+\.{exts})\)",
        re.IGNORECASE
    )

    matches = pattern.findall(file_string)
    if not matches:
        print("⚠️ Keine referenzierten Medien gefunden.")
        return

    # Alle Treffer zusammenführen (aus zwei Regex-Gruppen)
    referenced_files = set()
    for m in matches:
        referenced_files.update([f for f in m if f])

    print(f"📂 Gefundene Referenzen: {referenced_files}")

    copied_files = []
    for ref in referenced_files:
        # Normalisiere Pfad
        ref_name = os.path.basename(ref)
        found_path = None

        # Prüfe direkte Existenz
        direct_path = os.path.join(vault_path, ref)
        if os.path.exists(direct_path):
            found_path = direct_path
        else:
            # Durchsuche Vault rekursiv
            for root, _, files in os.walk(vault_path):
                if ref_name in files:
                    found_path = os.path.join(root, ref_name)
                    break

        # Kopieren falls gefunden
        if found_path:
            dest = os.path.join(export_path, ref_name)
            shutil.copy2(found_path, dest)
            copied_files.append(ref_name)
        else:
            print(f"❌ Datei nicht gefunden im Vault: {ref}")

    print(f"✅ {len(copied_files)} Dateien erfolgreich exportiert:")
    for f in copied_files:
        print(f" - {f}")

