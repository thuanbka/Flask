import hashlib
import sys
import json
def sha256_encode(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string

if __name__ == "__main__":
    number_args = len(sys.argv)
    if number_args >= 2:
        if sys.argv[1] == "check_encode_sha256":
            if number_args == 3:
                code = sys.argv[2]
                print("Encode SHA256 for '%s':"%(code))
                print(sha256_encode(code))
            else:
                print("Please enter a string which you want to encode.")

    else:
        print("...................")
