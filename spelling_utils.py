# -*- coding: utf-8 -*-

"""Set of helper functions for spelling_corrector.py"""

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
    
    """Reads input file and prepares text for name replacing."""
    
    # Read in input file into a string 
    with open(input_file, 'r', encoding='utf-8') as input_handle:
        passage = input_handle.read()
            
    # Split passage into words, whitespace, and punctuation tokens
    split_passage = re.findall(r'\w+|\s|[{}]'.format(
        string.punctuation), passage)
    
    # Return split passage to main function in spelling_correct.py
    return split_passage

def _is_a_word(token):
    
    """Differentiates word tokens from non-word tokens"""
    
    # Ignore if token is a non-alphabetical string, e.g. numbers, punctuation, etc.
    if not token.isalpha():
        return False
    # Ignore if token is whitespace, e.g. space, tab, newline, ec.
    elif token in string.whitespace:
        return False
    # Otherwise, token must be a word
    else:
        return True
        
def correct_spelling(tokens, logging, current_input):
    
    """Core spell correction process"""
    
    # Hold corrected words that will be output to log
    log_words = []
    # Check each word in text for possible misspelling
    for i, token in enumerate(tokens): 
        # Ignore token if a number, punctuation, whitespace, etc.
        if _is_a_word(token):
            # Don't proceed if word exists in English dictionary
            # No correction needed
            if token in ENGLISH_WORDS:
                continue
            # Check if word is a commonly misspelled one
            # Can map to the correct word before attempting the autocorrect algorithm
            if token in COMMON_MISSPELLINGS:
                # Log original word, corrected word, and source file if user requests
                if logging:
                    log_words.append(
                        '{}'.format(token) + '\t' + '>>>' \
                        + '\t' + '{}'.format(COMMON_MISSPELLINGS[token]) \
                        + '\t' + '|' + '\t' + 'Source: {}'.format(current_input))
                # Map and replace with correct word
                tokens[i] = COMMON_MISSPELLINGS[token]
            # Attempt correcting algorithm    
            else:
                corrected = autocorrect.spell(token)
                # Make sure corrected word differs from original word
                # Filter out words that begin with capital letter(s) (could be names)
                if corrected != token and token[0] not in string.ascii_uppercase:
                    # Log original word, corrected word, and source file if user requests
                    if logging:
                        log_words.append(
                            '{}'.format(token) + '\t' + '>>>' \
                            + '\t' + '{}'.format(corrected) \
                            + '\t' + '|' + '\t' + 'Source: {}'.format(current_input))
                    # Replace with correct word that autocorrect algorithm predicts
                    tokens[i] = corrected
        else:
            # Executes early if token is not a word
            continue
    
    # Rebuild passage from new tokens
    rebuilt_passage = ''.join(tokens)
    
    # Continuously append log info. to log file
    if log_words:
        with open('{}'.format(LOG_FILE), 'a', encoding='utf-8') as log_handle:
            log_handle.writelines(log_word + '\n' for log_word in log_words)
    
    # Return rebuilt passage to main function in spelling_correct.py
    return rebuilt_passage
            