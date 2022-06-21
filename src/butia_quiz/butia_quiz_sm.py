import rospy
from std_msgs.msg import String

import time

from butia_speech.srv import SpeechToText, SynthesizeSpeech


class ButiaQuizSM():

    def __init__(self):
        self.question = None
        self.answer = None

        self.butia_quiz_answer = None
        self.butia_quiz_listen = None
        self._readParameters()

        self.pub = rospy.Publisher(self.butia_quiz_listen, String, queue_size=1)

    def toListen(self):
        response = False

        rospy.wait_for_service("/butia_speech/asr/transcribe")
        try:
            speech_to_text = rospy.ServiceProxy("/butia_speech/asr/transcribe", SpeechToText)
            self.question = speech_to_text()
            print("The question is: %s" % self.question.text)

            if response != '':
                response = True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            
        return response
    
    def _waitResponse(self):
        while self.answer is None:
            self.answer = rospy.wait_for_message(self.butia_quiz_answer, String)
            self.answer = self.answer.data
            rospy.sleep(0.4)

    def toReseach(self):
        response = False

        try:
            self.question = self.question.text
            rospy.loginfo("Your question is: %s" % self.question)

            self.pub.publish(self.question)

            self._waitResponse()

            rospy.loginfo("Your answer is: %s" % self.answer)

            response = True
        except rospy.ROSInternalException as e:
            print(e)
        
        return response

    def toTalk(self):
        response = False
        rospy.wait_for_service("butia/synthesize_speech")
        try:
            synthesize_speech = rospy.ServiceProxy("butia/synthesize_speech", SynthesizeSpeech)
            synthesize_speech(self.answer, "en")

            if response != '':
                response = True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

        return response

    def _readParameters(self):
        self.butia_quiz_answer = rospy.get_param("topics/butia_quiz/quiz_answer", "butia_quiz_answer")
        self.butia_quiz_listen = rospy.get_param("topics/butia_quiz/quiz_listen", "butia_quiz_listen")
