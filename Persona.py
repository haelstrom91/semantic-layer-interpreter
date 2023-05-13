import yaml

class Persona:
    def __init__(self, name):
        self.name = name
        self.system_message = get_persona_prompt(name)

    def construct_messages(self, database, question):
        semantics = read_semantics(database)
        return [
            {
                "role": "system", 
                "content": self.system_message
            },
            {
                "role": "user", 
                "content": yaml.dump(semantics)
            },
            {
                "role": "assistant", 
                "content": ""
            },
            {
                "role": "user", 
                "content": question
            }
        ]

def read_semantics(database):
    with open(f"semantics/{database}.yml", "r") as stream:
        try:
            semantics = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return semantics


def get_persona_prompt(name):
    with open(f'prompts/{name}.txt', 'r') as file:
        prompt = file.read()
    return prompt