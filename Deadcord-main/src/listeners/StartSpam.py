import json
from src.core.Controllers import *
from flask_restful import request
from flask_restful import Resource
from src.core.Util import response


class StartSpam(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "message_content" and "mode" in params:
            print(params["message_content"])
            return start_spam(server_id, params["message_content"], params["mode"])

        else:
            return response(500, "Could not start spam, no message content provided.", 3)
