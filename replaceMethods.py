import os
from datetime import datetime


def replace_latex_delimiter(abs_path):
    with open(abs_path, "r") as f:
        note = f.read()

    note = note.replace("\[", "$$")
    note = note.replace("\]", "$$")
    note = note.replace("\( ", "$")
    note = note.replace(" \)", "$")

    with open(abs_path, "w") as f:
            f.write(note)

def get_formatted_datetime():
    now = datetime.now()
    formatted = f"{now.strftime('%d.%m.%Y')} {now.strftime('%H:%M')}"
    return formatted

def replace_strings(abs_path_folder, str_to_replace, str_replacement):
    list_files_in_dir = []

    # Added all files in dir in list
    for dirpath, dirnames, filenames in os.walk(abs_path_folder):
        for filename in [f for f in filenames if f.endswith(".md")]:
            list_files_in_dir.append(os.path.join(dirpath, filename))

        # Change all files in list
    for path_for_file in list_files_in_dir:
        file = open(path_for_file, "r")
        str_file = file.read()

        str_file = str_file.replace(str_to_replace, str_replacement)

        if path_for_file == list_files_in_dir[0]:
            var = input("This is how it looks if the template is added:\n"+str_file+"\n\nIs that okay (y/n): ")

            if var == "n":
                print("\nNothing changed in vault")
                exit()

        file = open(path_for_file, "w")
        file.write(str_file)

    print("\nAll files in Directory changed as requested!")

# Ausführung
abs_path_folder = "/Users/benkostka/Library/Mobile Documents/iCloud~md~obsidian/Documents/Academia_and_Work/Experiment - Messung der Lichtgeschwindigkeit nach der Drehspiegelmethode von Fizeau-Foucault.md"

replace_latex_delimiter(abs_path_folder)