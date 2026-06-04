import json
from database import Database
from my_database import myDatabase as myDatabaseString
from pyscript import web, when

import base64, json

def decrypt(token: str, password: str) -> str:
    token = token.strip()
    token += "=" * (-len(token) % 4)
    xored = base64.b64decode(token.encode("ascii"))
    key_bytes = password.encode("utf-8")
    key = (key_bytes * (len(xored) // len(key_bytes) + 1))[:len(xored)]
    return bytes(a ^ b for a, b in zip(xored, key)).decode("utf-8")

awaiting_text = False
database = None
current_trait = None
HARD_LIMIT = 29

input_text = web.page["inputted"]

output_div = web.page["output"]
def printf(text="", end="\n"):
    text = str(text)
    output_div.innerText += text + end
    if output_div.innerText.count('\n') > HARD_LIMIT:
        output_div.innerText = output_div.innerText[output_div.innerText.index('\n')+1:]

def init():
    global database
    database = Database(decrypt(myDatabaseString,"bismillah"))
    printf("Hey there! Imma try to guess which friend of Panos' you're thinking of.\n")

    printf('The friends which currently exist in the database are:')
    for name in database.names:
        printf(" -   " + name)
    #printf()

    ask_question()

def ask_question():
    global database, awaiting_text, current_trait
    printf()

    current_trait = database.best_request()
    question = f"{current_trait} (yes/no/dunno)? " # STRAIGHT UP QUESTION

    printf(question, end=" --> ")
    awaiting_text = True

def do_something_with_the_answer(answer):
    global database, awaiting_text, current_trait

    match answer:
        case "yes": answer = True
        case "no": answer = False
        case "dunno":
            database.traits.remove(current_trait)
            answer = None
        case _:
            printf("Didn't get that. Repeat:", end=" --> ")
            return

    if answer != None:
        left, guess = database.update(current_trait, answer)

        awaiting_text = False

        if left == 0: printf("No results! You probably entered false information about your character.")
        elif left == 1:
            if guess != "Yours Truly":
                printf(f"*HIS* friend you are thinking of must be: {guess}!")
            else: printf("You are thinking of me. So kawai (nga)")
        else:
            printf(f"There are {left} characters left")
            ask_question()
    else:
        ask_question()

def do_something_with_the_input():
    inputted_text = input_text.value
    if inputted_text and awaiting_text:
        printf(inputted_text)
        input_text.value = ""

        answer = inputted_text.strip().lower()
        do_something_with_the_answer(answer)

@when("click", "#button")
def translate_english(event):
    do_something_with_the_input()

@when("keydown", "#inputted")
def handle_enter(event):
    if event.key == "Enter":
        do_something_with_the_input()

if __name__ == "__main__":
    init()