import json, random

class Database:
    def __init__(self, content) -> None:
        self.db = json.loads(content)

        self.traits = self.db["traits"]
        self.names = self.db["character_names"]
        self.current_characters = self.db["characters"]
        #self.file_name = file_name

    def update(self, trait, answer):
        self.current_characters = [char for char in self.current_characters if char['traits'].get(trait) == answer]
        characters_left = len(self.current_characters)
        if characters_left == 0: return (0, None)
        return (characters_left, self.current_characters[0]["name"])
        

    def best_request(self):
        n = len(self.current_characters)
        half = n//2

        best_traits = self.traits[:]
        if len(self.traits) == 0: return -1
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