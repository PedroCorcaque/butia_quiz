#!/usr/bin/env python
import wolframalpha
import requests
from html import unescape
from .pseudo_nlp import find_question
import json
import rospkg

PKG_DIR = rospkg.RosPack().get_path('butia_quiz')

app_id = '2GA6V9-T89KR7AJ2E'

with open(PKG_DIR+'/questions/doris_personal_questions.json') as json_file:
    doris_personal_questions = json.load(json_file)["questions"]

def ask_wolfram(question):

    client = wolframalpha.Client(app_id)
    try:
        res = client.query(question)
        if res['@success'] == 'false':
            return ''
        else:
            answer = next(res.results).text
            return answer
    except:
        return ''

def ask_google(question):
    question = question.replace(' ', '%20')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }

    r = requests.get(
        'https://www.google.com/search?q={:s}'.format(question),
        headers=headers
    )
     
    answer = ''
    # classe grande principal
    index = r.text.find('="Z0LcW XcVN5d')
    if index != -1:
        answer = r.text[index:]
        answer = answer.replace('<a', '')
        answer = answer.replace('</a>', '')
        index = answer.find('>')
        answer = answer[index+1:]
        index = answer.find('<')
        answer = answer[:index]
    if answer == '':
        # classe encontrada por vezes em palavras grandes
        index = r.text.find('data-tts-answer=')
        # porque se achar -1 pegava do começo
        if (index != -1):
            answer = r.text[index+1:]
            index = answer.find('"')
            answer = answer[:index]
    if answer == '':
        # classe do subanswero
        index = r.text.find('class="hgKElc"')
        if index != -1:
            answer = r.text[index:]
            index = answer.find('>')
            answer = answer[index+1:]
            index = answer.find('</span>')
            answer = answer[:index]
    if answer == '':
        # classe de endereços
        index = r.text.find('class="MWXBS"')
        if index != -1:
            answer = r.text[index:]
            index = answer.find('>')
            answer = answer[index+1:]
            index = answer.find('</div>')
            answer = answer[:index]
    # se não encontrar nada...
    if answer != '':
        answer = answer.replace('<b>', '')
        answer = answer.replace('</b>', '')
        if '>' in answer:
            index = answer.find('>')
            answer = answer[index+1:]

    answer = unescape(answer)
    return answer

def ask_doris(question):
    question_obj = find_question(question, doris_personal_questions)
    if question_obj['question'] == '':
        # answer = "I'm afraid I don't know the answer."
        answer = ''
    else: 
        answer = question_obj['answer']

    return answer

def answer_question(question):
    answer = ''

    question = question.lower()
    # if 'oxford' in question:
    #     # return ask_doris(question)
    #     answer = ask_doris(question)
    #     if answer != '':
    #         return answer
    
    # if 'rio grande do sul' in question:
    #     # return ask_doris(question)
    #     answer = ask_doris(question)
    #     if answer != '':
    #         return answer
    
    # if answer == '':
    answer = ask_google(question)
    
    if answer != '':
        return answer
    else:
        answer = ask_doris(question)
        if answer != '':
            return answer
        else:
            answer = ask_wolfram(question)
            if answer != '':
                return answer
            else:
                return 'I\'m sorry. I\'m afraid I do not know the answer for your question'
