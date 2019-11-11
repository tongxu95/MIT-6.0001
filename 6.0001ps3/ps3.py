# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    # 'r' is short for read, 'w' is short for write
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    #split(): The function can take one or no parameter. 
    #If no parameter is passed then only the leading and trailing spaces are removed
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    #dict.get(key,default value): returns the value for key if key is in the dictionary, else it
    #returns the default value (None by default). "Safe" way to access the value of a key when we
    #are not sure if the key is in the dictionary (using dict['key'] when the key is not 
    #available will result in KeyError)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    input_word = word.lower()
    score_comp_1 = 0
    for i in input_word:
        score_comp_1 += SCRABBLE_LETTER_VALUES.get(i,0)
    score_comp_2 = 7*len(input_word)-3*(n-len(input_word))
    if score_comp_2 >= 1:
        score = score_comp_1 * score_comp_2
    else:
        score = score_comp_1 * 1
    return(score)



#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line



#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    i.e. n=7, ceil(n/3)=ceil(2.333)=3

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    #Each hand dealt should initially contain exactly one wildcard (denote '*') as one of its 
    #letters. Replace one of the vowel slots with the wildcard.
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    hand['*'] = 1
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand



#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #When you assign dict2 = dict1 , you are not making a copy of dict1 , dict2 is an alias 
    #(another name) for dict1 . To copy the mutable types like list or dictionaries, use 
    #dict2 = dict1.copy()
    new_hand=hand.copy()
    for letter in word.lower():
        if letter in hand:
            new_hand[letter]=new_hand.get(letter,0)-1
    return new_hand



#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    #hand and word_list are lowercased strings, while word may be upper or lowercased strings
    
    #need to update hand (Does NOT assume that hand contains every letter in word at least as
    #many times as the letter appears in word.
    
    #update_hand(hand,word) is defined such that even if the word contains a letter more times
    #than the hand, the function updates to 0 (does not delete the key)
    
    #Wildcard can be used to replace a vowel. We do not know if the player will use the wildcard
    #or the index of the wildcard if they chose to use it, so we use find() which will return the
    #index of the first occurrance the substring. If not found, it returns -1
    lowercase_word = word.lower()
    new_hand = hand.copy()
    for letter in lowercase_word:
        if letter not in new_hand or new_hand[letter] == 0:
            return False
        else:
            new_hand = update_hand(new_hand, letter)
    if word.find('*') == -1 and lowercase_word not in word_list:
        return False
    if word.find('*') != -1:
        wildcard_word = lowercase_word
        attempts = len(VOWELS) 
        for vowel in VOWELS:
            wildcard_word = lowercase_word.replace('*',vowel)
            if wildcard_word in word_list:
                break
            attempts -= 1
            if attempts == 0:
                return False
    return True



#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    len = 0
    for letter in hand:
        len += hand[letter]
    return len



def play_hand(hand, word_list):

 
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    

    # Keep track of the total score
    score = 0
    # As long as there are still letters left in the hand:
    while sum(hand.values()) > 0:
        # Display the hand
        print('Current Hand: ')
        display_hand(hand)
        
        # Ask user for input
        word = input ('Enter word, or "!!" to indicate that you are finished: ')   
        
        # If the input is two exclamation points:
        if word == '!!':
            
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                
                # Tell the user how many points the word earned,
                score += get_word_score(word, sum(hand.values()))
                print('"'+word+'"', 'earned', get_word_score(word, sum(hand.values())), 'points.')
                
                # and the updated total score
                print('Total:', score, 'points')
                
            # Otherwise (the word is not valid):
            else:
                
                # Reject invalid word (print a message)
                print('That is not a valid word. Please chose another word.')
                
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    print('Total score for this hand:', score, 'points')
    
    # Return the total score as result of function
    return score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    #check if letter is in the hand
    if letter in hand:
           
        #create a new copy of the hand
        new_hand = hand.copy()
        
        #determine the occurrance of letter in hand
        i = hand[letter]
        
        #delete letter from copy
        del(new_hand[letter])
        
        #chose a letter at random from vowels and consonants
        x = random.choice(VOWELS + CONSONANTS)
        
        #while new letter is in hand
        while x in hand:
            
            #chose a new letter at random from vowels and consonants
            x = random.choice(VOWELS + CONSONANTS)

        #for the number of occurrances of the letter,
        while i > 0:
                
            #add new letter to hand
            new_hand[x] = hand.get(x,0) + 1
            
            #reduce number of occurrance by 1
            i -= 1
                
        return new_hand    
        
    #if letter is not in hand, return the original hand
    else:
        return hand
    
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    #ask user to input the number of hand
    num_hand = int(input('Enter total number of hands: '))
    #for the number of hand
    for i in range (num_hand):    
        #initialize total score
        total_score = 0
        #initialize number of substitution as 1
        num_of_sub = 1
        #initialize hand
        hand = {}
        #deal a random set of letters in hand using deal_hand(n)
        hand = deal_hand(HAND_SIZE)
        #display hand using display_hand(hand)
        print('Current hand:')
        display_hand(hand)
        #while number of substitution > 0
        while num_of_sub > 0:
            #ask user if they would like to substitute one letter for another
            sub_letter = input('Would you like to substitute a letter?')
            #if user answered 'yes'
            if sub_letter == 'yes' or sub_letter == 'Yes' or sub_letter == 'YES':
                #ask user what letter they would like to substitute
                letter_to_replace = input('Which letter would you like to replace?')
                #substitute letter using substitute_hand(hand,letter), return new hand
                hand = substitute_hand(hand,letter_to_replace)
                #reduce number of subsitution by 1
                num_of_sub -= 1
            #if user answered 'no', break
            if sub_letter == 'no' or sub_letter == 'No' or sub_letter =='NO':
                break
        #play hand using play_hand(hand, word_list); return score of hand
        score = play_hand(hand,word_list)
        #ask player if they would like to replay hand
        replay = input('Would you like to replay the hand?')
        #if player answered 'yes'
        if replay == 'yes' or replay == 'Yes' or replay =='YES':
            #play hand using play_hand(hand, word_list); return score of hand
            score = play_hand(hand,word_list)
        #add score to total score
        total_score += score
        
    #print total score for all hands
    print ('Total score over all hands:', total_score)




#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


