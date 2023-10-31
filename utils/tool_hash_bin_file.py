import hashlib
import sys
def hash_data(name_file):
    with open(name_file, 'rb') as file:
        binary_data = file.read()
        sha1 = hashlib.sha1(binary_data).hexdigest()
        sha256 = hashlib.sha256(binary_data).hexdigest()
        print("SHA1: " + sha1)
        print("SHA256: " + sha256)

if __name__ == "__main__":
    number_args = len(sys.argv)
    if number_args >= 2:
        path_file = sys.argv[1]
        hash_data(path_file)
    else:
        print("...................")

