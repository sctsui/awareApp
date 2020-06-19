from flask import Flask, request
import json
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')

App = Query()

@app.route('/', methods=['GET'])
def get_app_versions():
    print(f'Request: {request}')
    return json.dumps({"items": db.all()})


####### Developer API ######

#post new app (version and link)
@app.route('/<appId>/<version>', methods = ['POST'])
def post_newapp():
    link = request.get_json()
    db.insert({'appId': appId, 'version': version, 'link': link, 'changelog': changelog})
    return 201

#post changlog of specific app
@app.route('/changelog/<appId>/<version>', methods = ['POST'])
def post_changelog():
    changelog = request.get_json()
    db.update({'changelog': changelog}, (App.appId == appId & App.version == version) )
    return 200


###### Client API ######

#return changelog of specific app
@app.route('/changelog/<appId>', methods = ['GET'])
def get_changelog():
    apps = db.search(Query().appId == appId)
    if apps:
        return apps.changelog()
    return 200

#return notification message with install link (of app name/version)
@app.route('/<appId>/<version>', methods = ['GET'])
def get_changelog():
    apps = db.search(App.appId == appId & App.version == version)
    if apps:
        msg = "Please download " + appId + " using the link provided"
        return json.dumps({"notification": msg,"link": apps.link()})
    return 200

#get all versions of app
@app.route('/versions/<appId>', methods = ['GET'])
def get_changelog():
    apps = db.search(Query().appId == appId)
    if apps:
        return apps
    return 200

if __name__ == '__main__':
    app.run()
