from ciphers import CaesarCipher, RailFenceCipher, CombinedCipher
from scoring import english_score

def caesar_brute_force(ciphertext, top_n=10):
    potential_texts = []
    for shift in range(26):
        cipher = CaesarCipher(shift)
        decrypted_text = cipher.decrypt(ciphertext)
        score = english_score(decrypted_text)
        potential_texts.append((score, shift, decrypted_text))
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]

def rail_fence_brute_force(ciphertext, top_n=10):
    potential_texts = []
    max_rails = min(30, len(ciphertext) // 2)
    for num_rails in range(2, max_rails + 1):
        cipher = RailFenceCipher(num_rails)
        decrypted_text = cipher.decrypt(ciphertext)
        score = english_score(decrypted_text)
        potential_texts.append((score, num_rails, decrypted_text))
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]

def combined_brute_force(ciphertext, top_n=10):
    potential_texts = []
    for shift in range(26):
        for num_rails in range(2, 30):
            try:
                cipher = CombinedCipher(shift, num_rails)
                decrypted_text = cipher.decrypt(ciphertext)
                score = english_score(decrypted_text)
                potential_texts.append((score, shift, num_rails, decrypted_text))
            except:
                continue
    potential_texts.sort(reverse=True)
    return potential_texts[:top_n]
