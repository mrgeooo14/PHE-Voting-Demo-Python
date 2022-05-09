import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyCtxt # Pyfhel has most of the functions, plaintext and ciphertext classes
from time import sleep

def convert_bytes(bytes):
    return int.from_bytes(bytes, 'big')

def simulate_results(total_registered, candidate_n):
    if candidate_n == 3:
        results = [int(total_registered * 0.55), int(total_registered * 0.3), int(total_registered * 0.08)] ## Preset
    else:
        random_result = np.random.dirichlet(np.ones(candidate_n),size=1)
        turnout = total_registered * 0.85
        results = [int(turnout * x) for x in random_result[0]]
    voter_n = np.sum(results)
    votes = np.zeros((candidate_n, voter_n), dtype=int)
    for i in range(len(votes)):
        votes[i].flat[np.random.choice(1 * voter_n, results[i], replace = False)] = 1
    return votes, voter_n, results


def vote_encryption(ballot, context):
    x_gen = []
    for votes in ballot:
        print('...encrypted voting', end = '', flush = True)    
        encrypted = []
        for v in votes:
            encrypted.append(context.encryptInt(v))  ## Encrypt votes into ciphertexts
        print('...', end = '', flush = True)
        print()
        x_gen.append(encrypted)
    # print('Ciphertexts: ', x_gen)
    return x_gen


def ballot_safety(ballot):
    spoiled_ballots = []
    print('Ballot Safety Check Start [Injection Attacks]')
    sleep(2)
    for b in ballot:
        for i in range(0, len(b)):
            if (b[i] != 0 and b[i] != 1):
                print('Spoiled Vote Found!!', b[i])
                spoiled_ballots.append(b[i])
                b[i] = 0
    if spoiled_ballots == []:
        print('No spoiled votes found!')
    sleep(2)
    return spoiled_ballots


def count_votes(ballot):
    results = []
    for candidate in ballot:
        addition = candidate[0]
        for i in range(1, len(candidate)):
            addition += candidate[i]
        results.append(addition)
    return results
