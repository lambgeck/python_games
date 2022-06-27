#! python3

import random
import os
import time
import sys

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''','''
  +---+
  O   |
 /|\  |
 /    |
     ===''','''
  +---+
  O   |
 /|\  |
 / \  |
     ===''','''
  +---+
 [O   |
 /|\  |
 / \  |
     ===''','''
  +---+
 [X]  |
 /|\  |
 /:\  |
  :  ===''']

words = {'Colors': 'red orange yellow green blue indigo violet white black brown'.split(),
         'Shapes': 'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon octagon'.split(),
         'Fruits': 'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
         'Animals': 'bat bear beaver cat cougar crab deer dog donkey duck eagle fish frog goat leech lion lizard monkey moose mouse otter owl panda python rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf wombat zebra'.split()}

def get_random_word(word_dict):
    # This function returns a random string from the passed dictionary of list of strings and its key.
    # 1st, randomly select a key from the dictionary:
    word_key = random.choice(list(word_dict.keys()))

    # 2nd, randomly select a word from the key's list in the dictionary:
    word_index = random.randint(0, len(word_dict[word_key]) - 1)
    return [word_dict[word_key][word_index], word_key]

def display_board(missed_letters, correct_letters, secret_word):
    #os.system('cls')
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print('Missed letters:', end= ' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)):  # Replace blanks with correctly guessed letters.
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks:  # Show the secret word with spaces in between each letter
        print(letter, end=' ')
    print()

def get_guess(already_guessed):
    # Returns the letter the player entered.
    # This function makes sure the player entered a single letter and not something else.
    while True:
        print(f'The number of letters in the word is above. Guess a letter!')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def play_again():
    # This function returns True if the player wants to play again and False if not.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        time.sleep(.2)

# Beginning of Game
print_slow('- H A N G M A N -')

difficulty = 'X'
while difficulty not in ['E', 'M', 'H']:
    print('\nEnter difficulty: E)asy, M)edium, or H)ard')
    difficulty = input().upper()
if difficulty == 'M':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
if difficulty == 'H':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
    del HANGMAN_PICS[5]
    del HANGMAN_PICS[3]

missed_letters = ''
correct_letters = ''
secret_word, secret_set = get_random_word(words)
game_is_over = False

while True:
    print(' - - - - - - - - - - - - - - - - - - - ')
    print(f'*The word category is: {secret_set}')
    display_board(missed_letters, correct_letters, secret_word)

    # Let the player enter a letter.
    guess = get_guess(missed_letters + correct_letters)

    if guess in secret_word:
        correct_letters = correct_letters + guess

        # Check if the player has won.
        found_all_letters = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                found_all_letters = False
                break
        if found_all_letters:
            print(f'Yes! The secret word is {secret_word}! You won!')
            game_is_over = True

    else:
        missed_letters = missed_letters + guess

        # Check if player has guessed to many times and has lost.
        if len(missed_letters) == len(HANGMAN_PICS) - 1:
            display_board(missed_letters, correct_letters, secret_word)
            print(f'You have run out of guesses!\nAfter {len(missed_letters)} missed guesses and {len(correct_letters)} correct guesses, the word was "{secret_word}".')
            game_is_over = True

    # Ask the player if they want to play again (but only if the game is done).
    if game_is_over:
        if play_again():
            missed_letters = ''
            correct_letters = ''
            game_is_over = False
            secret_word, secret_set = get_random_word(words)
        else:
            break
