# ALOP Scraper

This repository contains a Python scraper designed to extract card data and images from the Liga One Piece (ALOP) website. It uses Selenium for web scraping, BeautifulSoup for parsing HTML, and requests for downloading images.

## Features

* **Automated Data Extraction:** Scrapes card names, slugs, prices, and illustration image URLs from ALOP set pages.
* **Image Downloading:** Downloads card illustrations and saves them locally.
* **Multi-threaded Downloads:**  Utilizes multi-threading to speed up image downloading.
* **Special Character Handling:** Includes a function to delete local image files containing invalid characters.
* **Cleaned Editions List:** Generates a JSON file (`data/cleaned_editions.json`) with structured information about each ALOP set (name, code, deck link).
* **Path List for Scraping:** Creates a JSON file (`data/path_list.json`) containing the paths to local HTML files or URLs for each set, streamlining the scraping process.


## Requirements

* Python 3.11 (recommended)
* Libraries listed in `pyproject.toml` (install using `poetry install`)
* ChromeDriver (ensure compatibility with your Chrome browser version)

## Usage

1. **Install Dependencies:**
   ```bash
   poetry install
   ```

2. **Download ChromeDriver:** Download the appropriate ChromeDriver executable for your Chrome version and place it in the `drivers` directory.

3. **Update `data/path_list.json`:** 
   - The scraper can either work with local HTML files of set pages (recommended for large datasets to avoid excessive web requests) or directly scrape from URLs.
   - If using local files, first download the HTML for each set page (e.g., using the `download_editions` function in `src/download_editions.py`) and save them to the `htmls` directory. Ensure the `path_dir` values in `path_list.json` point to these local files.
   - If scraping directly from URLs, update the `path_dir` values in `path_list.json` with the ALOP set page URLs. 


4. **Run the Scraper:**
   ```bash
   poetry run python main.py
   ```
   - Set `DOWNLOAD_IMAGES = True` in `main.py` to download images.
   - Set `CHECK_SPECIAL_CHARS = True` to delete existing image files with special characters before downloading. 

## Data Output

* `data/cards_extracted.json`: Contains the extracted card data.
* `static/`: Stores the downloaded card illustration images.

## Project Structure

* `constants.py`: Stores constant values like the base URL.
* `data/`: Contains JSON files for storing extracted data and configuration.
* `drivers/`: Stores web driver executables.
* `htmls/`: Stores downloaded HTML files of set pages (when using local files).
* `main.py`: The main script to run the scraper.
* `src/`: Contains the scraping and data processing functions.
   - `download_editions.py`: Functions to download set page HTML using Selenium.
   - `extract_cards_data.py`: Functions to extract card data from HTML using BeautifulSoup.
   - `mount_edition_list.py`: Functions to generate the cleaned editions list and the path list for scraping.
* `static/`: Stores downloaded card images.
