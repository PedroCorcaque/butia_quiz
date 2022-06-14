#!/usr/bin/env python

import rospy
from std_msgs.msg import String

from butia_quiz.search import answer_question

def publisherAnswer(answer):
    publisher_answer = rospy.Publisher("butia_quiz_answer", String, queue_size=1)
    publisher_answer.publish(answer)

def callbackListener(data):
    question = data.data
    rospy.loginfo(question)
    answer = answer_question(question=question)

    publisherAnswer(answer=answer)

def listener():
    rospy.init_node("butia_quiz") 
    rospy.Subscriber("butia_quiz_listen", String, callback=callbackListener) 
    
    rospy.spin()

if __name__ == "__main__":
    listener()

