
import template
import json


class TestClient(template.TestingTemplate):

    def test_login_success(self):
        """ Tests that the user is logged in when passing in correct 
            credentials """
        pass


    def test_login_fail(self):
        """ Test that the user is not logged in when passing in incorrect
            details """
        pass


    def test_logout(self):
        """ Tests that the user's session is cleared without fail """
        pass


    def test_session(self):
        """ Test that /session correctly returns relevant session info """
        pass



