import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    upper_case = {chr(i+65): chr(((i+shift) % 26) + 65) for i in range(0, 26)}
    lover_case = {chr(i+97): chr(((i+shift) % 26) + 97) for i in range(0, 26)}

    for i in plaintext:
        if i in upper_case:
            ciphertext += upper_case[i]
        elif i in lover_case:
            ciphertext += lover_case[i]
        else:
            ciphertext += i
    return ciphertext



def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    upper_case = {chr(i + 65): chr(((i - shift) % 26) + 65) for i in range(0, 26)}
    lover_case = {chr(i + 97): chr(((i - shift) % 26) + 97) for i in range(0, 26)}

    for i in ciphertext:
        if i in upper_case:
            plaintext += upper_case[i]
        elif i in lover_case:
            plaintext += lover_case[i]
        else:
            plaintext += i

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
