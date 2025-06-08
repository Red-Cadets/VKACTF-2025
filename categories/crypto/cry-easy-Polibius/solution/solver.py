#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import numpy as np

def matrix_2_number(number_str: str) -> np.ndarray:
    numbers = []
    size = 6
    for i in range(0, len(number_str), 4):
        num = int(number_str[i:i+4])
        numbers.append(num)

    matrix = np.zeros((size, size), dtype=int)
    
    for i in range(size):
        for j in range(size):
            index = i * size + j
            if index < len(numbers):
                matrix[i][j] = numbers[index]
    return matrix

def decrypt_matrix(encrypted_matrix: np.ndarray) -> str:
    M = np.array([
        [9, 5, 2, 7, 1, 5],
        [8, 3, 4, 8, 8, 7],
        [9, 8, 9, 9, 5, 2],
        [2, 1, 7, 3, 8, 10],
        [10, 5, 4, 5, 7, 5],
        [2, 9, 9, 6, 5, 10]
    ])
    M_inv = np.linalg.inv(M)
    

    decrypted = np.dot(encrypted_matrix, M_inv).round().astype(int)
    decrypted = decrypted.T
    
    numbers = []
    for row in decrypted:
        for num in row:
            numbers.append(f"{num}")
    
    return ''.join(numbers)

def polibiusrator(encrypted_text: str) -> str:
    polybius_square = [
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'],
        ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a'],
        ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
        ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'],
        ['t', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1'],
        ['2', '3', '4', '5', '6', '7', '8', '9', ' '],
        ['.', '!', '?', '_', '+', '-', '{', '}', '@'],
        ['#', '$', '%', '^', '&', '*', '(', ')', ';'],
        [':', '"', "'", ',', '<', '>', '=', '/', '\\'],
        ['|', '~', '`', '[', ']', '©', '®', '™', '§']
    ]

    decrypted_text = ""
    i = 0
    while i < len(encrypted_text):
        if i + 1 < len(encrypted_text):
            row = int(encrypted_text[i]) - 1
            col = int(encrypted_text[i+1]) - 1
            if 0 <= row < len(polybius_square) and 0 <= col < len(polybius_square[0]):
                decrypted_text += polybius_square[row][col]
            i += 2
        else:
            i += 1
    return decrypted_text

def decrypt_message(encrypted_number: str) -> str:
    try:
        encrypted_matrix = matrix_2_number(encrypted_number)
        numbers_str = decrypt_matrix(encrypted_matrix)
        decrypted_text = polibiusrator(numbers_str)
        return decrypted_text
    except Exception as e:
        return e

encrypted_flag = "138714421479152711741769214518742199216420612517210518391975217319222272209713751255171810231050240614291842208819921985203311741204158414291169"
decrypted_flag = decrypt_message(encrypted_flag)
print("Расшифрованный флаг:", decrypted_flag)