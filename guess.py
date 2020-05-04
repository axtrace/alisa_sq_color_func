import random


def while_or_black(text):
    whites = ('белый', 'белая', 'белые', 'белое', 'белого')
    blacks = (
        'черный', 'черная', 'черное', 'черные', 'чёрн', 'черного', 'черн')
    for c in whites:
        if c in text:
            return 'WHITE'
    for c in blacks:
        if c in text:
            return 'BLACK'
    return ''


def square_color(square):
    file = square[0]
    rank = int(square[1])

    file_num = ord(file.lower()) - ord('a') + 1
    if (rank + file_num) % 2 == 0:
        return 'BLACK'
    return 'WHITE'


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

    answer = 'Привет! Давай поиграем. Я буду называть клетку шахматной доски, а ты попробуй угадать её цвет. Начинаем?'
    answer_tts = ''
    square = ''
    is_session_end = 'false'
    count = 0
    # if event is not None and event['request']['session']['new']:
    # Новая сессия

    if event is not None and 'request' in event and 'original_utterance' in \
            event['request'] and len(event['request']['original_utterance']):
        text = event['request']['command']
        intents = {}
        if 'nlu' in event['request']:
            if 'intents' in event['request']['nlu']:
                intents = event['request']['nlu']['intents']

        if 'YANDEX.HELP' in intents or 'YANDEX.WHAT_CAN_YOU_DO' in intents:
            answer = 'Я называю координаты шахматной клетки, а ты угадываешь её цвет. Например, a1 - чёрный, a2 - белый'
            answer_tts = f'Я называю координаты шахматной клетки, а ты угадываешь её цвет. Например, {say_square("a1")} - чёрный, {say_square("a2")} - белый'
        elif 'YANDEX.CONFIRM' in intents or 'да' in text or 'начин' in text:
            square = random_square()
            color = square_color(square)
            answer = f'Какого цвета клетка {square}?'
            answer_tts = f'Какого цвета клетка {say_square(square)}?'
        elif 'WHITE_WORD' in intents or 'BLACK_WORD' in intents or while_or_black(
                text.lower()):
            prev_square = event['state']['session']['square']
            count = event['state']['session']['count']
            color = square_color(prev_square)
            user_color = 'BLACK'
            if 'WHITE_WORD' in intents or while_or_black(
                    text.lower()) == 'WHITE':
                user_color = 'WHITE'
            if user_color == color:
                answer = 'Правильно! '
                answer_tts = 'Правильно! '
                count += 1
            else:
                answer = f'Неправильно! Клетка {prev_square} {say_color(color)} цвета. Увы, обнуляем счетчик. '
                answer_tts = f'Неправильно! Клетка {say_square(prev_square)} {say_color(color)} цвета. Увы, обнуляем счетчик. '
                count = 0
            if count > 0 and count % 3 == 0:
                answer += f'У тебя уже {count} правильных ответов подряд. Так держать! '
                answer_tts += f'У тебя уже {count} правильных ответов подряд. Так держать! '
            square = random_square()
            answer += f'А теперь скажи, какого цвета клетка {square}?'
            answer_tts += f'А теперь скажи, какого цвета клетка {say_square(square)}?'
        else:
            square = ''
            if 'state' in event:
                if 'session' in event['state']:
                    if 'square' in event['state']['session']:
                        square = event['state']['session']['square']
            if square:
                answer = f'Прости. Я не смогла понять твой ответ. Назови цвет клетки {square}: белый или чёрный'
                answer_tts = f'Прости. Я не смогла понять твой ответ. Назови цвет клетки {say_square(square)}: белый или чёрный'
            else:
                answer = f'Прости. Я не смогла понять твой ответ. Начинаем?'
                answer_tts = f'Прости. Я не смогла понять твой ответ. Начинаем?'
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
        'session_state': {
            'square': square,
            'count': count
        }
    }
