from src.core.Util import *
from src.core.Controllers import *
from flask_restful import Resource


class SpeakTokens(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "message_content" in params:

            return all_bots_speak(server_id, params["message_content"])

        else:
            return response(500, "No parameters provided.", 2)