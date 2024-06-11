from pathlib import Path
from typing import Generator
import math

def ext_euclid(a, b, verbose=False): 
    """a must be > b
    b mod a
    d = gcd(a, b)
    ax + by = d
    returns (x, y, d)
    so, y is the modulo multiplicative inverse of b mod a (when a > b)
    returns x, y, d: d = gcd(a, N) and ax+Ny = d
    """
    if b == 0:
        return (1, 0, a)
    (x, y, d) = ext_euclid(b, a % b, verbose)
    ret = (y, x-math.floor(a/b)*y, d)
    return ret


def mult_inv_mod(num, base):
    _, y, d = ext_euclid(base, num)
    if d == 1:
        return y if y > 0 else y + base
    else:
        raise Exception(f"{num} and {base} are not relatively prime")


def mod_exp(base: int, power: int, N: int):
    if power == 0:
        return 1
    z = mod_exp(base, power >> 1, N)
    if power & 1:  # Odd
        return (base * z ** 2) % N
    else:
        return (z ** 2) % N


def chunk_it(n_bytes: int, text: bytes) -> Generator[int, None, None]:
    for i in range(0, len(text), n_bytes):
        yield int.from_bytes(text[i:i+n_bytes], 'big')  # Specify byte ordering


def join_it(n_bytes: int, chunks: list[int]) -> bytes:
    # Convert each chunk back to bytes and join them
    return b''.join(chunk.to_bytes(n_bytes, 'big') for chunk in chunks)


def encrypt(N: int, exp: int, plaintext: bytes) -> bytes:
    n_bytes = (N.bit_length() + 7) >> 3  # i.e. // 8

    encrypted = []
    for chunk in chunk_it(n_bytes, plaintext):
        encrypted.append(mod_exp(chunk, exp, N))

    return join_it(n_bytes, encrypted)


def read_key(public_key_file: Path) -> tuple[int, int]:
    N, e, *_ = public_key_file.read_text().splitlines()
    return int(N), int(e)


def main(public_key_file: Path, input_file: Path, output_file: Path):
    N, e = read_key(public_key_file)
    plaintext = input_file.read_bytes()
    ciphertext = encrypt(N, e, plaintext)
    output_file.write_bytes(ciphertext)


if __name__ == '__main__':
    import sys
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
