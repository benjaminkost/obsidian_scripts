import time
import datetime
from pathlib import Path
import re

def delete_metadata_in_string(file_str) -> str:
    regex_for_metadata = r"^---.*---$"
    file_str = re.sub(regex_for_metadata, "", file_str, 1)

    return file_str

def check_if_string_contains_headlines(file_str:str) -> None:
    regex_for_headline = r"^#+\s"
    highest_headline_markers = re.search(regex_for_headline, file_str, re.MULTILINE)
    if not highest_headline_markers:
        raise Exception("There has to be headlines in the document to separate it in atomic notes!")

def create_upper_part_of_template(generic_template_start:str, mytags_list:list[str], aliases: list[str]=None) -> str:
    """
    Creates the upper part of a template by adding the mytags to the "mytags" section

    :param aliases:
    :param generic_template_start: Upper part of the template
    :param mytags_list: List of mytags
    :return: String for the defined upper part of the template
    """
    # timestamp
    regex_for_created_section = r"\n\"created date:\": .*\n"
    current_time = time.time()
    timestamp = datetime.datetime.fromtimestamp(current_time).strftime("%d.%m.%Y %H:%M")

    final_template = re.sub(regex_for_created_section, f"\n\"created date:\": {timestamp}\n", generic_template_start, 1)

    # Mytags
    regex_for_mytags_section = r"mytags:\n(.*?)(?=^\w+:|\Z)"
    match_existing_mytags_section = re.search(regex_for_mytags_section, final_template,re.MULTILINE | re.DOTALL)
    exisiting_tags = match_existing_mytags_section.groups()[0]

    str_of_mytags = "".join(f"  - \"[[{tag}]]\"\n" for tag in mytags_list)

    replacement_string = f"\nmytags:\n"+exisiting_tags+str_of_mytags
    final_template = re.sub(regex_for_mytags_section, replacement_string,final_template,1,re.MULTILINE | re.DOTALL)
    # Aliases
    if aliases:
        regex_for_aliase = r"\naliases:\n"
        str_of_mytags = "".join(f"  - {alias}\n" for alias in aliases)
        final_template = re.sub(regex_for_aliase, "\naliases:\n"+str_of_mytags, final_template)

    return final_template

def add_alias_to_list_of_mytags(mytags_list:list[str]) -> list[str]:
    prefix = r"(\d{12}) (.+)"
    print(mytags_list)
    new_mytags_list = []
    for mytag in mytags_list:
        if "|" in mytag:
            new_mytags_list.append(mytag)
            continue

        match = re.match(prefix, mytag)
        if match:
            _, title = match.groups()
            new_mytags_list.append(f"{mytag}|{title}")
        else:
            new_mytags_list.append(mytag)
    return new_mytags_list

def create_notes_from_big_note(abs_path_to_vault: Path, relative_path_to_file: Path, template_start:str, template_end:str,existing_tags=None) -> None:
    """
    Creates multiple notes from long note with multiple headings
    AND it takes the metadata from that note and applies it on each created note

    -> The new notes are found by a line containing "#" ending with new line with "#" and get the name of the first line that contains a "#"

    :param: abs_path_to_vault: absolute path to the obsidian vault
    :param: relative_path_to_file: relative path (to abs_path_to_vault) to file with the long text
    :param: existing_tags: "Mytags" that all atomic notes will share
    :param: template_start: Metadata that all atomic notes will share with placeholder for "existing_tags" signed as "mytags:"
    :param: template_end: Suffix that all Notes will share
    :return: creates multiple notes in the root directory of the vault
    """

    # Open File containing the long text
    abs_path_to_file = abs_path_to_vault / relative_path_to_file
    file_str:str = open(abs_path_to_file, "r").read()

    # Cut away metadata if it exists
    file_str = delete_metadata_in_string(file_str)

    # Check if it contains headlines
    check_if_string_contains_headlines(file_str)

    # Loop to create atomic notes
    lines = file_str.split("\n")
    regex_for_headline_title = r"^(#+)\s+(.*)"
    current_path = {}
    active_file_path = None
    for line in lines:
        # check if it is a headline
        match = re.match(regex_for_headline_title, line)
        if match:
            if active_file_path:
                with open(active_file_path, "a") as f:
                    f.write(f"\n{template_end}")

            # Get level of headline and title
            hashes, title = match.groups()
            current_level = len(hashes)

            if title == "Referenz":
                exit()

            # Set current path
            current_time = time.time()
            timestamp = datetime.datetime.fromtimestamp(current_time).strftime("%Y%m%d%H%M")
            no_structure_numbers_titles = re.sub(r"(\d.?)+\s", "", title)
            safe_title = re.sub(r"[\\/:|]", "", no_structure_numbers_titles)
            current_file_name = f"{timestamp} {safe_title}"
            current_path[current_level] = current_file_name

            # Delete all level beneath current lowest level
            keys_to_remove = [k for k in current_path if k > current_level]
            for k in keys_to_remove:
                del current_path[k]

            # Create empty text with template
            parent_titles = [current_path[k] for k in sorted(current_path.keys()) if k < current_level]
            existing_tags_with_aliases = add_alias_to_list_of_mytags(existing_tags or [])
            parent_titles_with_aliases = add_alias_to_list_of_mytags(parent_titles)
            combined_mytags_list = existing_tags_with_aliases + parent_titles_with_aliases
            atomic_note_template_start = create_upper_part_of_template(template_start, combined_mytags_list, [safe_title])
            atomic_note_text = atomic_note_template_start

            # write Atomic Note
            active_file_path = f"{abs_path_to_vault}/{current_file_name}.md"
            with open(active_file_path, "w") as f:
                f.write(atomic_note_text)

        elif current_path: # checks if there is at least one headline found in document
            with open(active_file_path, "a") as f:
                f.write(f"{line}\n")