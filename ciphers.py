import string

class Cipher:
    """Base class for ciphers."""
    def encrypt(self, text):
        raise NotImplementedError
    
    def decrypt(self, text):
        raise NotImplementedError

class CaesarCipher(Cipher):
    def __init__(self, shift=3):
        self.shift = shift % 26

    def encrypt(self, text):
        result = []
        for char in text:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - shift_base + self.shift) % 26 + shift_base)
                result.append(encrypted_char)
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, text):
        original_shift = self.shift
        self.shift = -self.shift
        decrypted_text = self.encrypt(text)
        self.shift = original_shift  # Restore original shift
        return decrypted_text

class RailFenceCipher(Cipher):
    def __init__(self, num_rails=3):
        self.num_rails = num_rails

    def encrypt(self, text):
        if self.num_rails <= 1:
            return text

        rail = ['' for _ in range(self.num_rails)]
        rail_idx = 0
        direction = 1  # 1: down, -1: up

        for char in text:
            rail[rail_idx] += char
            rail_idx += direction

            if rail_idx == 0 or rail_idx == self.num_rails - 1:
                direction *= -1

        return ''.join(rail)

    def decrypt(self, ciphertext):
        if self.num_rails == 1:
            return ciphertext

        rail = [[None for _ in range(len(ciphertext))] for _ in range(self.num_rails)]
        dir_down = None
        row, col = 0, 0

        # Mark positions
        for i in range(len(ciphertext)):
            if row == 0:
                dir_down = True
            elif row == self.num_rails - 1:
                dir_down = False

            rail[row][col] = True
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        # Fill rail matrix
        index = 0
        for i in range(self.num_rails):
            for j in range(len(ciphertext)):
                if rail[i][j] == True:
                    rail[i][j] = ciphertext[index]
                    index += 1

        # Read the matrix
        result = []
        row, col = 0, 0
        for i in range(len(ciphertext)):
            if row == 0:
                dir_down = True
            elif row == self.num_rails - 1:
                dir_down = False

            if rail[row][col] is not None:
                result.append(rail[row][col])
                col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        return ''.join(result)

class CombinedCipher(Cipher):
    def __init__(self, shift=3, num_rails=3):
        self.caesar_cipher = CaesarCipher(shift)
        self.rail_fence_cipher = RailFenceCipher(num_rails)

    def encrypt(self, text):
        shifted_text = self.caesar_cipher.encrypt(text)
        return self.rail_fence_cipher.encrypt(shifted_text)

    def decrypt(self, text):
        rail_decrypted = self.rail_fence_cipher.decrypt(text)
        return self.caesar_cipher.decrypt(rail_decrypted)
