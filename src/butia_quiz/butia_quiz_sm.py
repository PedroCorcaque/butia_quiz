import rospy

class ButiaQuizSM():

    def __init__(self):
        self.question = None
        self.answer = None

        self.butia_quiz_publisher = None
        self.butia_quiz_subscriber = None
        self._readParameters()

    def toListen(self):
        response = False
        """ 
        Call the service of the stt
        Publish the question in text format in butia_quiz topic
        """
        return response

    def toReseach(self):
        response = False
        """ 
        Listen the question in text format in butia_quiz topic
        Find the answer
        Publish the question in text format in butia_quiz topic
        """
        return response

    def toTalk(self):
        response = False
        """ 
        Call the service of the tts
        """
        return response

    def _readParameters(self):
        self.butia_quiz_publisher = rospy.get_param("topics/butia_quiz/quiz_answer", "butia_quiz_publisher")
        self.butia_quiz_subscriber = rospy.get_param("topics/butia_quiz/quiz_listen", "butia_quiz_subscriber")
