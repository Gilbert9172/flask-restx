#-- Module
from flask import request
from flask_restx import Resource, reqparse
from .user import User
from sqlalchemy import text
import app

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="아이디", location="json", required=True)
parser.add_argument("birth", help="생년월일", location="json", required=True)
parser.add_argument("phone", help="전화번호", location="json", required=True)


#-- SQL
CHECK_USER = "SELECT * FROM user_account  WHERE user_id=:user_id AND birth=:birth AND phone=:phone"


#-- Logic
@User.expect(parser)
@User.response(200, 'Success') 
@User.response(404, 'Page Not Found')
@User.response(500, 'Internal Server Error')
@User.route('/find-pw')
class FindPw(Resource):
    def post(self):
        """비밀번호 찾기"""

        user_info =  {
            'user_id' : request.json['user_id'],
            'birth' : request.json['birth'],
            'phone' : request.json['phone']
        }

        user_row = app.engine.execute(text(CHECK_USER), user_info).first()
        
        if not user_row :
            return {
                'code' : 500,
                'message' : "올바르지 않은 정보",
                'response' : None
            }, 500
        
        return {
            'code' : 200,
            'message' : "비밀번호 찾기 성공",
            'response' : {
                'user_id' : user_info['user_id'],
                'birth' : user_info['birth'],
                'phone' : user_info['phone']
            }
        }