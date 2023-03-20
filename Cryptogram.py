import os
import colorama
from shutil import copyfile
from termcolor import colored
from datetime import datetime


# Replaces letters in cryptogram and records if they should be considered changed or not
def replacer(old, new, changed=False, red=False):
    print()
    for i in range(len(cryptogram)):
        # Ensures letters of only one category (changed or unchanged) are replaced
        if cryptogram[i][0] == old and cryptogram[i][1] is changed:
            if red is True:  # It should be considered changed and be printed as red
                cryptogram[i] = [new, True]
            else:  # # It should be considered unchanged and be printed as white
                cryptogram[i] = [new, False]
        printing(cryptogram[i])
    print()


# Prints cryptogram, making changed letters appear as red
def printing(curr):
    if curr[1] is True:
        print(colored(curr[0], 'red'), end=' ')
    else:
        if curr[0] == '\n':  # Avoids adding spaces to newline characters
            print(curr[0])
        else:
            print(curr[0], end=' ')


# Used to check user inputs, whether they be responses to prompts or letters for substituting
def input_check(prompt, sec=False, responses=None, letter=False, revert=False):
    if responses is None:  # If a letter is being substituted, a list of responses is unneeded
        responses = []

    if letter is True:  # Checks letters in cryptogram for replacing
        if revert is False:  # If there's no reverting, a substituted letter is needed
            string = input(prompt).upper()
        else:
            string = alphaold[0]  # The string can be anything that passes upcoming checks
        if string.isalpha() is False:  # String is not a letter
            print("Please pick a letter from A-Z.")
            return input_check(prompt, letter=True, sec=sec)
        elif len(string) != 1:  # Multiple letters are given
            print("Please pick only one letter.")
            return input_check(prompt, letter=True, sec=sec)
        elif sec is False:  # If this is the letter to be replaced
            # Keeps track of whether the letter to be changed falls under two states: changed and unchanged
            difference = [False, False]
            for i in range(len(cryptogram)):
                if string == cryptogram[i][0]:  # Match is found
                    if cryptogram[i][1] is True:  # The letter is changed
                        difference[0] = True
                    else:
                        difference[1] = True  # The letter is unchanged
            # Since there can't be two falses, the letter must be present in both changed and unchanged forms
            if difference[0] is difference[1]:
                # Asks the user if they want to change the changed or unchanged string
                return [string,
                        input_check(f"\nWould you like to replace the changed {string} or the unchanged "
                                    f"{string}? [Changed/Unchanged/C/U] ", responses=["changed", "unchanged", "c", "u"])
                        in ['changed', 'c']]
            # The letter is only present in changed form, so no user input is required
            elif difference[0] is True:
                return [string, True]
            # The letter is only present in unchanged form, so no user input is required
            return [string, False]

        elif sec is True:  # If this is the letter for replacing
            if revert is False and string == alphaold[0]:  # The letter is replacing itself
                print("You cannot substitute a letter with itself.")
                return input_check(f"\nWhat letter do you want to replace {alphaold[0]} with? ",
                                   sec=True, letter=True)
            og = False  # Will track if the letter for replacing is from the original cryptogram
            substituted = [False, '']
            for i in range(len(cryptogram)):
                if string == cryptogram[i][0]:  # Match is found
                    if cryptogram[i][1] is True:  # The letter for replacing is already substituted
                        substituted = [True, i]
                # Matches with the letter to be replaced, to determine if the replacing letter is an original letter
                elif alphaold == cryptogram[i]:
                    if data[1][i] == string:  # If the original letter equals the letter for replacing
                        og = True
            if revert is True:
                return[data[1][substituted[1]], True]  # Return the original letter and that it's an original
            # The letter for replacing is substituted and it's not meant to be an original
            if og is False and substituted[0] is True:
                print(f"{string} is already substituted. Please undo '{string}' to '{data[1][substituted[1]]}' "
                      "or substitute a different letter.")  # Tells the user how to undo the substituted letter
                return input_check(f"\nWhat letter do you want to replace {alphaold[0]} with? ",
                                   sec=True, letter=True)
            else:
                return [string, og]

    else:  # Regular input checker
        rawinput = input(prompt).rstrip().lower()
        for response in responses:
            if rawinput == response:  # The user put an accepted response
                return response
        # The user didn't put an accepted response
        print("Please respond with {}.". format(' or '.join(map(lambda x: f'"{x}"', responses))))
        return input_check(prompt, responses=responses)  # Re-prompt them


# Prompts the user to enter their cryptogram
def creation():
    try:
        lines = int(input("\nHow many lines is your cryptogram? "))
    except ValueError:  # The user didn't enter an int
        print("Please type a whole number.")
        return creation()

    print()
    res = ""  # Will store cryptogram
    for i in range(lines):
        line = input(f"Line {i + 1}: ").rstrip().upper()
        if i + 1 == lines:  # Don't add a newline to the last line
            res += line
        else:
            res += line + '\n'
    return res


