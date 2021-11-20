from src.core.Util import *
from flask_restful import request
from src.core.Controllers import *
from flask_restful import Resource


class JoinServer(Resource):

    def post(self):
        params = json.loads(request.get_data().decode())

        if "invite" in params:

            invite = clean_input(params["invite"])[0]

            if "discord" in invite:

                return all_bots_join(invite)

            else:
                return response(400, "Invalid server invite, include full invite URL.")
        else:
            return response(500, "Could not join server, missing parameters.", 3)
