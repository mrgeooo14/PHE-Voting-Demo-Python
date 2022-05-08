import numpy as np
import election_key
from Crypto.Cipher import AES

polling_place = b'Carouge-01'

def generate_election(n):
    print('~~~~~Central Authorities~~~~~')
    print('Please specfiy the title of your election:')
    title = str(input())
    candidates = ['Louis', 'Friedrich', 'Ignazio']
    ballots = np.zeros((len(candidates), n), dtype=int)
    return title, candidates, ballots

# we need to encrypt the result of the election (again) (by the admin) so only the election officials can decrypt it
def distribute_key(polling):
    key = election_key.generate_key()
    components = election_key.generate_components(key)
    encrypted_cipher = AES.new(key, AES.MODE_EAX)
    nonce = encrypted_cipher.nonce
    ciphertext, tag = encrypted_cipher.encrypt_and_digest(polling)
    return components, ciphertext, tag, nonce


# ballot_test[0].flat[np.random.choice(1 * voter_n, 33, replace=False)] = 1
# print('After replacement: ')
# print(ballot_test)
