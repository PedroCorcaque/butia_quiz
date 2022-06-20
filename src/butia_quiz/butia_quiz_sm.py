import rospy
from std_msgs.msg import String

from butia_speech.srv import SpeechToText, SpeechToTextResponse

class ButiaQuizSM():

    def __init__(self):
        self.question = None
        self.answer = None

        self.butia_quiz_answer = None
        self.butia_quiz_listen = None
        self._readParameters()

    def toListen(self):
        response = False

        rospy.wait_for_service("/butia_speech/asr/transcribe")
        try:
            synthesize_speech = rospy.ServiceProxy("/butia_speech/asr/transcribe", SpeechToText)
            self.question = synthesize_speech()
            print("The question is: %s" % self.question.text)

            if response != '':
                response = True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            
        return response
    
    def _waitResponse(self):
        while self.answer is None:
            self.answer = rospy.wait_for_message(self.butia_quiz_answer, String)
            rospy.sleep(0.4)

    def _sendQuestion(self):
        pub = rospy.Publisher(self.butia_quiz_listen, String, queue_size=1)

        pub.publish(self.question)

    def toReseach(self):
        response = False

        try:
            self.question = "who is the president of brazil?" # self.question.text
            rospy.loginfo("Your question is: %s" % self.question)
            
            self._sendQuestion()

            rospy.loginfo("Your question was published")

            self._waitResponse()

            rospy.loginfo("Your answer is: %s" % self.answer.data)
        except rospy.ROSInternalException as e:
            print(e)
        
        return response

    def toTalk(self):
        response = False
        """ 
        Call the service of the tts
        """
        return response

    def _readParameters(self):
        self.butia_quiz_answer = rospy.get_param("topics/butia_quiz/quiz_answer", "butia_quiz_answer")
        self.butia_quiz_listen = rospy.get_param("topics/butia_quiz/quiz_listen", "butia_quiz_listen")
