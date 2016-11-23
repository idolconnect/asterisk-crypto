# Compatible with Python3
# -*- coding: utf-8 -*-

import requests
import crypto

if __name__ == '__main__':
	data = requests.get("http://app01.gameicone.net:10080/user/login").text
	print("OriginalResponse: ", data)
	decrypted = crypto.decrypt(data)
	print("DecryptedResponse: ", decrypted)
	encrypted = crypto.encrypt(decrypted)
	print("EncryptedDecryptedResponse: ", encrypted)
	decrypted2 = crypto.decrypt(encrypted)
	print("DecryptedEncryptedDecryptedResponse: ", decrypted2)
	if decrypted == decrypted2:
		print("True")
