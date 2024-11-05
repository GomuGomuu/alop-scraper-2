import json
import os
from bs4 import BeautifulSoup


def get_card_data(html_path=None, html_file=None):
    if not html_path and not html_file:
        raise ValueError(
            "You must provide either the HTML content or the HTML file path"
        )

    if html_path:
        with open(html_path, "r", encoding="utf-8") as f:
            html_file = f.read()

    soup = BeautifulSoup(html_file, "html.parser")

    # Wait for the div with class 'card-grid' to be present
    card_items = soup.select(".card-item")
    card_data = []

    for item in card_items:
        try:
            card = {}

            # Name
            name_element = item.select_one(".invisible-label")
            if name_element:
                # Extract full text, e.g., "Bepo (One Piece Film Red) (P-019-FR)" or "Bepo (P-020-FR)"
                full_text = name_element.text.strip()

                # Check if there are multiple sets of parentheses
                if full_text.count("(") > 1:
                    # Extract the name (everything before the last set of parentheses)
                    card["name"] = full_text.rsplit("(", 2)[0].strip()
                else:
                    # If only one set of parentheses, take everything before it as the name
                    card["name"] = full_text.split("(")[0].strip()

                # Extract the slug (content inside the last parentheses)
                card["slug"] = full_text.split("(")[-1].replace(")", "").strip()

            # Illustration image URL
            img_url_element = item.select_one(".main-link-card img")
            if img_url_element:
                card["illustration_img_url"] = "https:{}".format(
                    img_url_element.get("data-src", "")
                )

            # Price
            price_element = item.select_one(".avgp-minprc")
            if price_element:
                price_str = (
                    price_element.text.replace("R$", "").replace(",", ".").strip()
                )
                if price_str.count(".") > 1:
                    parts = price_str.split(".")
                    price_str = "".join(parts[:-1]) + "." + parts[-1]
                card["price"] = float(price_str) if price_str else 0.0

            card_data.append(card)
        except Exception as inner_e:
            print(f"Error extracting data from a card: {inner_e}")

    return card_data if card_data else None


if __name__ == "__main__":
    # Example usage with HTML file
    with open("../htmls/OP-03_Pillars_of_Strength.html", "r", encoding="utf-8") as f:
        html = f.read()
    cards = get_card_data(html)

    # Save data
    os.makedirs("../data", exist_ok=True)

    # If exists, overwrite the file
    cards_extracted_path = "../data/cards_extracted.json"
    with open(cards_extracted_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)
