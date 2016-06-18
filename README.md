# Google Play Music Album Art Fixer
Python Script to correct lost album art on GPM.

If you've ever tried uploading an album to GPM, you may have noticed that any songs within that album that have their own individual cover art lose that cover art once they're uploading. In addition, it's hardly ever replaced with the actual official album art, often it's just replaced by one of the individual song cover arts which has been picked at random.

I was annoyed that my only choices in fixing this were to manually edit the covers of my songs one by one or to just ignore it so I decided to write a script instead. This will pull the individual artworks from local copies of your MP3 files and automatically upload them to their respective songs on GPM, giving each song its proper individual cover art with minimal effort on your part.

## Getting set up
This script makes use of the ![gmusicapi](https://unofficial-google-music-api.readthedocs.io/en/latest/index.html) and ![mutagen](http://mutagen.readthedocs.io/en/latest/) Python modules, so make sure you have them installed. If you don't have them, you can install them by running `pip install gmusicapi` and `pip install mutagen` from a command-line respectively.

Once you have the dependencies, just grab `GPM Album Art Fixer.py` and place it in its own folder somewhere, preferably on the same drive as your locally stored music.

## Instructions
Run `GPM Album Art Fixer.py` and provide the details when prompted, the script will then automatically make all changes and clean up after itself.

When asked for the Album name, give it exactly how it appears in GPM. When asked for the Album Path, give the path to the locally stored files on your device which contain the correct cover artworks. e.g. `C:\path\to\album` - make sure the folder you provide only has the music files for the album you want to fix because if you provide a path to your entire music collection the script will try and generate artwork for every song in that folder.

You can leave the Android ID field blank and just press enter, this will prompt the script to try and use your device's MAC address as a fake Android ID. I'm not clear on how this works, this function is provided by the gmusicapi module. If you wish to play it safe and you have an Android device, you can use the ID from that device (you can get said ID through an app such as ![Device ID on the Play Store](https://play.google.com/store/apps/details?id=com.evozi.deviceid&hl=en)).

Unfortunately the gmusicapi module is unofficial and thus doesn't have access to OAuth for certain functions that are necessary for this script to work (like the function to upload new cover art). As such you will need to provide the username and password to your Google Account. This information is only used to log in to GPM and then immediately discarded - I tried to make this clear in the source.

If you wish to silence console output, change the VERBOSE variable to False.

### Screenshots
![1](http://i.imgur.com/mCNUtAC.png)
![2](http://i.imgur.com/eqNhDjK.png)
