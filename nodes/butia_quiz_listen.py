#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

from butia_quiz_src.search import answer_question

class ButiaListener():

    def __init__(self):
        self.question, self.answer = None, None

        self.butia_quiz_publisher = None
        self.butia_quiz_subscriber = None

        self._readParameters()

        self.publisher_answer = rospy.Publisher(self.butia_quiz_publisher, String, queue_size=1)

        rospy.init_node("butia_quiz_listen", anonymous=False)

    def waitQuestion(self):
        self.question = rospy.wait_for_message(self.butia_quiz_subscriber, String)
        self.question = self.question.data

    def answerQuestion(self):
        self.answer = answer_question(question=self.question)

    def publishAnswer(self):
        self.publisher_answer.publish(self.answer)

    def _readParameters(self):
        self.butia_quiz_publisher = rospy.get_param("topics/butia_quiz/quiz_answer", "butia_quiz_answer")
        self.butia_quiz_subscriber = rospy.get_param("topics/butia_quiz/quiz_listen", "butia_quiz_listen")

def listener():
    butia_listener = ButiaListener()

    butia_listener.waitQuestion()

    butia_listener.answerQuestion()

    butia_listener.publishAnswer()

if __name__ == "__main__":
    listener()

