#!/usr/bin/env python

import rospy
from std_msgs.msg import String

# ------------------------

import requests
from html import unescape

def _ask_google(question: str):
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

def answer_question(question):
    question = question.lower()

    answer = _ask_google(question)
    
    return answer

# ------------------------

def listener_callback(data):
    rospy.loginfo("Your question was: %s" % data.data)
    data = data.data
    ans = answer_question(question=data)
    if ans != '':
        rospy.loginfo("Your answer is: %s" % ans)
    else:
        rospy.loginfo("I\'m sorry. I\'m afraid I do not know the answer for your question")

def listener():
    rospy.init_node("butia_quiz_listener") # node butia_quiz_listener
    rospy.Subscriber("butia_quiz", String, callback=listener_callback) # topic butia_quiz

    rospy.spin()

if __name__ == "__main__":
    listener()