#!/usr/bin/env python
import rospy
from std_msgs.msg import String

from butia_quiz.search import answer_question

def listener_callback(data):
    rospy.loginfo("Your question was: %s" % data.data)
    data = data.data
    ans = answer_question(question=data)
    if ans != '':
        rospy.loginfo("Your answer is: %s" % ans)
    else:
        rospy.loginfo("I\'m sorry. I\'m afraid I do not know the answer for your question")

def listener():
    rospy.loginfo("Iniciou")
    rospy.init_node("butia_quiz_listener") # node butia_quiz_listener
    rospy.Subscriber("butia_quiz", String, callback=listener_callback) # topic butia_quiz

    rospy.spin()

if __name__ == "__main__":
    listener()