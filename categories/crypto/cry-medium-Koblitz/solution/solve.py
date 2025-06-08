from pwn import remote
import re
from collections import Counter
from tqdm import tqdm

arr_encrypt_letters = ['о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'п', 'у',
                       'я', 'ы', 'ь', 'г', 'з', 'б', 'ч', 'й', 'х', 'ж', 'ш', 'ю', 'ц', 'щ', 'э', 'ф', 'ъ', 'ё']

def replace_points_with_letters(ciphertext, mapping):
    result = []
    for point in ciphertext:
        if point not in mapping:
            letter = chr(1072 + len(mapping))  
            mapping[point] = letter
        result.append(mapping[point])
    return ''.join(result)

def decrypt(encrypted_texts, arr_encrypt_letters):
    combined_text = ''.join(encrypted_texts)

    letter_count = Counter(combined_text)

    most_common_letters = [letter for letter, _ in letter_count.most_common()]

    mapping = {letter: arr_encrypt_letters[i] for i, letter in enumerate(most_common_letters)}

    decrypted_texts = []
    for text in encrypted_texts:
        decrypted_text = ''.join(mapping.get(char, char) for char in text)
        decrypted_texts.append(decrypted_text)
    
    return decrypted_texts

def main():
    n_iterations = 8000
    russian_sentences = [] 
    mapping = {}

    conn = remote('localhost', 1338)

    conn.recvuntil(b'Press ENTER to continue')
    conn.sendline(''.encode())

    for _ in tqdm(range(n_iterations)):

        conn.recvuntil(b'Press ENTER to continue')
        conn.recvline()
        conn.recvline()

        ciphertext_raw = conn.recvline().decode()

        points = re.findall(r'\(([^)]+)\)', ciphertext_raw)

        russian_text = replace_points_with_letters(points, mapping)

        russian_sentences.append(russian_text)

        conn.sendline(''.encode())
        
    conn.close()

    decrypted_texts = decrypt(russian_sentences, arr_encrypt_letters)

    for text in decrypted_texts:
        if "флаг" in text:
            print(text)

if __name__ == "__main__":
    main()

