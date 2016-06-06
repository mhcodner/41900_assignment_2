import os
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


def decrypt_valuables(f):
    # Plain-text will print correctly
    try:
        print(str(f, 'ascii'))
        print("This text was not encrypted!")
    # Need to decrypt if it is actually encrypted
    except UnicodeDecodeError:
        # Get the private key and get associated hash digest size
        privateKey = RSA.importKey(open('Keys/master').read())
        digest_size = SHA.digest_size
        sentinel = Random.new().read(15 + digest_size)
        # Initialise the PKCS1 cipher
        cipher = PKCS1_v1_5.new(privateKey)
        # Decode the text
        decrypted_text = cipher.decrypt(f, sentinel)
        # Grab the digest and if the digest is right, print the decrypted data
        digest = SHA.new(decrypted_text[:-digest_size]).digest()
        if digest == decrypted_text[-digest_size:]:
            # Remove the digest from the message
            decrypted_text = decrypted_text[:-digest_size]
            decrypted_text = str(decrypted_text, 'ascii')
            print(decrypted_text)
        else:
            print("Decryption failed")


if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    decrypt_valuables(f)
