import os
import re
import shutil
from datetime import datetime
from pathlib import Path


def get_formatted_datetime():
    now = datetime.now()
    formatted = f"{now.strftime('%d.%m.%Y')} {now.strftime('%H:%M')}"
    return formatted

def add_template_to_multiple_notes(abs_path_folder, template_str_before, template_str_after):
    list_files_in_dir = []

    # Added all files in dir in list
    for dirpath, dirnames, filenames in os.walk(abs_path_folder):
        for filename in [f for f in filenames if f.endswith(".md")]:
            list_files_in_dir.append(os.path.join(dirpath, filename))

    print(f"Files found in Directory: {len(list_files_in_dir)}")

    # Change all files in list
    for path_for_file in list_files_in_dir:
        file = open(path_for_file, "r")
        str_file = file.read()

        str_file = template_str_before+str_file+template_str_after

        if path_for_file == list_files_in_dir[0]:
            var = input("This is how it looks if the template is added:\n"+str_file+"\n\nIs that okay (y/n): ")
            if var == "n":
                print("\nNothing changed in vault")
                exit()

        file = open(path_for_file, "w")
        file.write(str_file)

    print("\nAll files in Directory changed as requested!")

def move_all_files(src_dir: str, dest_dir: str):
    # Zielordner erstellen, falls nicht vorhanden
    os.makedirs(dest_dir, exist_ok=True)

    # Alle Dateien und Unterordner durchsuchen
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            # Falls eine Datei mit gleichem Namen schon existiert → umbenennen
            if os.path.exists(dest_file):
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_file):
                    dest_file = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                    counter += 1

            shutil.move(src_file, dest_file)
            print(f"Verschoben: {src_file} → {dest_file}")

def add_string_to_tags(file_str: str, tag: str) -> str:
    """
    Add a string as a tag to a note (as a string)

    :param file_str: complete text of a note
    :param tag: str that should be added to note
    :return: string of file with tag in tags section
    """

    identifier_of_tags_section = "\ntags:"
    index_of_tags_section = file_str.find(identifier_of_tags_section)

    if index_of_tags_section == -1:
        # Create tag section in the beginning of metadata section
        identifier_of_metadata_section_begin = "---"
        index_of_metadata_section_begin = file_str.find(identifier_of_metadata_section_begin)
        tags_metadata_paragraph = "tags:"
        str_file = file_str[:(index_of_metadata_section_begin + len(identifier_of_metadata_section_begin))] + f"\n{tags_metadata_paragraph}\n  - {tag}" + file_str[(index_of_metadata_section_begin + len(index_of_metadata_section_begin)):]
    else:
        str_file = file_str[:(index_of_tags_section + len(identifier_of_tags_section))] + f"\n  - {tag}" + file_str[(index_of_tags_section + len(identifier_of_tags_section)):]

    return str_file


def add_dir_names_as_mytags_to_metadata(abs_path_folder):
    """

    :param abs_path_folder: Path to directory to add metadata
    :return:
    """
    # Number of directories above the abs_path_folder
    number_of_sub_dir = len(abs_path_folder.split("/")) ##actually there is one element more but does not matter for the code

    # Initalize list which should contain all file paths needed
    list_files_in_dir = []

        # Added all files in dir in list
    for dirpath, dirnames, filenames in os.walk(abs_path_folder):
        for filename in [f for f in filenames if f.endswith(".md")]:
            list_files_in_dir.append(os.path.join(dirpath, filename))

    print(f"Files found in Directory: {len(list_files_in_dir)}")

    # Change all files in list
    for path_for_file in list_files_in_dir:
        list_skipped_notes = 0

        file = open(path_for_file, "r")
        str_file = file.read()

        for sub_dir in path_for_file.split("/")[(number_of_sub_dir-1):-1]:
            metadata_index = str_file.find("mytags:")
            str_file = str_file[:(metadata_index+7)] + f"\n  - \"[[{sub_dir}]]\""+str_file[(metadata_index+7):]

            if metadata_index != -1:
                if path_for_file == list_files_in_dir[0]:
                    var = input("This is how it looks if the template is added:\n"+str_file+"\n\nIs that okay (y/n): ")
                    if var == "n":
                        print("\nNothing changed in vault")
                        exit()

                file = open(path_for_file, "w")
                file.write(str_file)
            else:
                list_skipped_notes+=1

    print(f"{list_skipped_notes} Notes did not have \"mytags\" in the metadata !?")
    print("\nAll files in Directory changed as requested!")

