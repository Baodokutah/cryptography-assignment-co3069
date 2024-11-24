# scoring.py

import string
import re

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
    # Add more words or use a dictionary file
])

def english_score(text):
    frequencies = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
        'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
        'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
        'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
        'Q': 0.10, 'Z': 0.07
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
    
    combined_score = (letter_score * 0.3) + (word_score * 70)
    return combined_score
