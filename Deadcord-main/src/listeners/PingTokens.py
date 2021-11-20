from src.core.Controllers import *
from flask_restful import Resource


class PingTokens(Resource):

    def get(self):
        return ping_all_tokens()
