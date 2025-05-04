# Program to add / import new quizzes either through command-line text entry or .txt import
# Alex Carr, May 2025

from enum import Enum
import json
import os

QUIZ_DIR="quizFiles"

class MODE(Enum):
    ADD = 1
    IMPORT = 2

def main():
    running = True
    while running: 
        print("Add a new quiz (1) or import a quiz from txt (2)?")
        try:
            res = int(input())
        except ValueError:
            print("Invalid response. Please enter a number.")
            continue
        if res == MODE.ADD.value:
            quiz = add()
            if quiz.get("questions") is not None:
                write(quiz.get("name"), quiz.get("questions"))
                print("Quiz written to file")
        elif res == MODE.IMPORT.value:
            import_quiz()

def add() -> dict:
    '''
    Generate a new quiz from command line inputs
    
    returns: {name: str, questions: list}
    '''
    questions = []
    
    name = input("Name of quiz: ")
    if os.path.isfile(f"{QUIZ_DIR}/{name}.json"):
        print("Quiz already exists")
        return None
    
    print("Enter 'q' to cancel and quit, 'u' to undo last entry. Leave input blank to finish")
    
    while True:
        question = input("q: ")
        if question == "q": return None
        elif question == "":
            return {"name": name, "questions": questions}
        
        answer = input("a: ")
        if answer == "q": return None
        
        questions.append({
            "question": question,
            "answer": answer
        })
        
def import_quiz():
    '''
    Generates a quiz from a text file
    '''
    print("TODO")
    return False
        
def write(name: str, questions: list):
    '''
    Write a new quiz to file
    '''
    with open(f"{QUIZ_DIR}/{name}.json", "w") as f:
        f.write(json.dumps(questions, indent=4))

if __name__ == "__main__":
    main()