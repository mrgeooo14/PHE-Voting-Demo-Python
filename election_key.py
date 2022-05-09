from Crypto.Random import get_random_bytes
# This file generates the final election key [AES] that will be used to decrypt the final ciphertext giving the result of the election
officials_number = 5
security_level = 256

def byte_xor(b1, b2, b3, b4, b5): # XOR operation between the components and the key, [b1 to b5] represents the election officials
    return bytes([_a ^ _b ^ _c ^ _d ^ _e for _a, _b, _c, _d, _e in zip(b1, b2, b3, b4, b5)])

def generate_key():
    return get_random_bytes(security_level // 8)

def generate_components(key):
    components = [get_random_bytes(security_level // 8) for _ in range(officials_number - 1)]
    final_component = byte_xor(key, *components)
    components.append(final_component)
    return components
