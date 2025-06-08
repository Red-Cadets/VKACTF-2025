import os
from ECC_crypto import ECC_module
import pyfiglet
import random

class Converter:

    def rus_to_byte(self, text: str):
        byte = []
        for i in text:
            byte.append(int.from_bytes((i.encode("utf-8")), "little") // 256)
        return byte
    
    def byte_to_rus(self, byte: list):
        rus = ""
        for i in byte:
            if i == 0: 
                rus += int.to_bytes(32, 2, "little").decode("utf-8")
            else: 
                rus += int.to_bytes(i * 256 + 208, 2, "little").decode("utf-8")
        return rus
    
class Challenge:
    def __init__(self):
        self.conver = Converter()
        self.ecc = ECC_module()
        self.intro = pyfiglet.figlet_format("RusLit", font="slant")
        self.resp_num = 0
        self.texts = []

        with open("text/rus_3.txt", "r") as f:
            self.text = f.read()

        for line in self.text.splitlines():
            self.texts.append(line)

    def clear_screen(self):
        # Очищаем экран в зависимости от ОС
        os.system('cls' if os.name == 'nt' else 'clear')

    def new_text(self):
        self.clear_screen()  # Очистка экрана
        print("Press ESC to exit")
        print("\nPress ENTER to continue")
        ciphertext = self.cipher()
        print("\n" + str(ciphertext))

    def get_text(self):
        self.resp_num += 1
        return self.texts[self.resp_num - 1 % len(self.texts)]

    def cipher(self):
        rus = self.get_text()
        byte = self.conver.rus_to_byte(rus)

        ciphertext = self.ecc.encrypt(byte, self.k)
        byte = self.ecc.decrypt(ciphertext, self.k)

        rus = self.conver.byte_to_rus(byte)
        assert rus == rus

        return ciphertext

    def challenge(self):
        self.clear_screen()  
        print(self.intro)
        print("\nPress ENTER to continue")
        self.k = self.ecc.get_keys()
        while True:
            key = input()
            if key == "":  
                self.new_text()
            elif key == "\x1b":  
                break

if __name__ == "__main__":
    challenge = Challenge()
    challenge.challenge()
