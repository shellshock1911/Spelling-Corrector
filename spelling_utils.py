# -*- coding: utf-8 -*-

"""Set of helper functions for spelling_correct.py"""

# Allow compatibility between Python 2.7 and 3.5
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import open 
#####

import re # Used to parse texts
import pickle # Packs and unpacks pre-stored Python objects
import sys # Checks users Python version
import string # Contains lists of useful English characters
import autocorrect # autocorrect.spell(word) used as core correcting algorithm

# Create log file path
LOG_FILE = 'correct_log.txt'

# Check for Python 3.x
if sys.version_info.major == 3:
    # Unpack set of 236,055 valid english words
    # Derived from nltk.corpus.words.words()
    with open('pkl_objects/3_x/english_words.pkl', 'rb') as words_handle:
        ENGLISH_WORDS = pickle.load(words_handle)  
    # Unpack 2,167 misspelled versions of English words along with corresponding
        # correct forms (stored as a dictionary)
    with open('pkl_objects/3_x/common_misspellings.pkl', 'rb') as common_handle:
        COMMON_MISSPELLINGS = pickle.load(common_handle)

# Check for Python 2.7. 
if sys.version_info.major == 2:
    # Unpack set of 236,055 valid english words
    # Derived from nltk.corpus.words.words()
    with open('pkl_objects/2_7/english_words.pkl', 'rb') as words_handle:
        ENGLISH_WORDS = pickle.load(words_handle)  
    # Unpack 2,167 misspelled versions of English words along with corresponding
        # correct forms (stored as a dictionary)
    with open('pkl_objects/2_7/common_misspellings.pkl', 'rb') as common_handle:
        COMMON_MISSPELLINGS = pickle.load(common_handle)
    
def str_to_bool(option):
    
    """Converts True and False option strings to booleans."""
    
    if option == 'True': # String
        return True # Boolean
    elif option == 'False': # String
        return False # Boolean
    else: # Cannot proceed if values other than True or False are passed
        raise ValueError("Options can only be True or False")

def read_input(input_file):
    
    """Reads input file and prepares text for spelling correction."""
    
    # Read in input file into a string 
    with open(input_file, 'r', encoding='utf-8') as input_handle:
        passage = input_handle.read()
            
    # Split passage into words, whitespace, and punctuation tokens
    split_passage = re.findall(r'\w+|\s|[{}]'.format(
        string.punctuation), passage)
    
    # Return split passage to main function in spelling_correct.py
    return split_passage

def _is_a_misspelling(token):
    
    """Differentiates word tokens from non-word tokens"""
    
    # Ignore token if a number, punctuation, whitespace, etc.
    if not token.isalpha():
        return False
    # Ignore if token begins with capital letter
    # Could be name of person, place, company, etc.
    elif token.istitle():
        return False
    # Ignore if token is in English dictionary
    # Doesn't need to be corrected
    elif token in ENGLISH_WORDS:
        return False
    # Otherwise, correction is needed
    # True will be returned at this point
    return True
        
def correct_spelling(tokens, logging, current_input):
    
    """Core spell correction process"""
    
    # Hold corrected words that will be output to log
    log_words = []
    # Check each word in text for possible misspelling
    for i, token in enumerate(tokens): 
        if _is_a_misspelling(token):
            # Check if word is commonly misspelled
            if token in COMMON_MISSPELLINGS:
                corrected = COMMON_MISSPELLINGS[token]
            else:
                # Otherwise, attempt correcting algorithm 
                corrected = autocorrect.spell(token)
            # Replace with correct word if token differs from prediction
            if token != corrected:
                tokens[i] = corrected
                # Log original word, corrected word, and source file
                if logging:
                    log_words.append(
                        '{}'.format(token) + '\t' + '>>>' \
                        + '\t' + '{}'.format(corrected) \
                        + '\t' + '|' + '\t' + 'Source: {}'.format(current_input))
    
    # Rebuild passage from new tokens
    rebuilt_passage = ''.join(tokens)
    
    # Continuously append log info. to log file
    if log_words:
        with open('{}'.format(LOG_FILE), 'a', encoding='utf-8') as log_handle:
            log_handle.writelines(log_word + '\n' for log_word in log_words)
    
    # Return rebuilt passage to main function in spelling_correct.py
    return rebuilt_passage
            