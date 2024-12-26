import re
from nltk.tokenize import word_tokenize
from extraction import *

# Creating a master dictionary which contains all positive and negative words.
MasterDictionary = {'positive' : set(), 'negative': set()}

for sentiment in ['positive', 'negative']:
    with open(f'MasterDictionary/{sentiment}-words.txt', 'r') as f:
        for word in f:
            # The word should not exist in the stop words list.
            if word not in stop_words:
                MasterDictionary[sentiment].add(word.replace('\n', ''))

def count_syllable_heuristic(word):
    # Counting syllables in a word with a self made function in case the word is not in the nltk dictionary.
    # Usually, a word has as many syllables as the number of 'vowel groups' in it.
    syllable_count = 0
    word = word.lower()
    vowels = 'aeiouy'
    for index in range(len(word)):
        if index == 0:
            continue
        else:
            if word[index] in vowels and word[index-1] not in vowels:
                syllable_count += 1
    if word.endswith("e") or word.endswith('es') or word.endswith('ed'):
        # If the word ends with e, that does not contribute to another vowel.
        syllable_count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllable_count +=1
    if syllable_count == 0:
        syllable_count += 1
    if word[0] in vowels:
        syllable_count += 1
    return syllable_count

def count_syllable(word):
    try:
        word_lower = word.lower()
        if word_lower in d:
            pronunciations = d[word_lower]
            for pronunciation in pronunciations:
                syllable_count = 0
                for phoneme in pronunciation:
                    if phoneme[-1].isdigit():
                        syllable_count += 1
            return syllable_count
        else:
            # Raise an error if the word is not in dictionary so that we can manually find the number of syllables.
            raise KeyError
    except KeyError:
        return count_syllable_heuristic(word)

def analyse_text(filename):

    global MasterDictionary, stop_words

    # Extracting text.
    with open(f'ArticlesTextFiles/{filename}.txt', 'r', encoding= 'utf-8') as f:
        original_text = f.read()

    # Cleaning it by removing stop words.
    cleaned_text = ''
    for sentence in original_text.lower().split('\n'):
        for word in sentence.split():
            if word.lower() not in stop_words:
                cleaned_text += word + " "
        cleaned_text += '\n'

    # Extracting lists of words and sentences from the cleaned text.
    words = [word for word in word_tokenize(cleaned_text) if len(word) > 1]  # To avoid counting symbols such as .,!?
    sentences = list(filter(None,cleaned_text.split('\n'))) # Initially, seperated on the basis of new line.
    for sentence in sentences:
            # Further seperates sentences on period.
            if '. ' in sentence:
                sentences.extend(sentence.split('. '))
                sentences.remove(sentence)

    # Initializing and declaring useful variables.
    pos_score = 0
    neg_score = 0
    character_count = 0
    complex_words_count = 0
    total_syllables = 0
    personal_pronouns_count = 0

    personal_pronouns = ['\b[Ii]\b', '\b[Yy]ou\b', '\b[Hh]e\b', '\b[Ss]he\b', '\b[Ii]t\b', '\b[Ww]e\b', '\b[Tt]hey\b', '\b[Mm]e\b', '\b[Hh]im\b', '\b[Hh]er\b', '\b[Uu]s\b', '\b[Tt]hem\b', '\b[Mm]y\b', '\b[Yy]our\b', '\b[Hh]is\b', '\b[Ii]ts\b', '\b[Oo]ur\b', '\b[Tt]heir\b', '\b[Mm]yself\b', '\b[Yy]ourself\b', '\b[Hh]imself\b', '\b[Hh]erself\b', '\b[Ii]tself\b', '\b[Oo]urselves\b', '\b[Yy]ourselves\b', '\b[Tt]hemselves\b']

    # Calculation of different metrics.
    for word in words:
        if word.isalnum():
            if word in MasterDictionary['positive']:
                pos_score += 1
            if word in MasterDictionary['negative']:
                neg_score += 1
            for letter in word:
                character_count += 1
            total_syllables += count_syllable(word)
            if count_syllable(word) > 2:
                complex_words_count += 1
    
    for pronoun in personal_pronouns:
        matches = re.findall(pronoun, original_text)
        personal_pronouns_count += len(matches)

    polarity_score = round((pos_score - neg_score)/((pos_score + neg_score) + 0.000001),2)
    subectivity_score = round((pos_score + neg_score)/((len(words)) + 0.000001), 2)
    avg_sentence_length = round((character_count/len(sentences)), 2)      
    percentage_of_complex = round((complex_words_count/len(words))*100,2)    
    fog_index = round(0.4*(avg_sentence_length + percentage_of_complex),2)
    avg_no_of_words = round(len(words)/len(sentences),2)
    word_count = len(words)
    syllable_count_per_word = round(total_syllables/len(words),2)
    avg_word_length = round(character_count/len(words),2)
    
    row = [filename, urls.loc[urls['URL_ID'] == filename, 'URL'].values[0], pos_score, neg_score, polarity_score, subectivity_score, avg_sentence_length, percentage_of_complex, fog_index, avg_no_of_words, complex_words_count, word_count, syllable_count_per_word, personal_pronouns_count, avg_word_length]

    return row

# Creating a final dataset with all metrics against their respective url and url id.
output_dataset = []

for url_id in urls['URL_ID']:
    output_dataset.append(analyse_text(url_id))

columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
output_dataset = pd.DataFrame(output_dataset, columns = columns)

# Exporting the dataset to an excel file.
output_dataset.to_excel('final_output.xlsx', index=False)
