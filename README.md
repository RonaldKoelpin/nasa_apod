nasa_apod
=====

Python Script to Download the NASA APOD and set it as your Ubuntu Desktop Wallpaper 
-----

About:
=====
![NASA APOD Example](https://assets.science.nasa.gov/dynamicimage/assets/science/cds/apod/apod/2026/september/M83_Final2_1x.jpg?w=3828&h=3798&fit=clip&crop=faces%2Cfocalpoint
"Example of a NASA APOD")

NASA's Astronomy Picture of the Day provides a different image or photograph of our fascinating universe each day, 
along with a brief explanation written by a professional astronomer.
This script downloads the current NASA APOD (if it is an image) and sets it as your Ubuntu desktop wallpaper.
There are already other scripts (https://github.com/randomdrake/nasa-apod-desktop) or GNOME extensions 
(https://extensions.gnome.org/extension/1202/nasa-apod/) out there doing the same thing but I wanted my own solution.

https://science.nasa.gov/apod/

Created for and tested under Ubuntu 24.04.

How It Works:
=====
1. Downloads the current APOD from NASA using their API https://science.nasa.gov/wp-json/wp/v2/apod-basic
and saves it to a previously determined directory (creates the directory if necessary).
2. Sets the image as your desktop wallpaper 


Installation:
=====
* Download the file and place it wherever you like. 
* Ensure you have Python installed (default for Ubuntu) as well as the necessary libraries.
* Optionally: run "chmod +x DOWNLOAD_PATH/nasa_apod.py" in your terminal to make the script executable.

Usage:
=====
There are at least 3 ways you can use this script, not necessarily mutually exclusive:

(1) Manual Use:
-----
* Open a terminal, navigate to your download directory and run "python3 DOWNLOAD_PATH/nasa_apod.py" or just 
"DOWNLOAD_PATH/nasa_apod.py" if you previously ran chmod +x.

(2) Use in Startup:
-----
* Open the Activities Overview using the Super Key/Windows Key.
* Search for and Open "Startup Applications Preferences".
* Click the "Add"-Button.
* Add whatever Name and Comment you like, set the command to "python3 DOWNLOAD_PATH/nasa_apod.py" 
or simply "DOWNLOAD_PATH/nasa_apod.py" if you previously ran chmod +x.
* Confirm by clicking the "Add"-Button.

(3) Automated Use:
-----
* nasa_apod.servic and nasa_apod.timer (from the config folder) create a system service (though user specific) that runs 
the script daily at a specified time. Still, we are messing with system services here, so handle with care. Remember: 
with great power comes great responsibility.
* You can change preset time by changing the line OnCalendar=*-*-* 07:00:00 in the nasa_apod.timer file.
* Copy the files nasa_apod.service and nasa_apod.timer files to ~/.config/systemmd/user
* In your terminal run "systemctl --user daemon-reload" to reload your user services and 
"systemctl --user start nasa_apod.timer" and "systemctl --user enable nasa_apod.timer" to start and enable the timed 
execution of that service.

License:
=====
Open-source and free for use.

>Copyright (c) 2026 Ronald Kölpin
>
>Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
>
>http://www.apache.org/licenses/LICENSE-2.0
>
>Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

Author:
=====
Ronald Kölpin 