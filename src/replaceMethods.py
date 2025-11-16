import os
from datetime import datetime
from src.findAllReferences import check_str_in_mytags
from src.addMethods import add_string_to_tags

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

def replace_mytag_with_tag(abs_vault_path: str, mytag: str, tag_name=None) -> None:
    """
    Is changing every Note that contains the mytag given so that the mytag in the Obsidian custom metadata field "mytag"
    in to a normal tag in the Obsidian metadata field "tags"

    :param mytag: Is a custom Obsidian metadta field
    :param abs_vault_path: Absolute path to obsidian vault
    """
    count_notes_changed = 0

    # Go through all folders of vault
    for dirpath, dirnames, filenames in os.walk(abs_vault_path):
        proceed = False

        for filename in [f for f in filenames if f.endswith(".md")]:
            abs_file_path = f"{dirpath}/{filename}"
            with open(abs_file_path, "r") as f:
                file_str = f.read()
            if check_str_in_mytags(file_str, mytag):
                # Split file into a list
                list_file_str = file_str.split("\n")

                # Delete line containing mytag string
                for index, line in enumerate(list_file_str):
                    if mytag in line:
                        list_file_str.remove(line)
                        break

                new_file_str = "".join(line + "\n" for line in list_file_str)

                # Add string mytag to tags field
                if tag_name is None:
                    final_file_str = add_string_to_tags(file_str=new_file_str,tag=mytag)
                else:
                    final_file_str = add_string_to_tags(file_str=new_file_str, tag=tag_name)

                var = ""
                if not proceed:
                    print(abs_file_path)
                    var = input(
                        "This is how it looks if the template is added:\n" + final_file_str + "\n\nIs that okay (y/n): ")

                    if var == "n":
                        print("\nNothing changed in vault")
                        exit()

                if var == "y" or proceed:
                    with open(abs_file_path, "w") as file:
                        file.write(final_file_str)
                        print(f"This text is written in file: \n{final_file_str}")

                        count_notes_changed+=1

                    proceed = True

    print(f"Notes changed: {count_notes_changed}")

def replace_list_of_mytags(abs_vault_path:str, list_of_mytags:list) -> None:
    for mytag in list_of_mytags:
        replace_mytag_with_tag(abs_vault_path,mytag)