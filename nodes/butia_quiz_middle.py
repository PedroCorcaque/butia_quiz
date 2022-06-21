#!/usr/bin/env python

import rospy

from butia_quiz.butia_quiz_sm import ButiaQuizSM

if __name__ == "__main__":
    withQuestion, withAnswer = False, False

    rospy.init_node("butia_quiz", anonymous=False)

    quiz = ButiaQuizSM()

    if True: # Some action
        withQuestion = quiz.toListen()

    if withQuestion:
        withAnswer = quiz.toReseach()

    if withAnswer:
        res = quiz.toTalk()

        if not res:
            rospy.loginfo("Problem to talk the answer!")
        rospy.loginfo("toTalk ok")

