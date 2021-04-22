import hashlib

str_test = "test sha"

sha = hashlib.sha1(str_test.encode())

print(sha.hexdigest())