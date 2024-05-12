# program to read in `questionAnswers.json` file
# and ask user questions from the file
# program should present all user answers and actual answers at the end

import json
import random
import math
import sys
from glob import glob

from similarityChecker import mark_answer

class Colours:
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'


def print_results(data, user_answers, user_data):
    COLUMN_WIDTH = 60
    TABLE_WIDTH = COLUMN_WIDTH * 3

    def get_result_string(strings, correct, score):
        
        def process_string(s, result):
            offset = s[0]
            s = s[1].split()
            result = append_till_full(result, s, offset=offset)
            return result

        def append_till_full(result, words, offset=1):
            for word in words:
                if len(result) + len(word) <= COLUMN_WIDTH * offset:
                    result += word + ' '
                else:
                    break

            result = result.ljust((COLUMN_WIDTH+1)*offset)
            if offset < 3:
                result += '|'

            return result  

        result = ''
        for i, s in enumerate(strings):
            result = process_string((i+1, s), result)

        print(f"{Colours.GREEN if correct else Colours.RED}{result}[{round(score, 4)}]{Colours.END}")
        
    def reset_string(s):
        size = 0
        last_word = -1
        for i, word in enumerate(s.split()):
            if size + len(word) <= COLUMN_WIDTH:
                size += len(word) + 1
                last_word = i
            else:
                break

        return ' '.join(s.split()[last_word+1:])
    
    reset_strings = lambda strings: [reset_string(s) for s in strings]
    check_size = lambda strings: any([len(s) > COLUMN_WIDTH for s in strings])

    # present user data
    print("-" * (COLUMN_WIDTH+2))
    print(f'You answered {user_data["questions_answered"]} out of {user_data["total_questions"]} questions'.ljust(COLUMN_WIDTH+1)+"|")
    print(f'You got {user_data["correct_answers"]} out of {user_data["questions_answered"]} correct'.ljust(COLUMN_WIDTH+1)+"|")
    print("-" * TABLE_WIDTH)

    # present all user answers and actual answers at the end
    # in a table format
    print('Question'.ljust(COLUMN_WIDTH+1) + '|Actual Answer'.ljust(COLUMN_WIDTH+1) + '|Your Answer'.ljust(COLUMN_WIDTH+1))
    print('-' * TABLE_WIDTH)
    
    for question in data:
        # if text is longer than 50 characters, wrap onto next line
        # need to calculate this for all three columns
        # split on word boundaries, not in the middle of a word
        strings = [question['question'], question['answer'], user_answers[question['question']]]

        correct, score = mark_answer(question['answer'], user_answers[question['question']])

        while check_size(strings):
            get_result_string(strings, correct, score)
            strings = reset_strings(strings)
        get_result_string(strings, correct, score)
        
        print('-' * TABLE_WIDTH)


def main():
    GLOB_PATH = "quizFiles/*.json"

    for i, filename in enumerate(glob(GLOB_PATH)):
        print(f"[{i+1}] {filename.split('/')[-1].split('.')[0]}")

    def get_valid_input(prompt: str, min_val: int, max_val: int):
        validate_input_digit = lambda input, min_val, max_val: input.isdigit() and (min_val <= int(input) <= max_val)
    
        user_input = input(prompt)
        while not validate_input_digit(user_input, min_val, max_val):
            user_input = input(prompt)
        
        return int(user_input)

    fileIndex = get_valid_input('Select a file: ', 1, len(glob(GLOB_PATH)))
    
    data = []
    with open(glob(GLOB_PATH)[int(fileIndex)-1]) as f:
        data = json.load(f)

    range = (0,len(data))
    if (len(sys.argv) > 2):
        if (sys.argv[1].isdigit() and sys.argv[2].isdigit()):
            range = (math.floor(int(sys.argv[1])/100*len(data)), math.floor(int(sys.argv[2])/100*len(data)))

    data = data[range[0]:range[1]]

    print("[1] Inorder\n[2] Shuffled")
    inOrder = get_valid_input('Select an ordering : ', 1, 2)
    if inOrder != 1:
        random.shuffle(data)

    numberOfQuestions = int(get_valid_input(f"Select a number of questions from 1 to {len(data)}: ", 1, len(data)))

    # ask user questions from the file
    # randomise the order of questions
    user_answers = {}
    user_data = {
        'questions_answered': 0,
        'total_questions': numberOfQuestions,
        'correct_answers': 0,
    }

    for question in data[:numberOfQuestions]:
        print(question['question'])

        user_answer = input('Your answer: ')
        user_answers[question['question']] = user_answer
        user_data['questions_answered'] += len(user_answer) and 1 

        correct, score = mark_answer(question['answer'], user_answers[question['question']])
        user_data['correct_answers'] += 1 if correct else 0

        print(f"{Colours.GREEN if correct else Colours.RED}Correct answer was: {question['answer']} [{round(score, 4)}]{Colours.END}")

    print_results(data[:numberOfQuestions], user_answers, user_data)


if __name__ == '__main__':
    main()
