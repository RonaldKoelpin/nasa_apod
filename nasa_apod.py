#!/usr/bin/env python3
import re
import requests
import sys
import subprocess
from pathlib import Path
from datetime import date

# Globals
URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic/?per_page=1"
APOD_FOLDER = Path.home() / "Pictures" / "APOD"
TIMEOUT = 10
TIMEOUT_IMAGE = 30
WALLPAPER_OPTION = "zoom"

# get current APOD
try:
    response = requests.get(URL, timeout=TIMEOUT)
    response.raise_for_status()
except requests.RequestException as error:
    print("Error retrieving APOD:", error)
    sys.exit(1)

data = response.json()
# print("APOD entries received:", len(data))

# check if received apod is apod of today
today = date.today().isoformat()
apod = next((item for item in data if item["date"] == today), None)

if apod is None:
    print("No apod found for", today)
    sys.exit(1)

# check if apod is image
if apod["media_type"] != "image":
    print("APOD is not an image today.")
    sys.exit(0)

# Current APOD is an image
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

# get image
try:
    image_response = requests.get(image_url, timeout=TIMEOUT_IMAGE)
    image_response.raise_for_status()
except requests.RequestException as error:
    print("Error retrieving image:", error)
    sys.exit(1)

# save image
try:
    with open(image_path, "wb") as image_file:
        image_file.write(image_response.content)
        # print("APOD successfully downloaded:", image_path)
except OSError as error:
    print("Error saving image:", error)
    sys.exit(1)

# set image as wallpaper
wallpaper_uri = image_path.as_uri()
# print(wallpaper_uri)
try:
    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-options",
        WALLPAPER_OPTION
    ], check=True)

    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri",
        wallpaper_uri
    ], check=True)
except (OSError, subprocess.CalledProcessError) as error:
    print("Error setting wallpaper:", error)
    sys.exit(1)








# #!/usr/bin/env python3
#
# import subprocess
# from pathlib import Path
# from urllib.parse import urlparse
#
# import requests
#
#
# # ------------------------------------------------------------
# # Configuration
# # ------------------------------------------------------------
#
# API_KEY = "DEMO_KEY"
#
# DOWNLOAD_DIR = Path.home() / "Pictures" / "APOD"
#
# # The file that GNOME will use as the current wallpaper
# WALLPAPER_FILE = DOWNLOAD_DIR / "current.jpg"
#
#
# # ------------------------------------------------------------
# # Helper functions
# # ------------------------------------------------------------
#
# def get_apod():
#     """Retrieve today's Astronomy Picture of the Day metadata."""
#
#     url = "https://api.nasa.gov/planetary/apod"
#
#     response = requests.get(
#         url,
#         params={
#             "api_key": API_KEY,
#         },
#         timeout=30,
#     )
#
#     response.raise_for_status()
#
#     return response.json()
#
#
# def download_image(url, filename):
#     """Download an image from URL to filename."""
#
#     response = requests.get(url, timeout=60, stream=True)
#     response.raise_for_status()
#
#     with open(filename, "wb") as f:
#         for chunk in response.iter_content(chunk_size=1024 * 1024):
#             if chunk:
#                 f.write(chunk)
#
#
# def set_wallpaper(filename):
#     """Set the GNOME desktop wallpaper."""
#
#     uri = Path(filename).resolve().as_uri()
#
#     subprocess.run(
#         [
#             "gsettings",
#             "set",
#             "org.gnome.desktop.background",
#             "picture-uri",
#             uri,
#         ],
#         check=True,
#     )
#
#     # Also set the dark-mode wallpaper, if GNOME is using it.
#     subprocess.run(
#         [
#             "gsettings",
#             "set",
#             "org.gnome.desktop.background",
#             "picture-uri-dark",
#             uri,
#         ],
#         check=False,
#     )
#
#     # Zoom/crop the image so that it fills the screen.
#     subprocess.run(
#         [
#             "gsettings",
#             "set",
#             "org.gnome.desktop.background",
#             "picture-options",
#             "zoom",
#         ],
#         check=True,
#     )
#
#
# # ------------------------------------------------------------
# # Main program
# # ------------------------------------------------------------
#
# def main():
#
#     DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
#
#     print("Getting today's NASA APOD...")
#
#     apod = get_apod()
#
#     print(f"Title: {apod.get('title')}")
#     print(f"Date:  {apod.get('date')}")
#     print(f"Type:  {apod.get('media_type')}")
#
#     # APOD is occasionally a video rather than an image.
#     if apod.get("media_type") != "image":
#         print("Today's APOD is not an image.")
#         print("URL:", apod.get("url"))
#         return
#
#     image_url = apod["hdurl"] if "hdurl" in apod else apod["url"]
#
#     print("Image:", image_url)
#
#     # Determine a sensible extension.
#     extension = Path(urlparse(image_url).path).suffix.lower()
#
#     if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
#         extension = ".jpg"
#
#     # Keep a dated copy of the image.
#     dated_file = DOWNLOAD_DIR / f"{apod['date']}{extension}"
#
#     print(f"Downloading to {dated_file}")
#
#     download_image(image_url, dated_file)
#
#     # Copy it to the stable filename used by GNOME.
#     import shutil
#     shutil.copy2(dated_file, WALLPAPER_FILE)
#
#     print(f"Current wallpaper: {WALLPAPER_FILE}")
#
#     set_wallpaper(WALLPAPER_FILE)
#
#     print("Wallpaper successfully changed.")
#
#
# if __name__ == "__main__":
#     main()