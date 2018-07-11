import hashlib
import getpass
name = input("what is your user name: ") #inserting user name
pw = getpass.getpass("Enter Password: ") #inserting passsword

mystring = name + pw
# Assumes the default UTF-8
hash_object = hashlib.sha256(mystring.encode()) # hashing the password username and salt
hash1 = hash_object.hexdigest()  # printing the hashed password and username 

pw2 = getpass.getpass("Re-Enter Password: ") # Confirming password

mystring1 = name + pw2
# Assumes the default UTF-8
hash_object1 = hashlib.sha256(mystring1.encode()) # hashing the password username and salt
hash2 = hash_object1.hexdigest()  # printing the hashed password and username 
if hash1 == hash2:
    print(hash1)
else:
    while hash1!= hash2:
        pw = getpass.getpass("Enter Password: ")
        mystring = name + pw
        # Assumes the default UTF-8
        hash_object = hashlib.sha256(mystring.encode()) # hashing the password username and salt
        hash1 = hash_object.hexdigest()  # printing the hashed password and username 
        pw2 = getpass.getpass("Re-Enter Password: ")
        mystring1 = name + pw2
        # Assumes the default UTF-8
        hash_object1 = hashlib.sha256(mystring1.encode()) # hashing the password username and salt
        hash2 = hash_object1.hexdigest()  # printing the hashed password and username 

