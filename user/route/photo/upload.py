#-- Modelus
from flask import request
from flask_restx import Resource, reqparse
from .photo import Photo
from sqlalchemy import text
import app
from datetime import datetime
import time

#-- Upload 과련 Import
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

#-- Parser
parser = reqparse.RequestParser()
parser.add_argument("Authorization", help="Bearer 토큰" , location="headers", required=True)
parser.add_argument("upload", help="사진 업로드", type=FileStorage ,location="files",required=True) # 왜 action='append'를 사용하면 오류가 날까?

#-- SQL
TOKEN_CHECK = "SELECT uid FROM user_token WHERE token=:token "
SAVE_IMAGE = "INSERT INTO image_upload (uid, image_path, image_name) VALUE (:uid, :image_path, :image_name) "


#-- Logic 
IMAGE_TYPE = ['jpg', 'jpeg', 'png', 'gif']

@Photo.expect(parser)
@Photo.route('/upload')
class UploadFile(Resource):
    def post(self):
        """이미지 올리기"""
        #-- 로그인 정보 확인.
        bearer_token = request.headers['Authorization']
        token = {
            "token" : bearer_token.split(' ')[-1]
        }
        check_login = app.engine.execute(text(TOKEN_CHECK), token).first()
        uid = check_login['uid']

        if not check_login:
            return {
                "code" : 500,
                "mesage" : "옳바르지 않은 접근"
            }, 500

        # <class 'werkzeug.datastructures.FileStorage'>        
        images = request.files['upload']           
        
        #-- datetime module을 활용하 파일 이름명 지정해주는 로직. 
        now = datetime.now()

        #-- datetime → 문자열 <class 'str'>
        str_now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')      

        #-- str_now을 struct_time으로
        struct_now = time.strptime(str_now,'%Y-%m-%d %H:%M:%S')

        # time.mktime(struct_type이 들어가야함.) / 시간(초)을 돌려준다.
        t_in_secs = str(int(time.mktime(struct_now)))

        # 파일 이름 고유화.
        img_name = t_in_secs + '_' + secure_filename(images.filename)

        img_info = {
            "uid" : uid,
            "image_path" : './upload/',
            "image_name" : img_name
        }


        img_type = img_name.split('.')[-1]

        if img_type.lower() in IMAGE_TYPE:
            images.save('./upload/{0}'.format(img_name))
            app.engine.execute(text(SAVE_IMAGE),img_info)


        return 200
