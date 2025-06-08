#!/usr/bin/env python3

def charov_decrypt(encrypted_data: bytes, seed: int) -> bytes:
    MODULUS = 2**64
    INCREMENT = 1442695040888963407
    MULTIPLIER = 6364136223846793005

    class LCG:
        def __init__(self, seed):
            self.state = seed

        def next(self):
            self.state = (self.state * MULTIPLIER + INCREMENT) % MODULUS
            return self.state

    lcg = LCG(seed)

    result = bytearray()
    for b in encrypted_data:
        key_byte = lcg.next() & 0xFF
        result.append(b ^ key_byte)

    return bytes(result)


def brute_seed(start_year, start_day):
    end_year = 2025

    for year in range(start_year, end_year + 1):
        max_day = (
            366
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            else 365
        )

        for day in range(start_day, max_day + 1):
            seed = (year << 16) | day
            yield seed, year, day


def musor(text: str) -> str:
    target_length = len(text) // 2
    return ''.join([text[i] for i in range(len(text)) if i % 2 == 0][:target_length])


if __name__ == "__main__":
    start_year = 1970
    start_day = 1
    encrypted_data = (
        b'\xfe\x20\x05\x13\x00\x0b\x84\xd7\xe4\xdd\xdb\x48\x8a\x33\xe6\xa6'
        b'\xf4\x49\x93\xbe\x18\x49\xf3\xa3\xef\xef\x36\x1c\xa0\x45\x3d\x7b'
        b'\xcd\x9f\xfe\x6b\xee\x64\x4e\x38\xcc\x01\xb9\xb3\x6e\x86\x86\x06'
        b'\xc0\xa9\x6b\x06\xf8\xbd\xd3\xc3\xda\x4b\x0d\x7e\x7c\xad\x12\xb1'
        b'\xa2\xf1\xc6\xd0\xd1\xd7\x47\x91\xa0\x96\x94\x07\x54\xe7\x9a\x7b'
        b'\xbb\x08\x5c\x6d\xc5\x25\xae\x5b\xad\xa0\xf6\xdf\x60\x10\xe8\x10'
        b'\x8f\x45\xaa\x07\x98\x3e\x38\xe2\x98\xed\x7b\x69\x3b\x6d\x46\xd3'
        b'\x80\x6a\x29\xc9\xa5\x45\x8e\xaf\x95\x18\xc2\x3f\x00\x70\xcc\x65'
        b'\x6d\xbe\x82\x9b\x92\x91\x16\x4d\x63\x55\x48\xd6'
    )

    for seed, year, day in brute_seed(start_year, start_day):
        decrypted = charov_decrypt(encrypted_data, seed)

        try:
            decrypted_text = decrypted.decode('utf-8')
            if decrypted_text.isprintable():
                cleaned_text = musor(decrypted_text)
                print(f"Seed: {seed} | Флаг: {cleaned_text[int(len(cleaned_text)/2):]}")
        except UnicodeDecodeError:
            continue
