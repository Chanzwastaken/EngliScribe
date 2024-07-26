from spellchecker import SpellChecker
import re

spell = SpellChecker()

def preprocess_data(text):
    text = text.lower()
    text = text.replace("\n"," ").replace("\t"," ")
    text = re.sub("\s+"," ",text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def booleans_spell(text):
    splitted_ori_text = text.split()
    cleaned_words = preprocess_data(text)
    words = cleaned_words.split()
    list_of_booleans = [word in spell for word in words]
    return splitted_ori_text, list_of_booleans

# def preprocess_data_for_correct(text):
#     # Example preprocessing function, can be adjusted as needed
#     cleaned_text = text.lower()  # Convert to lowercase for processing
#     cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation
#     return cleaned_text

def correct_text_using_spellchecker(text):
    def preserve_case(original, corrected):
        if original.isupper():
            return corrected.upper()
        elif original.istitle():
            return corrected.title()
        else:
            return corrected
    
    # Use regex to find words and their positions in the original text
    words_with_positions = list(re.finditer(r'\w+|\W+', text))
    corrected_words = []
    
    for match in words_with_positions:
        original_word = match.group()  # Get the matched word or punctuation
        
        if original_word.isalpha():  # Check if it's a word (not punctuation)
            word = original_word.lower()
            corrected_word = spell.correction(word)
            corrected_words.append(preserve_case(original_word, corrected_word) if corrected_word is not None else '<unknown>')
        else:
            corrected_words.append(original_word)  # Preserve punctuation or non-word characters
    
    return ''.join(corrected_words)

def correction_and_accuracy(input_text):
    # Assuming booleans_spell and other parts are defined elsewhere
    splitted_words, list_of_booleans_from_word_checking = booleans_spell(input_text)
    total_words = len(list_of_booleans_from_word_checking)
    correctly_corrected = sum(list_of_booleans_from_word_checking)
    accuracy = correctly_corrected / total_words * 100
    
    if accuracy != 100:
        corrected_text = correct_text_using_spellchecker(input_text)
    else:
        corrected_text = input_text
        
    return accuracy, corrected_text, splitted_words, list_of_booleans_from_word_checking

# def correct_text_using_spellchecker(text):
#     cleaned_words = preprocess_data(text)
#     words = cleaned_words.split()
#     corrected_words = [spell.correction(word) if spell.correction(word) is not None else '<unknown>' for word in words]
#     if len(corrected_words) > 1:
#         return ' '.join(corrected_words)
#     elif len(corrected_words) == 1:
#         return corrected_words[0]
#     else:
#         return ''

# def correction_and_accuracy(input_text):
#     splitted_words, list_of_booleans_from_word_checking = booleans_spell(input_text)
#     total_words = len(list_of_booleans_from_word_checking)
#     correctly_corrected = sum(list_of_booleans_from_word_checking)
#     accuracy = correctly_corrected / total_words * 100
#     if accuracy != 100:
#         corrected_text = correct_text_using_spellchecker(input_text)
#     else:
#         corrected_text = input_text
#     return accuracy, corrected_text, splitted_words, list_of_booleans_from_word_checking

def highlighting_words(splitted_words, list_of_booleans_from_word_checking):
    highlighted_text = ''
    for i, word in enumerate(splitted_words):
        if i < len(list_of_booleans_from_word_checking) and not list_of_booleans_from_word_checking[i]:
            highlighted_text += f'<span class="highlight">{word}</span> '
        else:
            highlighted_text += word + ' '
    return highlighted_text.strip()
