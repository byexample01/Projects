#Encrypts a file using the symmetric AES-256 block cipher in GCM mode.
#GCM mode provides authenticated encryption for both data integrity and confidentiality. 
#A 32 byte key is generated from a hashed user input password - it is assumed
#that this password is already secretly agreed upon by the sender and receiver.
#Cryptographic cipher, hashing and padding algorithms taken from the pycryptodome
#package (an updated fork of the pycrypto package), available via the Python Package Index.

#Tested using pycryptodome v3.4.3 and Python v3.6.0

#For more info on ciphers and current cryptographic standards, see:
#http://csrc.nist.gov/groups/ST/index.html



from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from getpass import getpass




#---------------------------------------------------------------------------------#
#  FUNCTIONS                                                                      #
#---------------------------------------------------------------------------------#



# Generates a 32 byte key from a mutually-known password between sender and
# receiver. Password is input to the terminal, and hashed to 32 bytes using SHA-256.
# INPUT:  None
# RETURN: 32 byte key ("bytes" object)
def generate_key():

    password = getpass( "Enter password: " ) #get password without echoing
    byte_password = password.encode() #convert from string to "bytes" object
    hashed_password = SHA256.new( data=byte_password )
    key = hashed_password.digest()
    
    return key

    
    
# Encrypts a file using the AES-256 cipher in GCM mode.
# Writes encrypted file (incl. IV and MAC) to cwd with prefix: "encrypted_".
# INPUT:  filename including extension (string), key (32 byte "bytes" object)
# RETURN: None
def encrypt( plainfile, key ):

    #Read plaintext in binary mode:
    plain_handle = open( plainfile, "rb" )
    plaintext = plain_handle.read()
    plain_handle.close()
    
    #Padding of plaintext to a multiple of 16 bytes:
    block_size = 16
    plaintext = pad( plaintext, block_size, style="pkcs7" )
    
    #Construct and work on cipher object:
    cipher = AES.new( key, AES.MODE_GCM )
    ciphertext = cipher.encrypt( plaintext )
    nonce = cipher.nonce  #Initialisation Vector ("bytes" object)
    mac = cipher.digest() #Message Authentication Code ("bytes" object)
    
    #Write IV, MAC and ciphertext to file in binary mode:
    cipher_handle = open( "encrypted_"+plainfile , "wb" )
    [ cipher_handle.write(x) for x in (nonce, mac, ciphertext) ]
    cipher_handle.close()
  

  
# Decrypts a file using the AES-256 cipher in GCM mode.
# Writes plaintext to cwd with prefix: "decrypted_".
# Prints an error message if the encrypted file has been tampered with,
# or if the key does not match.
# INPUT:  filename including extension (string), key (32 byte "bytes" object)
# RETURN: 0 if MAC does not match, 1 if MAC does match
def decrypt( cipherfile, key ):

    #Read ciphertext in binary mode:
    cipher_handle = open( cipherfile, "rb" )
    nonce, mac, ciphertext = [ cipher_handle.read(x) for x in (16, 16, -1) ]
    cipher_handle.close()
    
    #Construct and work on cipher object:
    cipher = AES.new( key, AES.MODE_GCM, nonce )
    plaintext = cipher.decrypt( ciphertext )
    
    #Check for file tampering / wrong key first. If MAC does not match, raises a ValueError:
    try:
        cipher.verify( mac )
    except ValueError:
        print( "Either your key does not match, or the file has been tampered with." )
        return 0
    
    #Unpadding of plaintext, which should be a multiple of 16 bytes:
    block_size = 16
    plaintext = unpad( plaintext, block_size, style="pkcs7" )
    
    #Write plaintext to file in binary mode:
    plain_handle = open( "decrypted_"+cipherfile , "wb" )
    plain_handle.write( plaintext )
    plain_handle.close()
    
    return 1

    
 

    
#---------------------------------------------------------------------------------#
#  MAIN PROGRAM                                                                   #
#---------------------------------------------------------------------------------#



while True:

    #Encryption or decryption?
    resp = input( "Do you wish to perform encryption or decryption? (e/d): " )
    if resp != "e" and resp != "d":
        break 
        
    #Encryption:
    elif resp == "e":
        plainfile = input( "Enter the full filename in the cwd to encrypt: " )
        key = generate_key()
        encrypt( plainfile, key )
        print( plainfile, "encrypted." )
        print( "Saved as:", "encrypted_"+plainfile )
        print()
        
    #Decryption: 
    elif resp == "d":
        cipherfile = input( "Enter the full filename in the cwd to decrypt: " )
        key = generate_key()
        decrypt_boole = decrypt( cipherfile, key )
        if decrypt_boole == 1:
            print( cipherfile, "decrypted." )
            print( "Saved as: decrypted_"+cipherfile )
            print()
        else:
            print( cipherfile, "was not decrypted." )
            print()

    #Run again?
    proceed = input( "Run again? (y/n): " )
    if proceed == "y":
        print()
        continue
    else:
        break

        

