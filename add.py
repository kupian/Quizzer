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
            add()
        elif res == MODE.IMPORT.value:
            pass

def add() -> bool:
    questions = []
    
    name = input("Name of quiz: ")
    if os.path.isfile(f"{QUIZ_DIR}/{name}.json"):
        print("Quiz already exists")
        return False
    
    print("Enter 'q' to cancel and quit, 'u' to undo last entry. Leave input blank to finish")
    
    while True:
        question = input("q: ")
        if question == "q": return False
        elif question == "":
            write(name, questions)
            print("Quiz written to file")
            return True
        
        answer = input("a: ")
        if answer == "q": return False
        
        questions.append({
            "question": question,
            "answer": answer
        })
        
def write(name: str, questions: list):
    with open(f"{QUIZ_DIR}/{name}.json", "w") as f:
        f.write(json.dumps(questions, indent=4))

if __name__ == "__main__":
    main()