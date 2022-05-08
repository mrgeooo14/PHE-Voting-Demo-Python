import numpy as np
import HE_context, election_key, election_admin, voting, plot_results
from Crypto.Cipher import AES
import timeit
import matplotlib.pyplot as plt
start = timeit.default_timer()

def simulate_election(registered_n, rezyy):
    result_error = 0
    HE = HE_context.generate_HE()
    voter_n = np.sum(rezyy)
    polling_place = b'Carouge-01'
    title, candidates, votes_test = election_admin.generate_election(voter_n)

    for i in range(len(votes_test)):
        votes_test[i].flat[np.random.choice(1 * voter_n, rezyy[i], replace=False)] = 1

    errors = voting.ballot_safety(votes_test)
    print(errors, len(errors), votes_test[0])

    encrypted_votes = voting.vote_encryption(votes_test, HE)
    components, ciphertext, tag, nonce = election_admin.distribute_key(polling_place)
    officials = components
    quorum_key = election_key.byte_xor(*officials) ### Quorum 3/5
    cipher = AES.new(quorum_key, AES.MODE_EAX, nonce)
    result1 = cipher.decrypt_and_verify(ciphertext, tag)
    # Decryption by officials
    # resMul = [HE.decryptFrac(ctxtMul[i]) for i in np.arange(len(ctxtMul))]
    # decrypted_cipyer = AES.
    if (result1 == polling_place):
        print(result1,' - Election Officials Combined Key Matches the Master Key')
        print('Voting Count Started...')
        print('Election Results: ')
        election_results = voting.count_votes(encrypted_votes)
        
        # Print the final ciphers:
        for i in range(len(election_results)):
            bytes_test = election_results[i].to_bytes()
            int_cipher = int.from_bytes(bytes_test, byteorder='big')
            print('Cipher for candidate {}: {} | Length: {}'.format(i, int_cipher, len(str(int_cipher))))
        
        # print(ctxtMul)  ## This is the cipher containing the result of the election [each ballot]
        print(election_results[0]) ## the winner
        print("~~~ Partial HE (Addition) Voting Scheme: ~~~")
        print('Présidentielle 2022 | {}'.format(result1))
        print('Total Registered: ', registered_n)
        print('Turnout: {}%, ({}/{})'.format((voter_n / registered_n) * 100, voter_n, registered_n))
        intresults = []
        for i in range(len(election_results)):
            resMul = HE.decryptInt(election_results[i])
            intresults.append(resMul)
            if (resMul != rezyy[i]):
                result_error += 1
            print('{} total votes for candidate: {}'.format(resMul, candidates[i]))
        # print('what do you think')
        # print(HE.decrypt(election_results[0], decode_value=True))
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        print('wtf dude', intresults)
        
        plot_results.visualize(intresults, title, registered_n, candidates)
        return result_error


#Your statements here        
total_registered = 2500
candidate_number = 3
results = [int(total_registered * 0.55), int(total_registered * 0.3), int(total_registered * 0.08)]
runs = 1
total_errors = 0
for i in range(runs):
    total_errors += simulate_election(total_registered, results)

error = total_errors / (candidate_number * runs)
stop = timeit.default_timer()
time = stop - start

print('')
print('testing ended : {} Runs'.format(runs))
print('{} total voters, HE percentage of error on result: {}'.format(total_registered, error * 100))
print('Mean Time of Execution: {}'.format(time / runs))
