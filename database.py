import json, random, shutil

class Database:
    def __init__(self, content) -> None:
        self.db = json.loads(content)

        self.traits = self.db["traits"]
        self.names = self.db["character_names"]
        self.current_characters = self.db["characters"]
        #self.file_name = file_name

    def update(self, trait, answer) -> str:
        self.current_characters = [char for char in self.current_characters if char['traits'].get(trait) == answer]

        characters_left = len(self.current_characters)
        return (characters_left, self.current_characters[0]["name"])
        '''
        if characters_left == 1:
            return self.current_characters[0]["name"]
        if characters_left == 0:
            return "no result"
        return "There are {characters_left} characters left\n"
        '''
        

    def best_request(self) -> str:
        n = len(self.current_characters)
        half = n/2

        best_traits = self.traits[:]
        best_diff = n

        for trait in self.traits:
            count_true = sum(char['traits'].get(trait, False) for char in self.current_characters)

            diff = abs(count_true - half)

            if diff < best_diff:
                best_diff = diff
                best_traits = [trait]
            elif diff == best_diff:
                best_traits.append(trait)

        return random.choice(best_traits)
    
    def add_to_databse(self) -> None:
        name = input("To  append your character to the database you will have to answer with y (=yes) or n (=no) to each trait which will be printed. What is your character's name? ")
        character_dictionary = {"name": name, "traits":{}}
        for trait in self.traits: 
            ans = input(trait+' ').strip().lower()
            if ans == 'y': ans = True
            else: ans = False
            character_dictionary["traits"].update({trait:ans})
        
        self.db["characters"].append(character_dictionary)
        self.db["character_names"].append(name)

        shutil.copy('database.json', 'backup.json')
        with open("database.json", "w") as f:
            json.dump(self.db, f, indent=4)
            #f.write(json.dumps(self.db))