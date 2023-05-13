import json

from . import Persona

def main():
    def test_messages(dialect):
        db = 'chinook'
        interpreter = Persona('interpreter', dialect)
        question = ''
        messages = interpreter.construct_messages(db, question)
        # response = {'choices': [{"message": {"content": ""}}]}
        return json_serializable(messages)


    def json_serializable(x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    print(test_messages("SQLite"))

if __name__ == "__main__":
    main()

