import random

def randomString(Length, Uppercase = True, Lowercase = True, Numbers = True, Symbols = True):
    """

    Args:
        Length (Int): The length of the random string
        Uppercase (bool, optional): Dictats whenever the string should have uppercase letters or not. Defaults to True.
        Lowercase (bool, optional): Dictats whenever the string should have undercase letters or not. Defaults to True.
        Numbers (bool, optional): Dictats whenever the string should have numbers or not. Defaults to True.
        Symbols (bool, optional): Dictats whenever the string should have symbols or not. Defaults to True.

    Returns:
        String: Returns a random string
    """

    if type(Length) != int:
        raise TypeError("Length must be a integer")
    # TODO: Add better Error handeling


    lettersCharacter = "abcdefghijklmnopqrstuvwxyz"
    bigLettersCharacter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbersCharacter = "1234567890"
    symbolsCharacter = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    characterList = ""

    if Uppercase:
        characterList += bigLettersCharacter
    if Lowercase:
        characterList += lettersCharacter
    if Numbers:
        characterList += numbersCharacter
    if Symbols:
        characterList += symbolsCharacter
    
    return ''.join(random.choice(characterList) for _ in range(Length))

def fastRandomString(Length):
    """Removes Unnessery ifs and whatnot therefor its "Fast"

    Args:
        Length (Integer): Length of the random string

    Returns:
        String: returns a random string
    """
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?") for _ in range(Length))

# TODO: Add more random ID generator functions. Example: Card, Phone, Address.
