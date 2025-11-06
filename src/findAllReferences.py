import logging
import os
import re
from datetime import datetime

def check_str_in_mytags(str_file, tag) -> bool:
    pattern = re.compile(rf"mytags:\s*([\s\S]*)\stags:")

    matches = pattern.findall(str_file)

    for match in matches:
        if tag in match:
            return True

    return False

def check_all_tags_in_str(str_file, list_of_tags):
    for tag in list_of_tags:
        if not check_str_in_mytags(str_file, tag):
            return False

    return True

def find_and_return_reference_section(str_file):
    variable_name_de = "Referenz"
    pattern_de = re.compile(rf"# {variable_name_de}\s*([\s\S]*)")
    matches_de = pattern_de.findall(str_file)

    variable_name_en = "References"
    pattern_en = re.compile(rf"# {variable_name_en}\s*([\s\S]*)")
    matches_en = pattern_en.findall(str_file)

    unwanted_str_list = ["## Verknüpfung\n- \n## Quellen\n- ", "\n## Verknüpfungen\n- \n## Quellen\n- ", "en \n## Verknüpfung\n- \n## Quellen\n- ", "en \n## Verknüpfungen\n- \n## Quellen\n- ", "## Verknüpfung\n- \n## Quellen\n- \n## Übungsaufgaben", "## Links\n## Sources\n## Example Project\n## Command List", "en \n## Links\n## Sources\n## Example Project\n## Command List"]

    if len(matches_de) == 0 and len(matches_en) == 0:
        logging.error(f"No reference section found for str_file: {str_file}")
        return ""
    if len(matches_en) != 0:
        if matches_en[0] in unwanted_str_list:
            return ""
    if len(matches_de) != 0:
        if matches_de[0] in unwanted_str_list:
            return ""
    if len(matches_de) == 0:
        return matches_en[0]
    if len(matches_en) == 0:
        return matches_de[0]
    pass


def get_formatted_datetime():
    now = datetime.now()
    formatted = f"{now.strftime('%d.%m.%Y')} {now.strftime('%H:%M')}"
    return formatted

def create_source_list_and_save_in_file(vault_name: str, folder_path_from_root_of_vault: str, source_list_file_path: str, file_system="iCloud", tagNames=None):
    # resulting string that will be written in obsidian note
    tags_to_obsidian_format = ""
    if tagNames is not None:
        for tag in tagNames:
            tags_to_obsidian_format += f"- \"[[{tag}]]\"\n"
    res_file_start_str = f"---\n\"created date:\": {get_formatted_datetime()}\nmytags:\n{tags_to_obsidian_format}\n- \"[[source list]]\"\ntags:\n- baby\naliases: \n---\n"

    res_file = open(source_list_file_path, "w")
    res_file.write("")
    res_file = open(source_list_file_path, "w")
    res_file.write(res_file_start_str)
    with open(source_list_file_path, "a") as res_file:
        # Find path
        vault_path = ""
        if file_system == "iCloud":
            vault_path = f"/Users/benkostka/Library/Mobile Documents/iCloud~md~obsidian/Documents/{vault_name}/{folder_path_from_root_of_vault}"
        elif file_system == "Mac":
            vault_path = f"/Users/benkostka/Documents/{vault_name}/{folder_path_from_root_of_vault}"
        else:
            logging.error("File system not supported")
            raise Exception("File system not supported")

        # Open folder
        if not os.path.exists(vault_path):
            raise Exception(f"Folder {vault_path} does not exist")

        # walk through directory
        for dirpath, dirname, filenames in os.walk(vault_path):
            only_md_filenames = [f for f in filenames if f.endswith(".md")]
            for filename in only_md_filenames:
                file = open(f"{dirpath}/{filename}", "r")
                str_file = file.read()
                if tagNames is not None:
                    if check_all_tags_in_str(str_file, tagNames):
                        reference_section = find_and_return_reference_section(str_file)
                        if reference_section == "":
                            file_reference_section_content = ""
                        else:
                            file_reference_section_content = f"\n# [[{filename.split(".")[0]}]]\n{reference_section}"
                else:
                    reference_section = find_and_return_reference_section(str_file)
                    if reference_section == "":
                        file_reference_section_content = ""
                    else:
                        file_reference_section_content = f"\n# [[{filename.split(".")[0]}]]\n{reference_section}"

                res_file.write(file_reference_section_content)

                file.close()