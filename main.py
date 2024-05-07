# program to read in `questionAnswers.json` file
# and ask user questions from the file
# program should present all user answers and actual answers at the end

import json
import random

def print_results(data, user_answers, user_data):
    COLUMN_WIDTH = 65
    TABLE_WIDTH = COLUMN_WIDTH * 3

    def get_result_string(strings):

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

        print(result)
        
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
    print("-" * TABLE_WIDTH)

    # present all user answers and actual answers at the end
    # in a table format
    print('Question'.ljust(COLUMN_WIDTH+1) + '|Your Answer'.ljust(COLUMN_WIDTH+1) + '|Actual Answer'.ljust(COLUMN_WIDTH+1))
    print('-' * TABLE_WIDTH)
    
    for question in data:
        # if text is longer than 50 characters, wrap onto next line
        # need to calculate this for all three columns
        # split on word boundaries, not in the middle of a word
        strings = [question['question'], user_answers[question['question']], question['answer']]

        while check_size(strings):
            get_result_string(strings)
            strings = reset_strings(strings)
        get_result_string(strings)
        
        print('-' * TABLE_WIDTH)


def quiz(filenames):
    # read in questionAnswers.json file
    data = []
    for filename in filenames:
        with open(filename) as f:
            data = data + json.load(f)

    # ask user questions from the file
    # randomise the order of questions
    random.shuffle(data)
    user_answers = {}
    user_data = {
        'questions_answered': 0,
        'total_questions': 0
    }
    for question in data:
        print(question['question'])
        user_answer = input('Your answer: ')
        user_answers[question['question']] = user_answer
        user_data['total_questions'] += 1
        if len(user_answer) > 0:
            user_data['questions_answered'] += 1

    print_results(data, user_answers, user_data)


def main():
    quiz(['questionAnswersVK.json'])


if __name__ == '__main__':
    main()