# program to read in `questionAnswers.json` file
# and ask user questions from the file
# program should present all user answers and actual answers at the end

import json
import random
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


def quiz():
    GLOB_PATH = "quizFiles/*.json"

    # read in quiz file
    # mode = input('Select a mode (1 = answers only at end, 2 = answers also as you go): ')
    # while mode not in ['1', '2']:
    #     mode = input('Select a mode (1 = answers only at end, 2 = answers also as you go): ')

    data = []
    for i, filename in enumerate(glob(GLOB_PATH)):
        print(f"[{i+1}] {filename.split('/')[-1].split('.')[0]}")

    fileIndex = input('Select a file: ')
    while not fileIndex.isdigit() or int(fileIndex) < 1 or int(fileIndex) > len(glob(GLOB_PATH)):
        fileIndex = input('Select a file: ')
    
    with open(glob(GLOB_PATH)[int(fileIndex)-1]) as f:
        data = json.load(f)

    # ask user questions from the file
    # randomise the order of questions
    random.shuffle(data)
    user_answers = {}
    user_data = {
        'questions_answered': 0,
        'total_questions': 0,
        'correct_answers': 0,
    }

    for question in data:
        print(question['question'])
        user_answer = input('Your answer: ')
        user_answers[question['question']] = user_answer
        user_data['total_questions'] += 1
        if len(user_answer) > 0:
            user_data['questions_answered'] += 1

        correct, score = mark_answer(question['answer'], user_answers[question['question']])
        if correct:
            user_data['correct_answers'] += 1

        print(f"{Colours.GREEN if correct else Colours.RED}Correct answer was: {question['answer']} [{round(score, 4)}]{Colours.END}")

    print_results(data, user_answers, user_data)


def main():
    quiz()


if __name__ == '__main__':
    main()
