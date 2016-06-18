import os
import shutil
from mutagen import File
from getpass import getpass
try:
	from gmusicapi import Webclient
	from gmusicapi import Mobileclient
except ImportError:
	raise("Please make sure you install the gmusicapi library by running 'pip install gmusicapi' from a command line!")

BASE_DIR = os.getcwd()
USERNAME = raw_input("Google Username:\n")
PASSWORD = getpass("Google Password:\n")
ANDROID_ID = raw_input("Android ID (this is optional, leaving it blank will attempt to use MAC address as ID):\n")
ALBUM = raw_input("Name of Album to fix in GPM:\n")
ALBUM_DIR = raw_input("Folder path containing the songs with the correct artwork embedded:\n")
BACKED_UP_FOLDER_ALBUM = False
BACKED_UP_FOLDER = False
VERBOSE = True

api = Mobileclient()
webapi = Webclient()
clear = lambda: os.system('cls')

if VERBOSE: print "Logging in...\n"
api_logged_in = api.login(USERNAME, PASSWORD, ANDROID_ID) if ANDROID_ID else api.login(USERNAME, PASSWORD, Mobileclient.FROM_MAC_ADDRESS)
web_logged_in = webapi.login(USERNAME, PASSWORD)

if not api_logged_in and not web_logged_in:
	raise('Both Mobile and Web logins failed!')
elif api_logged_in and not web_logged_in:
	raise('Web login failed!')
elif web_logged_in and not api_logged_in:
	raise('Mobile login failed!')
elif api_logged_in and web_logged_in:
	if VERBOSE: print "Logged in!\n"

### THROWING AWAY YOUR PASSWORD! ###
USERNAME = ''
PASSWORD = ''
ANDROID_ID = ''

### Extracting Album Art! ###
if VERBOSE: print "Extracting Album Art from MP3 Files...\n"
os.chdir(ALBUM_DIR)
try:
	os.mkdir("AlbumArt")
except WindowsError:
	if VERBOSE: print "Detected existing AlbumArt folder, backing up..."
	os.rename("AlbumArt","AlbumArtBackup")
	os.mkdir("AlbumArt")
	BACKED_UP_FOLDER_ALBUM = True

song_files = [file for file in os.listdir(os.getcwd()) if os.path.splitext(file)[1] == '.mp3']
for item in song_files:
	file = File(item)
	for i in file.tags:
			if i.startswith("APIC"):
				artwork = file.tags[i].data
				if file.tags[i].mime == 'image/jpeg':
					image_ext = '.jpg'
				elif file.tags[i].mime == 'image/png':
					image_ext = '.png'
				else:
					image_ext = '.' + file.tags[i].mime.split('/')[1]
	title = file.tags['TIT2'].text[0].replace('/','-')
	if artwork:
		with open('AlbumArt\\' + title + image_ext, 'wb') as outfile:
			outfile.write(artwork)
	else:
		print "Song '" + title + "' has no embedded artwork, skipping."
if os.path.exists(BASE_DIR+"\\AlbumArt"):
	if VERBOSE: print "Detected existing AlbumArt folder, backing up..."
	os.rename(BASE_DIR+"\\AlbumArt", BASE_DIR+"\\AlbumArtBackup")
	BACKED_UP_FOLDER = True
os.rename("AlbumArt", BASE_DIR+"\\AlbumArt")
if BACKED_UP_FOLDER_ALBUM:
	if VERBOSE: print "Restoring AlbumArt folder backup..."
	os.rename("AlbumArtBackup", "AlbumArt")
os.chdir(BASE_DIR)

### Uploading proper art! ###
if VERBOSE: print "Uploading proper art...\n"

library = api.get_all_songs()
album_songs = [{'title':track['title'],'id':track['id']} for track in library if track['album'] == ALBUM]
art_files = [{'title':os.path.splitext(x)[0],'path':x} for x in os.listdir('AlbumArt')]
success_list = []

os.chdir("AlbumArt")
for song in album_songs:
	for artwork in art_files:
		if song['title'].replace('/','-') == artwork['title']:
			success = webapi.upload_album_art(song['id'], artwork['path'])
			if success:
				if VERBOSE: print "Fixed art for: " + song['title']
				success_list.append(song['title'])
if VERBOSE: print "Fixed the artwork of " + str(len(success_list)) + "/" + str(len(album_songs)) + " songs."
os.chdir(BASE_DIR)
shutil.rmtree("AlbumArt")
if BACKED_UP_FOLDER:
	if VERBOSE: print "Restoring AlbumArt folder backup..."
	os.rename("AlbumArtBackup", "AlbumArt")