# Spelling Corrector

This script automates word spelling correction over one or more
text files. The algorithm that identifies and corrects a misspelled
word is quite computationally expensive, therefore runtime can be
slow. Expect 3 to 5 minutes per 1000 text files. Run the following
at the Terminal prompt to get started for Python 2.7:
    
    $ python2 spelling_correct.py --input test_batch_input --logging True

or (for Python 3.x)
       
    $ python3 spelling_correct.py --input test_batch_input --logging True

Although this script does a generally good job, given the complexity of 
language, no spell corrector can obtain perfect accuracy for all texts. 
To compensate for this to some degree, there is a --logging option
included that can be passed at script call. After a successful run, the 
user can eyeball the logs that are generated in correct_log.txt to get a 
transparent understanding of where misspelled words were found and how they 
were corrected. Particularly bad mistakes may need to be hand-corrected.
This log file will never be overwritten, so if you want to start fresh, delete
it manually. A new one will automatically be created on the next run.

The core spell correcting function requires the Python autocorrect package.
To install this in your current environment, input the following at
your Terminal prompt:
    
    $ pip install autocorrect

For more details on this package see:
    
- https://pypi.python.org/pypi/autocorrect/0.2.0 --- (Package host)
- https://github.com/phatpiglet/autocorrect/ --- (Source repository)
- http://norvig.com/spell-correct.html --- (Theoretical basis)

**Current Issues**
    
1.) Capitalized words are ignored entirely. This was done so that
    that names of people, places, events, etc., don't get attempt
    getting respelled.
        
2.) Misspelled words can be handled, however grammar errors and/or 
    incorrectly used words cannot be. "Loss" in the sentence -
    "I always loss my keys." would not be respelled as "lose",
    although that is the correct word to use in that context.
        
3.) Context around words is not considered, so all the words in "John 
    wanted to buy some peanut" would be considered correctly spelled,
    even though a person would want to change "peanut" to "peanuts".
        
4.) Two (otherwise correctly spelled) words that are not separated by 
    spaces cause major issues. If the corrector encounters "toprepare" 
    for example, it will respell it as "prepare", although one can clearly 
    see it should be "to prepare". "perperson" becoming "perversion" is a 
    particulary bad mistake. 
   
5.) URLs and email addresses are troublesome because they are typically
    presented entirely in lowercase and involve names of people, places
    events, companies, etc.
