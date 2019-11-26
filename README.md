# Basics
This is a simple proof of concept ransomware writen in Python that uses asymmetric encyption via an RSA public/private key pair.


# Usage
## WARNING: 
   Only use on systems you yourself own or on systems you have the explicit permission of the owners to run on (i.e. CTFs, etc).
   
## encrypt.py
Load the file encrypt.py onto the target system and run it.  It will automatically install the decryptor file after it has finished encrypting the targets files. The variable SERVER must be changed in the file at a minimum to contact the correct C2 server 

## decryptor.py
After the file is loaded you can run decryptor.py and it will ask for a password.  The default password is "Password".  At this point the files will be decrypted. The SERVER variable will also need to be changed to contact the correct C2. 

## c2.py
c2.py sets up a simple Flask server at port 5000 of your machine to create and serve up the RSA keys.

# Limitations
1. This software intentionally does not scale very well, as it just dumps all current keys in the current working directory. 
2. While the decryptor file warns there is a maximum password attempt limit, no limit exists as it was not implemented on the server. 
3. All ransomware agents share the common password of 'Password' to decrypt the files. This is by design. 


## Additional Information / Disclaimer
This PoC was created solely with the intent to learn how other ransomeware variants work as well as give those in the Infosec community a fairly safe copy to examine.
I do not support or encourage the use of this software or other software like it in any illegal form and will not be held responsible if others use it illegally. 
