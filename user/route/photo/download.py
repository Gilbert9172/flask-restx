#-- Modules
from flask import request
from flask_restx import Resource, reqparse
from .photo import Photo
from sqlalchemy import text
import app
from PIL import Image

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("user_id", help="사용자 아이디", location="headers", required=True)
parser.add_argument("search", help="검색어", location="headers", required=True)

#-- SQL
FIND_IMG = "SELECT IU.image_path, IU.image_name FROM user_account AS UA LEFT JOIN image_upload AS IU ON UA.id = IU.uid WHERE user_id=:user_id "


@Photo.response(200, 'Success') 
@Photo.response(404, 'Page Not Found')
@Photo.response(500, 'Internal Server Error')
@Photo.expect(parser)
@Photo.route('/download')
class Download(Resource):
    def get(self):

        """이미지 다운"""

        row_info = {
            "user_id" : request.headers['user_id'],
        }
        
        img_info = app.engine.execute(text(FIND_IMG),row_info).all()

        for i in img_info:
            
            if request.headers['search'] in i['image_name']:

                img_path = i['image_path']+i['image_name']

                image = Image.open(img_path)

                image.show()

        return 200