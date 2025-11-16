import os
import shutil
from datetime import datetime

def get_formatted_datetime():
    now = datetime.now()
    formatted = f"{now.strftime('%d.%m.%Y')} {now.strftime('%H:%M')}"
    return formatted

def add_template_to_multable_notes(abs_path_folder, template_str_before, template_str_after):
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