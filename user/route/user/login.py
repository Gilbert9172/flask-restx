#-- Module
from flask import request
from flask_restx import Resource, reqparse
from .user import User
from sqlalchemy import text
import app, jwt

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="아이디 입력", location="json", required=True)
parser.add_argument("password", help="암호 입력", location="json", required=True)

#-- SQL
CHECK_ID =  "SELECT id, user_id,password FROM user_account WHERE (user_id=:user_id)"
TOKEN_INSERT = 'INSERT INTO user_token(uid, token) VALUES(:uid, :token)'
TOKEN_DELETE = 'DELETE FROM user_token WHERE uid=:uid'

#-- Logic
@User.expect(parser)
@User.response(200, 'Success') 
@User.response(404, 'Page Not Found')
@User.response(500, 'Internal Server Error')
@User.route('/login')
class Login(Resource):
    def post(self):
        """로그인"""
        # GET요청으로 할 경우 URL에 모든 정보가 넘어가서 POST로 요청을 보내야한다.
        
        #-- 입력한 아이디
        login_id = {
            'user_id' : request.json['user_id']
        }

        #-- DB에 있는 아이디, 비밀번호
        db_row= app.engine.execute(text(CHECK_ID),login_id).first()

        uid = db_row[0]
        user_id = db_row[1]
        pw = db_row[2]
        print(pw)
        #-- DB에 있는 아이디와 일치하는지.
        if login_id['user_id'] != user_id:
            return {
                "message" : "등록된 사용자가 없습니다."
            }, 500
        
        elif request.json['password'] != pw:
            return {
                "message" : "잘못된 비밀번호 입니다."
            }, 500

        #-- 로그인 / JWT 생성
        token = jwt.encode({'user_id':user_id}, "크리스마스", algorithm='HS256')

        token_info = {
            'uid' : uid,
            'token' : token
        }

        token_insert = app.engine.execute(text(TOKEN_INSERT), token_info)

        return {
            'code' : 200,
            'message' : "로그인 성공",
            'response' : {
                'token' : token
            }
        }, 200
        