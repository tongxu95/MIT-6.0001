# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    '''
    This code only returns true if all letters, including repetition in secret_word
    are accounted for in letters_guessed


    copy_letters_guessed = letters_guessed[:]
    for char in secret_word:
        if char in letters_guessed:
            letters_guessed.remove(char)
    if len(secret_word)== len(copy_letters_guessed) - len(letters_guessed):
         return True
    else:
         return False
    '''
    
    '''
    This code will return true if all unique letters in secret_word in accounted for in letters_
    guessed.
    '''
    
    for char in secret_word:
        if char not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for char in secret_word:
        if char not in letters_guessed:
            guessed_word += '_ '
        else:
            guessed_word += char
    return guessed_word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    available_letters = ''
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            available_letters += char
    return available_letters
            
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guess=6
    warning=3
    vowels = 'aeiou'
    letters_guessed = []
    print ('Welcome to the game Hangman!')
    print ('I am thinking of a word that is', len(secret_word),'letters long.')
    print ('You have', warning, 'warnings left')
    print ('------------')
    while guess>0 and is_word_guessed(secret_word, letters_guessed) == False :
        print('You have', guess, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        user_guess = str.lower(input('please guess a letter:\n'))
        is_char_valid = user_guess.isalpha()
        is_letter_already_guessed = user_guess in letters_guessed
        if is_char_valid == False:
            if warning > 0:
                warning -= 1
                print('Oops! That is not a valid letter. You now have', warning, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
                print ('------------')
            else:
                guess -= 1
                print('Oops! This is not a valid letter. You have no warning left so you lose one guess：',get_guessed_word(secret_word, letters_guessed))
                print ('------------')
        elif is_letter_already_guessed == True:
            if warning > 0:
                warning -= 1
                print('Oops! You have already guessed that letter. You now have', warning, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
                print ('------------')
            else:
                guess -= 1
                print('Oops! You have already guessed that letter. You now have no warning left so you lose one guess',get_guessed_word(secret_word, letters_guessed))
                print ('------------')
        else:
            letters_guessed.append(user_guess)
            if user_guess in secret_word:
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
                print ('------------')
            else:
                if user_guess in vowels:
                    guess -= 2
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
                else:
                    guess -= 1
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
    if is_word_guessed(secret_word,letters_guessed)==True:
        print('Congratulations! You won!\n')
        unique_letter=''
        for char in secret_word:
            if char not in unique_letter:
                unique_letter += char
        score = guess*len(unique_letter)
        print ('Congratulations! You won!')
        print('Your score for this game is:', score)
    else:
        print ('Sorry, you ran out of guesses. The word is', secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    guessed_word = my_word.replace(' ','')
    if len(guessed_word) != len(other_word):
        return False
    for i in range(len(guessed_word)):
        if guessed_word[i] != '_' and guessed_word[i] != other_word[i]:
            return False
    return True




def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = []
    for other_word in wordlist:
        if match_with_gaps(my_word,other_word):
            possible_matches.append(other_word)
    print(possible_matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guess=6
    warning=3
    vowels = 'aeiou'
    letters_guessed = []
    print ('Welcome to the game Hangman!')
    print ('I am thinking of a word that is', len(secret_word),'letters long.')
    print ('You have', warning, 'warnings left')
    print ('------------')
    while guess>0 and is_word_guessed(secret_word, letters_guessed) == False :
        print('You have', guess, 'guesses left.')
        print('Available letters:', get_available_letters(letters_guessed))
        user_guess = str.lower(input('please guess a letter:\n'))
        is_char_valid = user_guess.isalpha()
        is_letter_already_guessed = user_guess in letters_guessed
        if is_char_valid == False:
            if user_guess == '*':
                print('Possible word matches are:',)
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            else:
                if warning > 0:
                    warning -= 1
                    print('Oops! That is not a valid letter. You now have', warning, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
                else:
                    guess -= 1
                    print('Oops! This is not a valid letter. You have no warning left so you lose one guess：',get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
        elif is_letter_already_guessed == True:
            if warning > 0:
                warning -= 1
                print('Oops! You have already guessed that letter. You now have', warning, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
                print ('------------')
            else:
                guess -= 1
                print('Oops! You have already guessed that letter. You now have no warning left so you lose one guess',get_guessed_word(secret_word, letters_guessed))
                print ('------------')
        else:
            letters_guessed.append(user_guess)
            if user_guess in secret_word:
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
                print ('------------')
            else:
                if user_guess in vowels:
                    guess -= 2
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
                else:
                    guess -= 1
                    print('Oops! That letter is not in my word.', get_guessed_word(secret_word, letters_guessed))
                    print ('------------')
    if is_word_guessed(secret_word,letters_guessed)==True:
        print('Congratulations! You won!\n')
        unique_letter=''
        for char in secret_word:
            if char not in unique_letter:
                unique_letter += char
        score = guess*len(unique_letter)
        print ('Congratulations! You won!')
        print('Your score for this game is:', score)
    else:
        print ('Sorry, you ran out of guesses. The word is', secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
