import random

# main function to begin game and display everything to the user
def main():
    filename = input("Enter the name of the word file: ")
    play_game(filename)
    
# function to display rules
def rules():
    print("")
    print("========================================================================")
    print("                                 Rules                                  ")
    print("You have 6 guesses to figure out the solution.")
    print("All solutions are words that are 5 letters long.")
    print("Words may include repeated letters.")
    print("Letters that have been guessed correctly are displayed in uppercase.")
    print("Letters that are in the word but have been guessed in the wrong location")
    print("are displayed in lowercase.")
    print("========================================================================")
    print("")

# play game function to play the game that takes in one parameter, filename
def play_game(filename):
    # opens file
    word_file = open(filename, "r")
    # reads file and puts it into a list
    words = word_file.read().split()
    # closes file
    word_file.close()

    name = str(input("Please enter your name: "))

    print(f"\nWelcome to Wordle 101 {name}")
    
    rules()
    rounds(words)

# rounds function to determined the rounds played, rounds won and if the player was
# successful or not at completing the game.
def rounds(words):
    rounds_played = 0
    rounds_won = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    while True:
        # gets the list from the file
        word = get_random_word(words)
        print(f"\nRound: {rounds_played + 1}")
        print("")
        
        # gets the returned tuple from play round function
        guesses, success = play_round(word)
        
        # finds out if the player was successful or not
        if success:
            print(f"Success! The word is {word}!")
            rounds_won[guesses] += 1

        else:
            print(f"Better luck next time! The word is {word}!")

        rounds_played += 1
        print("")

        # asks user to play again or not, if not it breaks
        if not play_again():
            break

    # prints summary
    summary(rounds_won, rounds_played)

# play again function to ask user if they want to play again or not
def play_again():
    while True:
        play_again = input("Please enter 'Y' to continue or 'N' to stop playing: ")
        
        if play_again == "Y":
            return True

        if play_again == "N":
            return False
        
        print("Only enter 'Y' or 'N'!")

# summary function taking two parameters, rounds_won and rounds_played
def summary(rounds_won, rounds_played):
    print("")
    print("========================================================================")
    print("                                Summary                                 ")
    
    # calculates win percentage    
    win_percentage = (sum(rounds_won.values()) / rounds_played) * 100
    print(f"Win percentage: {round(win_percentage)}%")
    print("Win Distribution:")

    # sorts the rounds_won dictionary
    sorted_rounds_won = dict(sorted(rounds_won.items()))
    
    # loops over to find key and the value and displays it
    for key, value in sorted_rounds_won.items():
        print(f"{key}|{'#' * value}{value}")
        
    print("========================================================================")

# function to get the player's guess
def get_player_guess():
    # player input
    guess = input("\nPlease enter your guess: ")
    
    # loops the player input if unvalid (less than five or a number)
    while len(guess) != 5 or not guess.isalpha():
        guess = input("Your guess must have 5 letters: ")

    # returns the player's guess in lower case
    return guess.lower()

# function to play the game
def play_round(word):
    # original game state 
    game_state = "_ _ _ _ _"
    
    # loops over 6 times, to give the user only 6 guesses to find out the word
    for guess_number in range(1, 7):
        print(f"Guess {guess_number}:")
        # defines guess with the get_player_guess function 
        guess = get_player_guess()
        # defines game_state with the update_game_state function with three parameters, guess, word, game_state
        game_state = update_game_state(guess, word)
        # print new game state
        print(game_state)
        # print new line
        print("")

        # when the game state (without spaces) is equal to the word in uppercase, it will return the guess number and true to indicate teh word was solved
        if game_state.replace(" ", "") == word.upper():
            return guess_number, True
        
    # returns 6 guess and false to indicate the word was not solved
    else:
        return 6, False

# function to get the letter frequencies for either the word or guess
def get_letter_frequencies(string):
    # empty dictionary to store letter frequencies
    frequencies = {}
    
    for letter in string:
        if letter in frequencies:
            # if letter already exists in the dictionary, add one to the frequency
            frequencies[letter] += 1
            
        else: 
            # if letter does not exist in the dictionary, make the frequency equal to one
            frequencies[letter] = 1
            
    # returns the dictionary with letter frequencies
    return frequencies

# function to update the game state
def update_game_state(guess, word):
    # get frequencies of letters in word and guess
    word_frequency = get_letter_frequencies(word)
    guess_frequency = get_letter_frequencies(guess)

    # check letters are in correct position
    updated_state = check_correct_positions(guess, word, word_frequency, guess_frequency)
    # check how many letters are remaining
    updated_state = check_remaining_letters(guess, word, word_frequency, guess_frequency, updated_state)

    # return updated state
    return updated_state


# function to check if any letters are in their correct positions
def check_correct_positions(guess, word, word_frequency, guess_frequency):
    # blank game state
    updated_state = ""

    # loop to add to the blank game state
    for i in range(len(word)):
        # check if letter in the guess is in the correct position and makes letter upper case if so
        if guess[i] == word[i] and word_frequency[guess[i]] > 0 and guess_frequency[guess[i]] > 0:
            updated_state += guess[i].upper()
            # decreases the frequency for word and guess by one
            word_frequency[guess[i]] -= 1
            guess_frequency[guess[i]] -= 1
            
        else:
            # any other letter from guess that is not in the word will be an underscore 
            updated_state += "_"
            
        # adds the spaces in between the letters / underscore for the updated game state
        updated_state += " "

    # returns updated game state 
    return updated_state.strip()


# function to check the remaining letters
def check_remaining_letters(guess, word, word_frequency, guess_frequency, updated_state):
    # loop to check the remaining letters of the guess and word
    for i in range(len(word)):
        # check if the game state position is an underscore
        if updated_state[i * 2] == "_":
            # check if the letter of guess is in word and still has other occurrences within word
            if guess[i] in word and word_frequency[guess[i]] > 0 and guess_frequency[guess[i]] > 0:
                # makes the letter lowercase if the guess letter is in the word but wrong position
                updated_state = updated_state[:i * 2] + guess[i].lower() + updated_state[i * 2 + 1:]
                # decreases the frequency for word and guess by one
                word_frequency[guess[i]] -= 1
                guess_frequency[guess[i]] -= 1
                
            else:
                # adds underscore if the guess letter is not present in the word at all, or if the word has no more occurences
                updated_state = updated_state[:i * 2] + "_" + updated_state[i * 2 + 1:]
                
    # returns updated game state 
    return updated_state

# function to get random words
def get_random_word(words):
    return random.choice(words)
