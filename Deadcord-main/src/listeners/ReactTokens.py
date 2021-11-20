from src.core.Util import *
from src.core.Controllers import *
from flask_restful import request
from flask_restful import Resource


class ReactTokens(Resource):

    def post(self):
        params = json.loads(request.get_data().decode())

        if "channel_id" and "message_id" and "emoji" in params:

            channel_id = params["channel_id"]
            message_id = params["message_id"]
            emoji = params["emoji"]

            return all_bots_react(channel_id, message_id, emoji)

        else:
            return response(500, "No parameters provided.", 2)
