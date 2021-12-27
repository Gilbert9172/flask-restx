from flask_restx import Namespace

Photo = Namespace(
    name = "Photo",
    description= "사진 전송 API"
)

#-- API Import 
from . import upload, download



