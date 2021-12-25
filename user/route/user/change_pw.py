#-- Modules 
from flask import request
from flask_restx import reqparse, Resource
from .user import User
from sqlalchemy import text
import app


#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="사용자 아이디", location="json", required=True)
parser.add_argument("new_pw", help="새로운 비밀번호", location="json", required=True)
parser.add_argument("check_pw", help="새로운 비번 확인", location="json", required=True)


#-- SQL
CHANGE_PW = "UPDATE user_account SET password=:new_pw WHERE user_id=:user_id "


#-- Logic
@User.expect(parser)
@User.response(200, 'Success')
@User.response(404, 'Page Not Found')
@User.response(500, 'Server Error')
@User.route('/change-pw')
class NewPw(Resource):
    def put(self):
        """비밀번호 변경"""
        if request.json['new_pw'] != request.json['check_pw']:
            return {
               "message" : "비밀번호가 일치하지 않습니다." 
            }, 500
        
        new_pw = {
            'new_pw' : request.json['new_pw'],
            'user_id' : request.json['user_id']
        }

        pw_row = app.engine.execute(text(CHANGE_PW), new_pw)

        return {
            'code' : 200,
            'message' : "비밀번호가 변경되었습니다.",
            'response' : {
                'user_id' : request.json['user_id'],
            }
        }