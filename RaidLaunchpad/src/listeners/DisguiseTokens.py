from src.core.Controllers import *
from flask_restful import Resource


class DisguiseTokens(Resource):

    def get(self, server_id):

        return disguise_all_bots(server_id)
