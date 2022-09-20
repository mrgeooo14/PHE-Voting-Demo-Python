# PHE-Voting-Demo-Python

This project and election demo using Homomorphic Encryption was created as part of the course "Advanced Security" given at the University of Geneva with the general goal being 
the demonstration of an election process with accurate results while working in the encrypted world, a personal choice of mine inspired by the 1988 PhD Thesis of *J. C. Benaloh* on
the same topic.

The **full documentation** explaining the theoretical concepts behind it,
motivation, implementation, and performance, can be found [here](https://drive.google.com/file/d/1DV14BTcAZMIW2E2fY8HWK9PymC0w54OF/view).

## Pyfhel
As Python was my language of choice used to create this demo, a highly effective and optimized library known as [Pyfhel](https://github.com/ibarrond/Pyfhel) was used. 
It essentially stands as a Python API for the other well-known C++ HE library developed by Microsoft, [SEAL](https://github.com/microsoft/SEAL#homomorphic-encryption), given
that the vote count is based on its implementation of the additive Paillier Scheme or RSA's multiplicative property.

## HE Context
Two important parameters called the *plaintext modulus* **p**, and the *polynomial coefficient modulus* **m** must be set on the **HE_context.py** file. These are two key parameters
since they affect the whole behaviour of ciphertexts during encryption/decryption and addition for the election result.

**m** is a power of 2 (starting from 1024) and its increase directly increases ciphertext sizes too, allowing more encrypted operations and security however resulting in a
hefty performance increase aswell.

## Admin Password
During the election simulation on the command line, the user is asked to type the password given by the election authorities. This was added as a simple method to demonstrate
an exchange of passwords from the election authorities to administrators on a local level and can be found and customized in the *adminpass.txt* file.

The default password is: **bern**

## Running
The simulation of an election using Partially Homomorphic Encryption can be started by simply running the *main.py* file which will start a custom election defined by the user
on the command line.

In addition to that, this demo can be tested for perfomance, results, and decryption failures by running the *simulate_election.py* file with custom run parameters defined
by the variables on the same file.
