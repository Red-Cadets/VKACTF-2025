#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from re import findall
import random
import math
import numpy as np

with open("flag.txt", "r") as f:
    flag = f.read()
with open("banner.txt","r") as f:
    banner = f.read()


def zapret(text):
    alphavit = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return any(char in alphavit for char in text)

def polybius(text: str) -> str:
    if text is None:
        return None

    if text == "":
        return None

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

    encrypted_text = ""

    for char in text:
        found = False
        for i, row in enumerate(polybius_square):
            for j, ch in enumerate(row):
                if char == ch:
                    encrypted_text += str(i + 1) + str(j + 1)
                    found = True
                    break
            if found:
                break
        if not found:
            encrypted_text += char

    return encrypted_text

def splitter(number_str: str) -> list:
    pairs = []
    for i in range(0, len(number_str), 2):
        pair = number_str[i:i+2]
        pairs.append(int(pair))
    return pairs

def sizer(pairs_count: int) -> tuple:
    size = math.ceil(math.sqrt(pairs_count))
    return (size, size)

def zagnat_v_ramki(pairs: list, rows: int, cols: int) -> list:
    padded = pairs + [0] * (rows * cols - len(pairs))
    matrix = []
    for i in range(rows):
        start = i * cols
        end = start + cols
        matrix.append(padded[start:end])
    return matrix

def transposer(matrix: list) -> list:
    return [list(row) for row in zip(*matrix)]

def multiplier(matrix1: list, matrix2: np.ndarray) -> list:
    np_matrix1 = np.array(matrix1)
    result = np.dot(np_matrix1, matrix2)
    return result.astype(int).tolist()

def razdelitel(matrix: list) -> str:
    number_str = ""
    for row in matrix:
        for num in row:
            number_str += str(num)
    return number_str

def encrypt(text: str):
    try:
        MAX_MATRIX_SIZE = 6
        MAX_TEXT_LENGTH = MAX_MATRIX_SIZE * MAX_MATRIX_SIZE * 2
        
        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]
        
        encrypted = polybius(text)
        
        pairs = splitter(encrypted)
             
        matrix = zagnat_v_ramki(pairs, MAX_MATRIX_SIZE, MAX_MATRIX_SIZE)
        
        transposed = transposer(matrix)
        
        invertible_matrix = np.array([
        [9, 5, 2, 7, 1, 5],
        [8, 3, 4, 8, 8, 7],
        [9, 8, 9, 9, 5, 2],
        [2, 1, 7, 3, 8, 10],
        [10, 5, 4, 5, 7, 5],
        [2, 9, 9, 6, 5, 10]
        ])
        
        multiplied = multiplier(transposed, invertible_matrix)

        final_number = razdelitel(multiplied)

        return final_number
        
    except ValueError as e:
        print("invalid input:", e)
        return None
        
def menuska():
    print("\n" + "="*40)
    print("Выберите действие:")
    print("1. Get flag - получить зашифрованный флаг")
    print("2. Encrypt - зашифровать свою фразу")
    print("3. Exit - выход из программы")
    print("="*40)
    
def main():
    print(banner)
    
    while True:
        menuska()
        choice = input("> ").strip().lower()
        
        if choice in ['1', 'get flag']:
            while True:
                FLAG = flag
                encrypted_flag = encrypt(FLAG)
                if encrypted_flag and len(encrypted_flag) == 144:
                    print(encrypted_flag)
                    break
        
        elif choice in ['2', 'encrypt']:
            while True:
                user_text = input("Введите текст: ")
                try:
                    if zapret(user_text):
                        print("Только латиница(")
                        continue
                    result = encrypt(user_text)
                    if result:
                        print(result)
                    break
                except Exception as e:
                    print("Попробуй еще раз")
        
        elif choice in ['3', 'exit']:
            break
        
        else:
            print("\nНеизвестная команда.")

if __name__ == "__main__":
    main()