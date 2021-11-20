from src.core.Controllers import *
from flask_restful import Resource


class LeaveServer(Resource):

    def get(self, server_id):
        return all_bots_leave(server_id)
