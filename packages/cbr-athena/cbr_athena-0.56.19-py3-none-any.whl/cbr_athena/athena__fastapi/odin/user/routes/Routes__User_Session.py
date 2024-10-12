from fastapi import Depends, Request, Security

from cbr_athena.athena__fastapi.CBR__Session_Auth import cbr_session_auth, api_key_header
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTE_PATH__USER_SESSION        = 'user-session'
EXPECTED_ROUTES__USER_SESSION   = ['/session-details']



class Routes__User_Session(Fast_API_Routes):

    tag : str = ROUTE_PATH__USER_SESSION

    def session_data(self, request: Request, session_id: str = Security(api_key_header)):
        return cbr_session_auth.session_data(request, session_id)


    def chat_debug(self):
        from cbr_athena.config.CBR__Config__Athena import cbr_config_athena
        return {'aws_disabled': cbr_config_athena.aws_disabled()}

    def setup_routes(self):
        self.add_route_get(self.session_data)
        self.add_route_get(self.chat_debug)