# Sets up the program by opening and handling files
def setup(dir):
    try:  # Checks if the file exists
        file = open(dir, 'r')
        reader = file.read().rstrip()
        try:  # Checks if the file contains any alphabetical data
            if reader[0].isalpha() is False:  # If it doesn't, have the user fill it
                file.close()
                with open(dir, 'w') as file:
                    file.write(creation())
        except IndexError:  # If the file doesn't contain anything, have the user fill it
            file.close()
            with open(dir, 'w') as file:
                file.write(creation())
    except FileNotFoundError:  # If the file doesn't exist, create one and have the user fill it
        with open(dir, 'w') as file:
            file.write(creation())

    with open(dir, 'r') as file:  # Reads cryptogram into memory
        rawcryptogram = file.read()

    # If the program has been run before, changed and unchanged data will be separated by the string "##"
    data = rawcryptogram.split("##")
    if len(data) == 1:  # The program has not been run before, so the cryptogram is still in an unchanged state.
        data.append(data[0])  # Makes a copy of the unchanged data for later use
    else:  # The program has been run before
        # Prompts the user if they'd like to continue where they left off or start over
        if input_check("\nWould you like to continue where you left off or start over? [Left off/Start over] ",
                       responses=["left off", "start over"]) == 'start over':

            # They can clear the current cryptogram, or make a new one
            action = input_check("\nWould you like to work on a new cryptogram or clear your current one? [New/Clear] ",
                                 responses=["new", "clear"])

            # Extra confirmation check
            if 'y' in input_check("\nAre you sure? Your progress will be deleted and this can't be undone. [Y/N] ",
                                  responses=["yes", "no", 'y', 'n']):
                timestamp = datetime.now().strftime("/%m-%d-%Y-%H.%M.%S")
                os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "/archive", exist_ok=True)
                copyfile(dir, os.path.dirname(os.path.realpath(__file__)) + "/archive" + timestamp + ".txt")
                print("A copy of the save file has been created as a precautionary measure in your current directory.")
                print(os.path.dirname(os.path.realpath(__file__)) + "/archive" + timestamp)
            # If the user would like to start over, delete the save file and return false
                if action == "new":
                    os.remove(dir)
                    return False
                else:  # The user would like to clear their changes
                    data[0] = data[1]  # Set the changed cryptogram equal to the unchanged one
    print()
    return data


colorama.init()
dir = os.path.dirname(os.path.realpath(__file__)) + "/input.txt"  # Path to save file
data = setup(dir)  # Sets up program
while data is False:  # Calls setup until a new cryptogram is entered
    data = setup(dir)

cryptogram = []  # Will store the user changed cryptogram

# Finds differences between changed and unchanged cryptograms and notates the changed letters
for x, y in zip(data[0], data[1]):
    if x != y:
        itm = [x, True]
    else:
        itm = [x, False]
    cryptogram.append(itm)
    printing(itm)  # Print the cryptogram
print()

while True:
    alphaold = input_check("\nWhat letter do you want to replace? ", letter=True)
    rev = False
    alphanew = []
    if alphaold[1] is True:
        if input_check(f"\nWould you like to revert {alphaold[0]} to its original letter?[Y/N] ",
                          responses=["yes", "no", 'y', 'n']) in ["y", "yes"]:
            alphanew = input_check("\n", sec=True, letter=True, revert=True)
            rev = True
    if rev is False:
        alphanew = input_check(f"\nWhat letter do you want to replace {alphaold[0]} with? ", sec=True, letter=True)

    # Replaces letters, notating if old one is the changed version or not and if the new one is an original
    replacer(alphaold[0], alphanew[0], changed=alphaold[1], red=not alphanew[1])

    # Gives the user an option to undo their change, continue, or exit the program
    action = input_check("\nDone, undo, or continue?[D/U/C] ", responses=["done", "undo", "continue", "d", "u", "c"])
    if action in ["u", "undo"]:
        # Reverses the first replacement, retaining if the original letter was changed
        # and noting that, unless the new letter is an original, it must be changed
        replacer(alphanew[0], alphaold[0], changed=not alphanew[1], red=alphaold[1])

    if action in ["d", "done"]:
        completed = True
        for i in range(len(cryptogram)):
            if cryptogram[i][0].isalpha() is True:
                if cryptogram[i][1] is False:
                    completed = False
        if completed is True:
            for i in range(len(cryptogram)):
                print(colored(cryptogram[i][0], "green"), end='')
            print()
            print(colored("Congrats on finishing!!", "blue"))
        else:
            print("\nSee you next time :-)")
        break

with open(dir, 'w') as file:
    for itm in cryptogram:
        file.write(itm[0])
    file.write("##{}".format(data[1]))  # Writes the unchanged cryptogram to the end of the save file
