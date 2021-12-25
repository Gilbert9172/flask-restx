#-- Module
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from sqlalchemy import create_engine
from user.route.user.user import User
from dotenv import load_dotenv
import os


#-- App성성
app = Flask(__name__)

load_dotenv()
cors = CORS()
cors.init_app(app)

#-- API Swagger 설정
api = Api(
    app,
    version='0.1',
    title = "todo"
)


#-- 데이터 베이스 주소.
DB_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}?charset={os.getenv('MYSQL_CHARSET')}"
port = int(os.getenv('PORT'))

#-- MySQL과 연결다리.
engine = create_engine(DB_URL, encoding="utf-8")

#-- app객체의 DB설정
app.db = engine

#-- api 추가
URL_PREFIX ='/todo'
api.add_namespace(User, URL_PREFIX + '/auth')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0" ,port=port)