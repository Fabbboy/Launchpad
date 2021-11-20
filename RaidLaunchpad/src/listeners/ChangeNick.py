from src.core.Util import *
from src.core.Endpoints import *
from src.core.Controllers import *
from flask_restful import Resource


class ChangeNick(Resource):

    def post(self, server_id):
        params = json.loads(request.get_data().decode())

        if "nick" in params and not None or not "":

            nick = clean_input(params["nick"])[0]

            return change_all_bots_nick(server_id, nick)

        else:
            return response(500, "No nickname provided.", 3)
