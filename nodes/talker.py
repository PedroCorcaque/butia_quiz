#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker(question):
    pub = rospy.Publisher("butia_quiz", String, queue_size=10) # topic butia_quiz
    rospy.init_node("talker", anonymous=True) # node talker

    rospy.loginfo(question)
    pub.publish(question)

if __name__ == "__main__":
    try:
        question = input("Type your question: ")
        talker(question)
    except rospy.ROSInterruptException:
        pass
