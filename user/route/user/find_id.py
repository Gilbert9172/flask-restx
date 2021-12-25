#-- Module
from flask import request
from flask_restx import Resource, reqparse
from .user import User
from sqlalchemy import text
import app

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("name", help="이름", location="json", required=True)
parser.add_argument("birth", help="생년월일", location="json", required=True)
parser.add_argument("phone", help="전화번호", location="json", required=True)

#-- SQL
CHECK_USER = "SELECT user_id FROM user_account WHERE name=:name AND birth=:birth AND phone=:phone "

#-- Logic
@User.expect(parser)
@User.response(200, 'Success') 
@User.response(404, 'Page Not Found')
@User.response(500, 'Internal Server Error')
@User.route('/find-id')
class FindId(Resource):
    def post(self):
        """아이디 찾기"""
        check_info = {
            'name' : request.json['name'],
            'birth' : request.json['birth'],
            'phone' : request.json['phone']
        }

        find_row = app.engine.execute(text(CHECK_USER), check_info).first()

        find_id = find_row[0]

        if not find_row : 
            return {
                'code' : 500,
                'message' : "존재하는 회원정보가 없습니다."
            }, 500
        
        return {
            'code' : 200,
            'message' : "사용자 아이디 찾기 성공",
            'response' : {
                'user_id' : find_id
            }
        },200 