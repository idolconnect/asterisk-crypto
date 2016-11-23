# Compatible with Python3
# -*- coding: utf-8 -*-
# Crypto of AsteriskLive on Python3.

import base64, time, hashlib
import requests
import rijndael

def encrypt_cbc(data, iv, key):
	if len(data) % 16:
		data += b"\x00" * (16 - (len(data) % 16))
	out = [iv]
	for i in range(0, len(data), 16):
		blk = bytes(data[i+j] ^ out[-1][j] for j in range(16))
		out.append(rijndael.encrypt(key, blk))
	return b"".join(out[1:])

def decrypt_cbc(data, iv, key):
	p = b"".join(rijndael.decrypt(key, bytes(data[i:i + len(iv)])) for i in range(0, len(data), len(iv)))
	return bytes((iv+data)[i] ^ p[i] for i in range(len(p)))

def encrypt(decrypted_body):
	iv = create_iv().encode()
	key = "XzPetwRQtSj7btjf24LJIahPhcLGQZCi".encode()
	step1 = encrypt_cbc(decrypted_body.encode(), iv, key)
	step2 = iv + base64.b64encode(step1)
	step3 = base64.b64encode(step2).decode()
	step4 = step3.replace("+", "*").replace("/", ",").replace("=", "-")
	return step4

def decrypt(encrypted_body):
	key = "XzPetwRQtSj7btjf24LJIahPhcLGQZCi".encode()
	step1 = encrypted_body.replace("*", "+").replace(",", "/").replace("-", "=")
	step2 = base64.b64decode(step1.encode()).decode()
	step3 = base64.b64decode(step2[16:].encode())
	step4 = step2[0:16].encode()
	step5 = decrypt_cbc(step3, step4, key).decode()
	step6 = remove(step5)
	return step6

def create_iv():
	step1 = str(int(time.time()))
	step2 = hashlib.sha1(step1.encode()).hexdigest()
	step3 = step2.replace("-", "")
	step4 = step3[0:16]
	return step4

def remove(s):
	ret = ""
	for c in s:
		if ord(c) >= 31:
			ret += c
	return ret