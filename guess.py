import random


def square_color(square):
    file = square[0]
    rank = int(square[1])

    file_num = ord(file.lower()) - ord('a') + 1
    if (rank + file_num) % 2 == 0:
        return 'BLACK'
    return 'WHITE'

def while_or_black(text):
    whites = ('белый', 'белая', 'белые', 'белое')
    blacks = ('черный', 'черная', 'черное', 'черные', 'чёрн')
    for c in whites:
        if c in text:
            return 'WHITE'
    for c in blacks:
        if c in text:
            return 'BLACK'
    return ''


def random_square():
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rank = random.randint(1, 8)
    file_index = random.randint(0, 7)
    return str(files[file_index]) + str(rank)


def say_square(square):
    letters_for_pronunciation = {
        'ru': {'a': 'а', 'b': 'бэ', 'c': 'цэ', 'd': 'дэ', 'e': 'е', 'f': 'эф',
               'g': 'же', 'h': 'аш'}}

    if not square:
        return ''
    file = square[0]
    rank = int(square[1])
    file_pron = letters_for_pronunciation['ru'].get(file, '')
    return file_pron + str(rank)

def say_color(color):
    if color == 'WHITE':
        return 'белого'
    elif color == 'BLACK':
        return 'чёрного'
    return ''


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    answer = 'Привет! Давай поиграем. Я буду называть клетку шахматной доски, а ты попробуй угадать её цвет. Для начала игры скажите "Да". Начинаем?'
    answer_tts = ''
    square = ''
    color = ''
    is_session_end = 'false'
    right_count = 0

    if event is not None and 'request' in event and 'original_utterance' in event['request'] and len(event['request']['original_utterance']):
        text = event['request']['command']
        user_color = while_or_black(text.lower())

        if 'помощь' in text.lower() or 'что ты умеешь' in text.lower():
            answer = 'Я называю координаты шахматной клетки, а ты угадываешь её цвет. Например, а1 - чёрный, a2 - белый'
        elif 'да' in text.lower():
            square = random_square()
            color = square_color(square)
            answer = f'Какого цвета клетка {square}?'
            answer_tts = f'Какого цвета клетка {say_square(square)}?'
        elif user_color:
            if user_color == color:
                answer = 'Правильно!'
            else:
                answer = f'Неправильно! Клетка {square} {say_color(color)} цвета'
                answer_tts = f'Неправильно! Клетка {say_square(square)} {say_color(color)} цвета'
            square = random_square()
            color = square_color(square)
            answer += f'. А теперь скажи, какого цвета клетка {square}?'
            answer_tts += f'. А теперь скажи, какого цвета клетка {say_square(square)}?' 
        else:
             answer = f'Я не поняла. Назови цвет клетки {square}: белый или чёрный'
             answer_tts = f'Я не поняла. Назови цвет клетки {say_square(square)}: белый или чёрный'
    if not len(answer_tts):
        answer_tts = answer
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': answer,
            'tts': answer_tts,
            'end_session': is_session_end
        },
    }