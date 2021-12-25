#-- Modules
from flask import request
from flask_restx import Resource, reqparse
from .user import User
from sqlalchemy import text
import app

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="아이디", location="json", required=True)
parser.add_argument("password", help="비밀번호", location="json", required=True)
parser.add_argument("gender", help="성별", location="json", required=True)
parser.add_argument("birth", help="생년월일", location="json", required=True)
parser.add_argument("phone", help="전화번호", location="json", required=True)
parser.add_argument("email", help="이메일", location="json", required=True)
parser.add_argument("name", help="이름", location="json", required=True)

#-- SQL
SIGNUP_SQL = "INSERT INTO user_account (user_id, password, gender, birth, phone, email, name) \
VALUE (:user_id, :password, :gender, :birth, :phone, :email, :name)"

CHECK_ID = "SELECT user_id FROM user_account WHERE (user_id=:user_id)"

CHECK_EMAIL= "SELECT email FROM user_account WHERE (email=:email)"

#-- Logic
@User.route('/signup')
@User.expect(parser)
@User.response(200, "Success")
@User.response(500, "Server Error")
class UserSignUp(Resource):
    def post(self):
        """회원가입"""

        user_info = {
            'user_id' : request.json['user_id'],
            'password' : request.json['password'],
            'gender' : request.json['gender'],
            'birth' : request.json['birth'],
            'phone' : request.json['phone'],
            'email' : request.json['email'],
            'name' : request.json['name']
        }
        
        # 동일한 아이디가 존재할 경우
        check_id = app.engine.execute(text(CHECK_ID),{'user_id':user_info['user_id']}).first()
        if check_id:
            return {
                "message" : "존재하는 아이디입니다."
            }, 500
    
        # 동일한 이메일이 존재할 경우
        check_email = app.engine.execute(text(CHECK_EMAIL), {'email':user_info['email']}).first()
        if check_email:
            return {
                'message' : "존재하는 이메일 입니다."
            }, 500

        # 모두 정상일 경우 
        user_sign_up = app.engine.execute(text(SIGNUP_SQL),user_info)

        return {
            'code': 'Success',
            'message': '회원가입을 축하드립니다.'
        }, 200