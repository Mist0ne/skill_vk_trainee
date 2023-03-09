# flake8: noqa: E501
import random
from . import main_phrases


def handle_dialog(req):
    res = dict()
    res['version'] = req['version']
    res['session'] = req['session']
    res['response'] = {
        'end_session': False
    }

    original_utterance = req['request']['command']
    res['session_state'] = {'error_count': 0}

    flag = True
    for question in main_phrases.phrases:
        if original_utterance in question['question_list']:
            if type(question['answer']) == list:
                random_number = random.randint(0, len(question['answer'])-1)
                res['response']['text'] = question['answer'][random_number]
                res['response']['tts'] = question['tts'][random_number]
            else:
                res['response']['text'] = question['answer']
                res['response']['tts'] = question['tts']
            flag = False
            break

    if flag and original_utterance in main_phrases.stop_phrases['question_list']:
        res['response']['text'] = main_phrases.stop_phrases['answer']
        res['response']['tts'] = main_phrases.stop_phrases['tts']
        res['response']['end_session'] = True
        flag = False

    if flag:
        if 'error_count' in req['state']['session']:
            res['session_state'] = {'error_count': req['state']['session']['error_count'] + 1}
            # if req['state']['session']['error_count'] <= 3:
            #     res['response']['text'] = main_phrases.dont_understand['answer']
            #     res['response']['tts'] = main_phrases.dont_understand['tts']
            # else:
            #     res['response']['text'] = main_phrases.dont_understand_last_try['answer']
            #     res['response']['tts'] = main_phrases.dont_understand_last_try['tts']
            #     res['response']['end_session'] = True

            res['response']['text'] = main_phrases.dont_understand['answer']
            res['response']['tts'] = main_phrases.dont_understand['tts']
        else:
            res['session_state'] = {'error_count': 1}
            res['response']['text'] = main_phrases.dont_understand['answer']
            res['response']['tts'] = main_phrases.dont_understand['tts']

    return res
