#!/usr/bin/env python3

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

from datetime import date
from pathlib import Path
import re
import requests
import subprocess
import sys

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/?per_page=1"
APOD_FOLDER = Path.home() / "Pictures" / "APOD"
TIMEOUT_API = 10
TIMEOUT_IMAGE = 30
WALLPAPER_OPTION = "zoom"

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

# get current APOD
def get_apod(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        print("Error retrieving APOD:", error)
        sys.exit(1)

    data = response.json()

    today = date.today().isoformat()

    apod = next((item for item in data if item["date"] == today), None)

    if apod is None:
        print("No apod found for", today)
        sys.exit(1)

    return apod

def download_image(url, path, timeout):
    # get image
    try:
        image_response = requests.get(url, timeout=timeout)
        image_response.raise_for_status()
    except requests.RequestException as error:
        print("Error retrieving image:", error)
        sys.exit(1)

    # save image
    try:
        with open(path, "wb") as image_file:
            image_file.write(image_response.content)
    except OSError as error:
        print("Error saving image:", error)
        sys.exit(1)

def set_wallpaper(path, wallpaper_option):
    wallpaper_uri = path.as_uri()

    try:
        subprocess.run([
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-options",
            wallpaper_option
        ], check=True)

        subprocess.run([
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri",
            wallpaper_uri
        ], check=True)

        subprocess.run([
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri-dark",
            wallpaper_uri
        ], check=True)

    except (OSError, subprocess.CalledProcessError) as error:
        print("Error setting wallpaper:", error)
        sys.exit(1)


# ------------------------------------------------------------
# Main programme
# ------------------------------------------------------------

def main():
    apod = get_apod(URL, TIMEOUT_API)

    # check if apod is image
    if apod["media_type"] != "image":
        print("APOD is not an image today.")
        sys.exit(0)

    # current apod is an image
    # get image data
    image_title = apod["title"]
    image_title = re.sub(r'[:/?]', '-', image_title).strip()
    image_date = apod["date"]
    image_url = apod["hdurl"]

    # prepare filename
    APOD_FOLDER.mkdir(parents=True, exist_ok=True)

    filename = image_date + "_" + image_title + ".jpg"
    image_path = APOD_FOLDER / filename

    # check if image already exists
    existing_files = list(APOD_FOLDER.glob(image_date + "_*"))

    if existing_files:
        print("APOD for", image_date, "already downloaded:", existing_files[0])
        sys.exit(0)

    download_image(image_url, image_path, TIMEOUT_IMAGE)

    set_wallpaper(image_path, WALLPAPER_OPTION)

if __name__ == "__main__":
    main()