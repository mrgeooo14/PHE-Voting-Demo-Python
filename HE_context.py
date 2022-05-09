from Pyfhel import Pyfhel, PyPtxt, PyCtxt

# # Generating context. The value of p is important as it affects ciphertext lengths and overall performance.
# #  There are tje most important configurable parameters on this step
# #  Pallier encryption scheme that preserves addition

plaintext_mod = 65537
poly_coeff_mod = 4096

def generate_HE():
    print('~ Welcome to the Partially Homomorphic Encryption voting scheme ~')
    print("Creating Context and KeyGen in a Pyfhel Object ")
    print('Plaintext modulus: {}, Polynomial Coefficient Modulus: {}'.format(plaintext_mod, poly_coeff_mod))
    print()
    HE = Pyfhel()   # Creating empty Pyfhel object
    HE.contextGen(p=plaintext_mod, m=poly_coeff_mod)
    HE.keyGen()             # Key Generation.
    return HE

def display_ciphers(candidates, results): # Results as Pyfhel Ciphertext Objects
    for i in range(len(results)):
        bytes_cipher = results[i].to_bytes()
        int_cipher = int.from_bytes(bytes_cipher, byteorder='big')
        print('Cipher for candidate {}: {} | Length: {}'.format(candidates[i], int_cipher, len(str(int_cipher))))


def decrypt_results(HE_context, cipher_results):
    decrypted_results = []
    for i in range(len(cipher_results)):
        resMul = HE_context.decryptInt(cipher_results[i])
        decrypted_results.append(resMul)
    return decrypted_results