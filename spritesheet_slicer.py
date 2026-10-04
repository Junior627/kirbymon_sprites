import os
import re
from PIL import Image

def process_name_list(name_list_path: str) -> list:
    formatted_names = []
    if not os.path.exists(name_list_path):
        print(f"Error: Could not find {name_list_path}")
        return formatted_names
    with open(name_list_path, "r", encoding="utf-8") as file:
        for line in file:
            name = line.strip()

            cleaned_name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
            words = cleaned_name.split()
            proper_case_no_spaces = "".join(word.capitalize() for word in words)

            if proper_case_no_spaces:
                formatted_names.append(proper_case_no_spaces)

    return formatted_names

def slice_sheet(
    sheet_path: str, tile_width: int, tile_height: int, names:list, output_dir: str      
):
    os.makedirs(output_dir, exist_ok=True)

    sheet = Image.open(sheet_path)
    sheet_width, sheet_height = sheet.size

    cols = sheet_width // tile_width
    rows = sheet_height // tile_height

    total_tiles = cols * rows

    if len(names) != total_tiles:
        print(f"Warning: The number of names provided ({len(names)}) does not match the total number of tiles ({total_tiles}).")

    for index, name in enumerate(names):
        if(index) >= total_tiles:
            break

        col = index % cols
        row = index // cols

        left = col * tile_width
        upper = row * tile_height
        right = left + tile_width
        lower = upper + tile_height

        tile = sheet.crop((left, upper, right, lower))
        file_path = os.path.join(output_dir, f"{name}.png")
        tile.save(file_path)

        print(f"Saved tile {index + 1}/{total_tiles} as {file_path}")


if __name__ == "__main__":
    SPRITE_SHETT_FILE = "allies.png"
    NAME_LIST_FILE = "names.txt"
    TILE_WIDTH = 640
    TILE_HEIGHT = 640

    SPRITE_NAMES = process_name_list(NAME_LIST_FILE)

    if SPRITE_NAMES:
        slice_sheet(SPRITE_SHETT_FILE, TILE_WIDTH, TILE_HEIGHT, SPRITE_NAMES, "output")