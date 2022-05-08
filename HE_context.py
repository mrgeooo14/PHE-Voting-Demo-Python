from Pyfhel import Pyfhel, PyPtxt, PyCtxt

# # Generating context. The value of p is important.
# #  There are many configurable parameters on this step
# #  More info in Demo_ContextParameters.py, and
# #  in the docs of the function (link to docs in README)
# #  Pallier encryption scheme that preserves addition

plaintext_mod = 65537
poly_coeff_mod = 2048

def generate_HE():
    print('~ Welcome to the Partially Homomorphic Encryption voting scheme ~')
    print("Creating Context and KeyGen in a Pyfhel Object ")
    print('Plaintext modulus: {}, Polynomial Coefficient Modulus: {}'.format(plaintext_mod, poly_coeff_mod))
    print()
    HE = Pyfhel()   # Creating empty Pyfhel object
    HE.contextGen(p=plaintext_mod, m=poly_coeff_mod)
    HE.keyGen()             # Key Generation.
    return HE
