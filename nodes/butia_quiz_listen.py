#!/usr/bin/env python

import rospy
from std_msgs.msg import String

from butia_quiz.search import answer_question

def publisherAnswer(answer):
    butia_quiz_publisher = rospy.get_param("topics/butia_quiz/quiz_answer", "butia_quiz_answer")

    publisher_answer = rospy.Publisher(butia_quiz_publisher, String, queue_size=1)
    publisher_answer.publish(answer)

def callbackListener(data):
    question = data.data
    rospy.loginfo(question)
    answer = answer_question(question=question)

    publisherAnswer(answer=answer)

def listener():
    butia_quiz_subscriber = rospy.get_param("topics/butia_quiz/quiz_listen", "butia_quiz_listen")
    rospy.Subscriber(butia_quiz_subscriber, String, callback=callbackListener) 

    rospy.init_node("butia_quiz_listener", anonymous=False) 

    rospy.loginfo("Listener function is on")

    rospy.spin()

if __name__ == "__main__":
    listener()

