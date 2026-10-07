#!/usr/bin/env python3
#
# Copyright (c) 2026 David Drake
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# nasa_apod.py
# https://github.com/RonaldKoelpin/nasa_apod
#
# Written/Modified by Ronald Kölpin
#
# Tested on Ubuntu 24.04
#
#
#
# DEFAULTS
# URL               - address of NASA API to download the APOD from.
# APOD_FOLDER       - where you want you APOD to be downloaded
# TIMEOUT_API       - max waiting time when requesting current APOD from NASA APOD API
# TIMEOUT_IMAGE     - max waiting time to download actual image file from NASA APOD API
# WALLPAPER_OPTION  -
#       "none"      : no change. picture is taken as is.
#       "wallaper"  : tile pattern. picture is repeated.
#       "centered"  : picture is centered using its original size.
#       "scaled"    : picture is scaled proportionally to screen resolution.
#       "stretched" : picture is stretched to fit the entire screen.
#       "zoom"      : picture is enlarged proportionally. excess areas are cut off
#       "spanned"   : image is spread across multiple monitors.



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
WALLPAPER_OPTION = "scaled"

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def get_apod(url, timeout):
    # get current APOD
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