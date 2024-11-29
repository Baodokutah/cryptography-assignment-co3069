import string
import re
# source: https://en.wikipedia.org/wiki/Most_common_words_in_English
common_words = set([
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
    'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
    'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
    'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
    'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
    'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
    'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
    'give', 'day', 'most', 'us'
])

def english_score(text):
    # source: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/
    frequencies = {
        'E': 12.10, 'T': 8.94, 'A': 8.55, 'O': 7.47, 'I': 7.33, 'N': 7.17,
        'S': 6.73, 'R': 6.33, 'H': 4.96, 'L': 4.21, 'D': 3.87, 'C': 3.16,
        'U': 2.68, 'M': 2.53, 'F': 2.18, 'G': 2.09, 'P': 2.07, 'W': 1.83,
        'Y': 1.72, 'B': 1.60, 'V': 1.06, 'K': 0.81, 'J': 0.22, 'X': 0.19,
        'Z': 0.11, 'Q': 0.10 
    }
    text_upper = text.upper()
    text_letters = [c for c in text_upper if c in string.ascii_uppercase]
    if not text_letters:
        letter_score = 0
    else:
        letter_counts = {char: text_letters.count(char) for char in string.ascii_uppercase}
        letter_score = sum(frequencies.get(char, 0) * count for char, count in letter_counts.items())
        letter_score /= len(text_letters)
    
    words_in_text = re.findall(r'\b\w+\b', text.lower())
    if not words_in_text:
        word_score = 0
    else:
        valid_words = sum(1 for word in words_in_text if word in common_words)
        word_score = valid_words / len(words_in_text)
    
    combined_score = (letter_score * 0.3) + (word_score * 0.7)
    return combined_score
