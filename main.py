import numpy as np
from timeit import default_timer
from time import sleep
import HE_context, election_key, election_admin, voting, plot_results
from Crypto.Cipher import AES

def simulate_election():
    # Election Setup
    HE = HE_context.generate_HE()
    title, polling_place, candidates, registered_n = election_admin.generate_election()
    candidate_number = len(candidates)

    components, ciphertext, tag, nonce = election_admin.distribute_key(polling_place)
    officials = components
    print('Components distributed to officials, successful election setup. Proceeding with the voting')
    sleep(1)
    print('Voting Started')
    sleep(3)
    start1 = default_timer()
    
    # Voting Phase
    votes_test, voter_n, results = voting.simulate_results(registered_n, candidate_number)
    encrypted_votes = voting.vote_encryption(votes_test, HE)
    errors = voting.ballot_safety(votes_test)
    end1 = default_timer()
    print('Voting Simulation & Encryption End | Elapsed Time {}'.format(end1 - start1))
    sleep(2)
    
    # Officials Key
    quorum_key = election_key.byte_xor(*officials) ### Election Officials in agreement
    cipher = AES.new(quorum_key, AES.MODE_EAX, nonce)
    officials_result = cipher.decrypt_and_verify(ciphertext, tag)
    
    # STart counting & Decrypt Results
    if (officials_result == polling_place):
        print(officials_result,' - Election Officials Combined Key Matches the Master Key')
        print('Voting Count in the Cipherspace Started...')
        sleep(3)
        start2 = default_timer()
        election_results = voting.count_votes(encrypted_votes)
        end2 = default_timer()
        print('Counting finished | Elapsed Time: {}'.format(end2 - start2))
        print()
        
        # Print the final ciphers:
        print('Type "yes" if you want to display the final ciphertexts representing the results')
        if input() == 'yes':
            HE_context.display_ciphers(candidates, election_results)
        
        # Final Results
        print("~~~ Partial HE (Addition) Voting Scheme: ~~~")
        print('Election Results: ')
        print('{} | {}'.format(title, officials_result))
        print('Total Registered: ', registered_n)
        print('Turnout: {:10.2f}%, ({}/{})'.format((voter_n / registered_n) * 100, voter_n, registered_n))
        decrypted_results = HE_context.decrypt_results(HE, election_results)

        result_error = 0
        print('why dude', results)
        for i in range(len(election_results)):
            if (decrypted_results[i] != results[i]):
                result_error += 1
            print('{} total votes for candidate/option: {}'.format(decrypted_results[i], candidates[i]))        
        
        # Plotting the Pie & Donut Charts
        print('{} / {} result decryption failures'.format(result_error, candidate_number))
        if result_error > 0:
            raise SystemError('Decryption Failure | Process Compromised')
        plot_results.visualize(decrypted_results, title, registered_n, candidates)
        print('Successful Homomorphic Encryption Experience')
        return result_error

if __name__ == "__main__":       
    runs = 1
    for i in range(runs):
        simulate_election()

    # error = total_errors / (candidate_number * runs)

    # print('')
    # print('testing ended : {} Runs'.format(runs))
    # print('{} total voters, HE percentage of error on result: {}'.format(total_registered, error * 100))
