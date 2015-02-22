import os
from pymongo import MongoClient
from bson import ObjectId
from flask import request
from flask.ext.restful import Resource

from calabaza import mongo
from calabaza import connection
from calabaza import userModel

from calabaza.modules.calabaza_game import calabaza_game


# class MongoConnection():
#     def connect():
#         client = MongoClient()
#         db = client.emonitor
#         renderJobs = db.renderJobs
#         return renderJobs

class GameListApi(Resource):
    def get(self):
        #collection = connection()
        #user = userModel()
        #user['username'] = u'testname'
        #user['email'] = u'user@user.com'
        #user['password'] = u'1234'

        #print (user.safe())

        images = [
            "static/weather/calabaza_nubes.gif",
            "static/weather/calabaza_llovizna.gif",
            "static/ground/calabaza_tierra_normal.gif",
            "static/base/calabaza_base.gif",
            "static/health/calabaza_pachucho.gif",
            "static/faces/calabaza_durmiendo_anim.gif",
            "calabaza_gorro_navidad.gif"
        ]

        resp = {
            "image":images,
            "text":"113",
            "background":"rgb(3, 24, 17)",
            "anim":"animb"
        }

        return resp, 200

    def post(self):
        renderJobs = MongoConnection.connect()
        data = emonitor_data()
        data.name = request.form['name']
        data.status = request.form['status']
        iid=renderJobs.insert(data.array())

        return {'uuid':str(iid)}, 200

class GameActionApi(Resource):
    def get(self, job_id=None):
        renderJobs = MongoConnection.connect()
        data_client=renderJobs.find_one({'_id':ObjectId(job_id)})
        emon_data = emonitor_data()
        emon_data.name = data_client['name']
        emon_data.status = data_client['status']
        emon_data.engine = data_client['engine']
        emon_data.freestyle = data_client['freestyle']
        emon_data.compositor = data_client['compositor']
        emon_data.sequencer = data_client['sequencer']
        emon_data.frame_start = data_client['frame_start']
        emon_data.frame_end = data_client['frame_end']
        emon_data.frame_current = data_client['frame_current']

        return emon_data.array(), 200

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ['png']

    def patch(self, job_id=None):
        from werkzeug import secure_filename

        renderJobs = MongoConnection.connect()
        emon_data = emonitor_data()
        emon_data.status = request.form['status']
        emon_data.engine = request.form['engine']
        emon_data.freestyle = request.form['freestyle']
        emon_data.compositor = request.form['compositor']
        emon_data.sequencer = request.form['sequencer']
        emon_data.frame_start = request.form['frame_start']
        emon_data.frame_end = request.form['frame_end']
        emon_data.frame_current = request.form['frame_current']

        try:
            file = request.files.get('images')
            if file and self.allowed_file(file.filename):
                filename = "{0}.png".format(job_id)
                file.save(os.path.join('/home/gabriel/dev/emonitor/eMonitor/emonitor/emonitor/static/thumbnails/', filename))
        except:
            print ("Error reading file")

        key = {'_id':ObjectId(job_id)}
        renderJobs.update(key, {'$set':emon_data.array_update()})
