from asyncore import poll
import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyCtxt # Pyfhel has most of the functions, plaintext and ciphertext classes
from HE_context import generate_HE
from Crypto.Cipher import AES
import election_key, election_admin
import time

def convert_bytes(bytes):
    return int.from_bytes(bytes, 'big')


def vote_encryption(ballot, context):
    x_gen = []
    for votes in ballot:
        encrypted = []
        for v in votes:
            encrypted.append(context.encryptInt(v))  ## Encrypt votes into ciphertexts
        x_gen.append(encrypted)
    # print('Ciphertexts: ', x_gen)
    return x_gen


def ballot_safety(ballot):
    spoiled_ballots = []
    for b in ballot:
        for i in range(0, len(b)):
            if (b[i] != 0 and b[i] != 1):
                print('wtf: ', b[i])
                print('Spoiled Vote Found!')
                spoiled_ballots.append(b[i])
                b[i] = 0
    return spoiled_ballots


def count_votes(ballot):
    results = []
    for candidate in ballot:
        addition = candidate[0]
        for i in range(1, len(candidate)):
            addition += candidate[i]
        results.append(addition)
    return results
