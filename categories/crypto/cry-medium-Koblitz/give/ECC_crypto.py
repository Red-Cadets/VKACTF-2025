from sage.all import *
from Crypto.Util.number import getPrime


class SafeEllipticCurve:
    def __init__(self, bits, secp256k1):
        self.bits = bits
        if secp256k1:
            self.curve, self.generate_point = self.generate_secp256k1()
        else:
            self.curve, self.generate_point = self.generate_elliptic_curve()


    def generate_secp256k1(self):

        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a = 0
        b = 7
        gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        F = GF(p)
        E = EllipticCurve([F(a), F(b)])
        G = E((F(gx), F(gy)))

        return E, G

    def generate_elliptic_curve(self):
        while True:
            p = getPrime(self.bits)
            a = randrange(1, p-1)
            b = randrange(1, p-1)

            if (4*a**3 + 27*b**2) % p != 0:
                E = EllipticCurve(GF(p), [a, b])
                if E.order().is_prime():
                    self.G = E.random_point()
                    return E, self.G

    def get_curve(self):
        return self.curve

    def get_parameters(self):
        return {
            'field': self.curve.base_ring(),
            'equation': self.curve,
            'order': self.curve.order()
        }
    
    def get_generate_point(self):
        return self.generate_point
    
class KoblitzCurve:
    def __init__(self, SafeEllipticCurve):
        self.SafeEllipticCurve = SafeEllipticCurve
        self.G = SafeEllipticCurve.get_generate_point()
        self.alp_enc = {i: self.G * i for i in range(256)}
        self.alp_enc_flipped = {value: key for key, value in self.alp_enc.items()}

    def keygen(self, block_size):
        k = [randrange(1, self.SafeEllipticCurve.get_curve().order() - 1) for _ in range(block_size)]
        return k
        
    def encrypt(self, msg: list, k: list):

        G_k = [self.G * k[i] for i in range(len(k))]
        ciphertext = []

        for i in range(len(msg)):
            ciphertext.append(self.alp_enc[msg[i]] + G_k[i%len(G_k)])
        
        return ciphertext
    
    def decrypt(self, ciphertext, k: list):

        G_k = [self.G * k[i] for i in range(len(k))]
        plaintext = []

        for i in range(len(ciphertext)):
            plaintext.append(self.alp_enc_flipped[ciphertext[i] - G_k[i%len(G_k)]])
                
        return plaintext

class ECC_module:
    def __init__(self):

        bits_length = 64
        self.block_size = 1
        curve_instance = SafeEllipticCurve(bits_length, secp256k1=False)
        self.Koblitz = KoblitzCurve(curve_instance)

    def get_keys(self):
        return self.Koblitz.keygen(self.block_size)
    
    def encrypt(self, msg: list, k: list):
        ciphertext = self.Koblitz.encrypt(msg, k)

        return ciphertext
    
    def decrypt(self, ciphertext, k: list):
        return self.Koblitz.decrypt(ciphertext, k)

