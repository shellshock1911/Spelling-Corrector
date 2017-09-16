#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script automates word spelling correction over one or more
text files. The algorithm that identifies and corrects a misspelled
word is quite computationally expensive, therefore runtime can be
slow. Expect 3 to 5 minutes per 1000 text files. Run the following
at the Terminal prompt to get started for Python 2.7:
    
    $ python spelling_correct.py --input test_batch_input --logging True
    
       or (for Python 3.x)
       
    $ python3 spelling_correct.py --input test_batch_input --logging True

Although this script does a generally good job, given the complexity of 
language, no spell corrector can obtain perfect accuracy for all texts. 
To compensate for this to some degree, there is a --logging option
included that can be passed at script call. After a successful run, the 
user can eyeball the logs that are generated in correct_log.txt to get a 
transparent understanding of where misspelled words were found and how they 
were corrected. Particulary bad mistakes may need to be hand-corrected.
This log file will never be overwritten, so if you want to start fresh, delete
it manually. A new one will automatically be created on the next run.

The core spell correcting function requires the Python autocorrect package.
In order to install this in your current environment, input the following at
your Terminal prompt:
    
    $ pip install autocorrect

For more details on this package see:
    
    > https://pypi.python.org/pypi/autocorrect/0.2.0 --- (Package host)
    > https://github.com/phatpiglet/autocorrect/ --- (Source repository)
    > http://norvig.com/spell-correct.html --- (Theoretical basis)

-------------------------------

Current issues to be aware of :
    
    1.) Capitalized words are ignored entirely. This was done so that
        that names of people, places, events, etc., don't get attempt
        getting respelled.
        
            *** Trying to fix this issue would likely cause even worse issues
        
    2.) Misspelled words can be handled, however grammar errors and/or 
        incorrectly used words cannot be. "Loss" in the sentence -
        "I always loss my keys." would not be respelled as "lose",
        although that is the correct word to use in that context.
        
            *** Fixing this issue is out of the scope of this task.
        
    3.) Context around words is not considered, so all the words in "John 
        wanted to buy some peanut" would be considered correctly spelled,
        even though a person would want to change "peanut" to "peanuts".
        
            *** Fixing this issue is out of the scope of this task.
        
    4.) Two (otherwise correctly spelled) words that are not separated by 
        spaces cause major issues. If the corrector encounters "toprepare" 
        for example, it will respell it as "prepare", although one can clearly 
        see it should be "to prepare". "perperson" becoming "perversion" is a 
        particularly bad mistake. 
        
            *** Working on handling this using regex.
        
    5.) URLs and email addresses are troublesome because they are typically
        presented entirely in lowercase and involve names of people, places
        events, companies, etc. 
        
            *** Working on handling this using regex.

"""

# Allow compatibility between Python 2.7 and 3.5
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import open
#####

import glob # Allows batch input file fetching
import os   # Allows convenient file handling
import time # Calculates script runtime
import spelling_utils # Collection of helper functions in the utils file

# Allows parsing of user-specified options at script call
from optparse import OptionParser 

# Initialize parser, then adds arguments. Input is required, 
PARSER = OptionParser()

PARSER.add_option('-i', '--input', dest='input_directory',
                  help='input directory with files that need spelling corrections')
PARSER.add_option('-l', '--logging', dest='logging', default="False",
                  help='log words that were caught and corrected')
PARSER.add_option('-v', '--verbose', dest='verbose', default="True",
                  help='toggle console output')

OPTIONS, _ = PARSER.parse_args() # Convert options into usable strings

# Load user options into global constants for use in the script
INPUT_DIR = OPTIONS.input_directory # Directory containing input files (required)
LOGGING = OPTIONS.logging # Logs original and correct words in corrected_log.txt
VERBOSE = OPTIONS.verbose # Display console output (optional)

# Ensure input directory exists, otherwise the script exits
assert os.path.isdir(INPUT_DIR), \
        "The input directory doesn't exist in the working directory"

# Default name for output directory, change if needed
OUTPUT_DIR = 'corrected_output'  
# Check if output directory exists, otherwise create one
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)  
    
##### Main Function #####
def spelling_corrector(input_dir, logging='False', verbose='True'):
    """Takes an input directory and processes all .txt files within, attempting
    to replace all misspelled words with their correctly spelled counterparts.
    Outputs to a separate directory new files where structure and content of 
    original text is preserved, albiet with as few spelling errors as possible.
    
    `input_dir` = name of directory that contains input .txt files
    `logging` = logs all instances of misspelled words with correct versions
    `verbose` = toggles console output (default True)
        
    """
    start_time = time.time() # Start runtime
    
    # Set verbose and logging flags for use throughout
    logging = spelling_utils.str_to_bool(logging)
    verbose = spelling_utils.str_to_bool(verbose)

    # Initialize generator that fetches input files one by one
    input_fetcher = glob.iglob('{}/*.txt'.format(input_dir))
    
    # Script begins
    if verbose:
        print("\n------------------------------\n"
              "Spelling correction starting\n"
              "------------------------------\n")
    
    attempted_files = 0 # Track how many files attempted conversion
    completed_files = 0 # Track how many files converted successfully
        
    # Main loop that batch processes input files 
    while input_fetcher:
        try:
            current_input = next(input_fetcher) # Fetch next input file
        except StopIteration:
            break # Execute when there are no more files to fetch
    
        # Create a path for the output file in the output directory
        # Flag each output file with '--CORRECTED', indicating that any
            # spelling errors have been found and corrected
        current_output = os.path.join(OUTPUT_DIR, '{0}--CORRECTED{1}'.format(
            *os.path.splitext(os.path.basename(current_input))))
        
        attempted_files += 1 # Increment prior to processing

        # Split text into list of complete words, whitespace, and punctuation
        split_passage = spelling_utils.read_input(current_input)
        
        # Check input to ensure that each file contains content before sending 
            # to parser. Skip and log files that don't meet this criteria
        if not split_passage:
            # Display bad input file
            if verbose:
                print("* ".rjust(2) + "No text was found in {}. "
                      "Nothing to convert.".format(current_input))
                
        # Rebuild text with any spelling errors corrected
        rebuilt_passage = spelling_utils.correct_spelling(
            split_passage, logging, current_input)
        
        # Write new passage to file in output directory at the path
            # specified in current_output variable
        with open(current_output, 'w', encoding='utf-8') as file_handle:
            file_handle.write(rebuilt_passage)
        # Display where current output file is located on the local file system
        if verbose:
            print("*".rjust(5), "\t", current_input, ">>>", current_output)

        # Increment upon successful processing of current input file
        completed_files += 1

    # Main loop ends
    end_time = time.time() # Runtime ends
        
    # Output Report
    if verbose:
        print("\n--------------------------------------------\n"
              "Conversion complete\n"
              "{0} of {1} files converted in {2} minutes\n"
              "--------------------------------------------\n".format(
                  completed_files, attempted_files, round((
                      end_time - start_time) / 60, 3)))
        
    # Exit
    return

# Standard code that allows the file to be run as a script from the terminal   
if __name__ == '__main__':
    spelling_corrector(INPUT_DIR, logging=LOGGING, verbose=VERBOSE)
