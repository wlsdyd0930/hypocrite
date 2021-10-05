import random

def change_to_another_unicode(latin_letter):
    if latin_letter == "!":
        another_unicode = random.choice(["ǃ"])
    elif latin_letter == ",":
        another_unicode = random.choice(["‚"])
    elif latin_letter == "/":
        another_unicode = random.choice(["̸"])
    elif latin_letter == ":":
        another_unicode = random.choice(["։"])
    elif latin_letter == ";":
        another_unicode = random.choice([";"])
    elif latin_letter == "d":
        another_unicode = random.choice(["ԁ"])
    elif latin_letter == "A":
        another_unicode = random.choice(["А","Α"])
    elif latin_letter == "a":
        another_unicode = random.choice(["а"])
    elif latin_letter == "B":
        another_unicode = random.choice(["В", "Β"])
    elif latin_letter == "C":
        another_unicode = random.choice(["С", "Ϲ"])
    elif latin_letter == "c":
        another_unicode = random.choice(["с"])
    elif latin_letter == "D":
        another_unicode = random.choice(["Ⅾ"])
    elif latin_letter == "E":
        another_unicode = random.choice(["Е", "Ε"])
    elif latin_letter == "e":
        another_unicode = random.choice(["е"])
    elif latin_letter == "F":
        another_unicode = random.choice(["Ϝ"])
    elif latin_letter == "G":
        another_unicode = random.choice(["Ԍ"])
    elif latin_letter == "g":
        another_unicode = random.choice(["ɡ"])
    elif latin_letter == "H":
        another_unicode = random.choice(["Н", "Η"])
    elif latin_letter == "h":
        another_unicode = random.choice(["һ", "հ"])
    elif latin_letter == "I":
        another_unicode = random.choice(["Ι", "І"])
    elif latin_letter == "i":
        another_unicode = random.choice(["і"])
    elif latin_letter == "J":
        another_unicode = random.choice(["Ј"])
    elif latin_letter == "j":
        another_unicode = random.choice(["ϳ", "ј"])
    elif latin_letter == "K":
        another_unicode = random.choice(["К", "Κ"])
    elif latin_letter == "M":
        another_unicode = random.choice(["М", "Μ", "Ꮇ", "Ⅿ"])
    elif latin_letter == "N":
        another_unicode = random.choice(["Ν"])
    elif latin_letter == "O":
        another_unicode = random.choice(["О", "Ο"])
    elif latin_letter == "o":
        another_unicode = random.choice(["о", "ο"])
    elif latin_letter == "P":
        another_unicode = random.choice(["Р", "Ρ"])
    elif latin_letter == "p":
        another_unicode = random.choice(["р"])
    elif latin_letter == "Q":
        another_unicode = random.choice(["Ⴍ"])
    elif latin_letter == "q":
        another_unicode = random.choice(["ԛ"])
    elif latin_letter == "S":
        another_unicode = random.choice(["Ѕ", "Տ"])
    elif latin_letter == "s":
        another_unicode = random.choice(["ѕ"])
    elif latin_letter == "T":
        another_unicode = random.choice(["Т", "Τ"])
    elif latin_letter == "U":
        another_unicode = random.choice(["Ս"])
    elif latin_letter == "V":
        another_unicode = random.choice(["Ꮩ", "Ⅴ"])
    elif latin_letter == "v":
        another_unicode = random.choice(["ᴠ"])
    elif latin_letter == "W":
        another_unicode = random.choice(["Ꮃ"])
    elif latin_letter == "w":
        another_unicode = random.choice(["ᴡ", "ԝ"])
    elif latin_letter == "X":
        another_unicode = random.choice(["Х", "Χ"])
    elif latin_letter == "x":
        another_unicode = random.choice(["х"])
    elif latin_letter == "Y":
        another_unicode = random.choice(["Ү", "Υ"])
    elif latin_letter == "y":
        another_unicode = random.choice(["у"])
    elif latin_letter == "Z":
        another_unicode = random.choice(["Ζ"])
    elif latin_letter == "z":
        another_unicode = random.choice(["ᴢ"])
    else:
        another_unicode = latin_letter
    return another_unicode