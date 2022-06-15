import election_key
import string, random
from time import sleep
from getpass import getpass
from Crypto.Cipher import AES

def generate_election():
    print('~~~~~Central Authorities~~~~~')
    print('Please specify the title of your election:')
    title = str(input())
    print('How many candidates/options on the ballot?')
    c_n = int(input())
    print('What are their names? ')
    candidates = [str(input()) for _ in range(0, c_n)]
    salting = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    print('In which local polling station is the election being conducted?')
    polling_place = bytes(str(input() + salting), encoding = 'utf-8')
    print('How many registered voters do you want the simulation to have? (Note: Max 50000 to avoid errors)')
    total_registered = int(input())
    print('Sending election data to administrators...')
    sleep(2)
    return title, polling_place, candidates, total_registered

# we need to encrypt the result of the election (again) (by the admin) so only the election officials can decrypt it
def distribute_key(polling):
    f = open('adminpass.txt', 'r')
    passw = f.read()
    print('~~~~~Election Administrators~~~~~')
    pass_input = getpass('Please input the password given from the authorities: ')
    if pass_input == passw:
        key = election_key.generate_key()
        sleep(1)
        print(r'Election Key k_e generated : ', key)
        sleep(3)
        components = election_key.generate_components(key)
        print('Key Components Generated: ', components)
        encrypted_cipher = AES.new(key, AES.MODE_EAX)
        nonce = encrypted_cipher.nonce
        ciphertext, tag = encrypted_cipher.encrypt_and_digest(polling)
        return components, ciphertext, tag, nonce
    else:
        raise PermissionError('Wrong password | Not an election administrator')


# ballot_test[0].flat[np.random.choice(1 * voter_n, 33, replace=False)] = 1
# print('After replacement: ')
# print(ballot_test)
