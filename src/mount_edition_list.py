import os
import re
import json

from constants import OLOP_BASE_URL


def extract_json_from_html(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"Error: HTML file not found at '{html_path}'")
        return None

    # Improved regular expression to handle whitespace and line breaks
    match = re.search(r"let\s+jsonEditions\s*=\s*({.*?});", html, re.DOTALL)

    if match:
        json_string = match.group(1)
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            print("Error: jsonEditions content is not valid JSON.")
            return None
    else:
        print("Error: jsonEditions variable not found in HTML.")
        return None


if __name__ == "__main__":
    file_path = "../htmls/Edições_de_One_Piece_LigaOnePiece.html"
    json_editions = extract_json_from_html(file_path)
    print("JSON extracted successfully.")
    # if json_editions:
    #     os.makedirs("../data", exist_ok=True)
    #     with open("../data/editions.json", "w") as f:
    #         json.dump(json_editions, f, indent=4)

    edition_example = {
        "name": "Starter Deck 15: RED Edward.Newgate",
        "code": "SD15",
        "deck_link": "https://www.ligaonepiece.com.br/?view=cards/search&card=edid=15%20ed=SD15",
    }

    json_example = {
        "id": "45",
        "acronym": "ST20",
        "name": "Starter Deck 20: YELLOW Charlotte Katakuri",
        "nameen": "Starter Deck 20: YELLOW Charlotte Katakuri",
        "namept": "",
        "nameptsa": "",
        "dtrelease": "2024-10-25",
        "idgrouped": "0",
        "icon": "",
    }

    editions = []
    for data in json_editions["main"]:
        editions.append(
            {
                "name": data["nameen"],
                "code": data["acronym"],
                "deck_link": f"{OLOP_BASE_URL}/?view=cards/search&card=edid={data['id']}%20ed={data['acronym']}",
            }
        )

    os.makedirs("../data", exist_ok=True)
    with open("../data/cleaned_editions.json", "w") as f:
        json.dump(editions, f, indent=4)

    print("Editions cleaned successfully.")

    path_list_example = [
        {
            "name": "Starter Deck 15: RED Edward.Newgate",
            "path_dir": "../htmls/ST15_Starter_Deck_15_RED_Edward_Newgate",
        }
    ]

    path_list = []

    for edition in editions:
        path_list.append(
            {
                "name": edition["name"],
                "deck_link": edition["deck_link"],
                "path_dir": (
                    f"htmls/{edition['code']}_{edition['name'].replace(' ', '_').replace(':', '_').replace('.', '_')}.html"
                ),
            }
        )

    os.makedirs("../data", exist_ok=True)
    with open("../data/path_list.json", "w") as f:
        json.dump(path_list, f, indent=4)

    print("Path list created successfully.")

    # for path in path_list:
    #     download_editions(path["deck_link"], path["path_dir"])
    #     print(f"Downloaded {path['name']} at {path['path_dir']}")