def get_mytags_section(file_str: str) -> str | None:
    """Hilfsfunktion, um den Inhalt der mytags-Sektion zu extrahieren."""
    # Regex sucht nach 'mytags:', gefolgt von Inhalt, bis zum nächsten Key (Zeilenanfang mit Wort:) oder Dateiende.
    regex = r"^mytags:\s*\n(.*?)(?=^\w+:|\Z)"
    match = re.search(regex, file_str, re.MULTILINE | re.DOTALL)

    if match:
        return match.group(1)
    return None

def mytags_exists(file_str:str, list_of_existing_mytags: list[str]) -> bool:
    mytags_section = get_mytags_section(file_str)
    if mytags_section is None:
        return False

    # add mytag to list_of_existing_mytags
    for mytag in list_of_existing_mytags:
        if f"[[{mytag}]]" not in mytags_section:
            return False

    return True

def mytag_exists(file_str:str, mytag:str) -> bool:
    mytags_section = get_mytags_section(file_str)
    if mytags_section is None:
        return False

    # add mytag to list_of_existing_mytags
    if f"[[{mytag}]]" not in mytags_section:
        return False

    return True

def add_mytag_to_file_str(file_str:str, mytag:str) -> str:
    """
    Adds a mytag to the mytags section of a file string

    :param file_str:
    :param mytag:
    :return: file string with added mytag
    """
    regex_for_mytags_section = r"(^mytags:\s*\n)(.*?)(?=^\w+:|\Z)"
    match_existing_mytags_section = re.search(regex_for_mytags_section, file_str,re.MULTILINE | re.DOTALL)

    header = match_existing_mytags_section.group(1)
    content = match_existing_mytags_section.group(2)

    str_of_mytag = f"  - \"[[{mytag}]]\"\n"

    if content and not content.endswith('\n'):
        content += '\n'

    replacement_string = header + content + str_of_mytag
    new_file_str = re.sub(regex_for_mytags_section, replacement_string,file_str,1,re.MULTILINE | re.DOTALL)

    return new_file_str

def add_mytag_if_not_exists(vault_path:Path, mytag:str, list_of_existing_mytags: list[str]) -> None:
    proceed = False
    count_notes_changed = 0

    # walk from markdown files
    for dirpath, dirnames, filenames in os.walk(vault_path):
        for filename in [f for f in filenames if f.endswith(".md")]:
            abs_file_path = f"{dirpath}/{filename}"
            with open(abs_file_path, "r") as f:
                file_str = f.read()
            if mytags_exists(file_str, list_of_existing_mytags) and not mytag_exists(file_str, mytag):
                final_file_str = add_mytag_to_file_str(file_str, mytag)

                if not proceed:
                    print(abs_file_path)
                    var = input(
                        f"This is how it looks if the template is added for \"{filename}\":\n" + final_file_str + "\n\nIs that okay (y/n/all): ").lower()

                    if var == "n":
                        print("Termination from user")
                        return
                    elif var == "all":
                        proceed = True
                    elif var != "y":
                        # Wenn weder y noch all noch n, überspringen wir diese Datei
                        continue

                # Schreiben
                with open(abs_file_path, "w") as file:
                            file.write(final_file_str)
                            count_notes_changed += 1
                            if proceed:
                                print(f"Tag hinzugefügt in: {filename}")
                            else:
                                print("Datei gespeichert.")

    print(f"\nFertig. {count_notes_changed} Dateien wurden geändert.")