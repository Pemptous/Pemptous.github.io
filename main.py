from database import Database
from my_database import myDatabase as myDatabaseString
from pyscript import web, when

import base64

def b(token: str, a: str) -> str:
    token = token.strip()
    token += "=" * (-len(token) % 4)
    xored = base64.b64decode(token.encode("ascii"))
    key_bytes = a.encode("utf-8")
    key = (key_bytes * (len(xored) // len(key_bytes) + 1))[:len(xored)]
    return bytes(a ^ b for a, b in zip(xored, key)).decode("utf-8")

awaiting_text = False
database = None
current_trait = None
nquestion = 1
#HARD_LIMIT = 0

question_div = web.page["box"]
output_div = web.page["console"]
def printf(text="", end="\n"):
    text = str(text)
    output_div.innerText += text + end
    '''
    if output_div.innerText.count('\n') > HARD_LIMIT:
        output_div.innerText = output_div.innerText[output_div.innerText.index('\n')+1:]
    '''
        
def quest(text):
    question_div.innerText = text

def init():
    global database, HARD_LIMIT
    
    database = Database(b(myDatabaseString,"bismillah"))
    #HARD_LIMIT = len(database.names) + 4
    printf("Hey there! Imma try to guess which friend of Panos' you're thinking of.\n")

    printf('The friends which currently exist in the database are:')
    for name in database.names:
        printf(" -   " + name)
    printf()

    ask_question()

def ask_question():
    global database, awaiting_text, current_trait, nquestion

    current_trait = database.best_request()
    if current_trait == -1:
        quest("I can't figure it out! You don't know enough about them.")
        return 


    quest(f"{nquestion}. {current_trait}")
    nquestion += 1
    awaiting_text = True

def do_something_with_the_input(answer):
    global database, awaiting_text, current_trait

    match answer:
        case "yes": answer = True
        case "no": answer = False
        case "dunno":
            database.traits.remove(current_trait)
            answer = None

    if answer != None:
        left, guess = database.update(current_trait, answer)

        awaiting_text = False

        if left == 0:
            quest("I can't figure it out! Something doesn't add up.")
            printf("0 characters left.")
        elif left == 1:
            printf("1 character left.")
            if guess != "Yours Truly":
                quest(f"*HIS* friend you are thinking of must be: {guess}!")
            else: quest("You are thinking of me. So kawai (nga)")
        else:
            printf(f"There are {left} characters left")
            ask_question()
    else:
        ask_question()

@when("click", "#yes")
def yes(event):
    do_something_with_the_input("yes")

@when("click", "#dunno")
def dunno(event):
    do_something_with_the_input("dunno")
    
@when("click", "#no")
def no(event):
    do_something_with_the_input("no")

if __name__ == "__main__":
    init()