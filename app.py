from flask import Flask, request, Response, jsonify
import base64
from werkzeug.utils import secure_filename

from db import db,Img
from flask_marshmallow import Marshmallow


app = Flask(__name__)
ma = Marshmallow()
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

class ImageSchema(ma.SQLAlchemyAutoSchema):
     class Meta:
          model = Img

img_schema = ImageSchema()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200


@app.route('/<int:id>')
def get_img(id):
    img = db.session.get(Img, id)
    if not img:
        return 'Img Not Found!', 404
    image_data = base64.b64encode(img.img).decode('utf-8')
    return Response(base64.b64decode(image_data), mimetype=img.mimetype)

if __name__ == '__main__':
     
    with app.app_context():
            db.create_all()

            from db import db

    app.run(debug=True)