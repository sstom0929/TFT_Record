import flask
import json
import os
import sys
import tftRecord
import flask_socketio

# Remove old database file, only for debugging
if False and os.path.exists("tftRecord.db"):
    os.remove("tftRecord.db")
    print("Remove Old Database")

# Create database file
if not os.path.exists("tftRecord.db"):
    print("CreateDB...")
    tftRecord.CreateDB()
    tftRecord.InsertDefaultValueIntoMain()

base_dir = "."
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

app = flask.Flask(__name__,
    static_folder=os.path.join(base_dir, 'static'),
    template_folder=os.path.join(base_dir, 'templates'))
socketio = flask_socketio.SocketIO(app)

@app.route("/", methods=['GET'])
def empty():
    return flask.redirect(flask.url_for('admin'))

@app.route("/admin", methods=['GET'])
def admin():
    data = tftRecord.SelectAll()
    return flask.render_template("admin.html", data = data)

@app.route("/updateMain", methods=['POST'])
def updateMain():
    mmrData = json.loads(flask.request.get_data())

    for key in mmrData:
        tftRecord.InsertIntoMain(key, mmrData[key])
    socketio.emit('UpdateMain', mmrData)
    return {'message': '<server>updateMain success'}

@app.route("/insertRecord", methods=['POST'])
def insertRecord():
    recordData = json.loads(flask.request.get_data())
    recordData["ID"] = tftRecord.InsertIntoRecord(recordData["Name"], recordData["Ranking"], recordData["MMR"])
    socketio.emit('InsertRecord', recordData)
    return {'message': '<server>insertRecord success', 'record': recordData}

@app.route("/updateRecord", methods=['POST'])
def updateRecord():
    recordData = json.loads(flask.request.get_data())
    tftRecord.UpdateRecord(recordData["ID"], recordData["Name"], recordData["Ranking"], recordData["MMR"])
    socketio.emit('UpdateRecord', recordData)
    return {'message': '<server>updateRecord success'}

@app.route("/deleteRecord", methods=['POST'])
def deleteRecord():
    recordData = json.loads(flask.request.get_data())
    tftRecord.DeleteRecord(recordData["ID"])
    socketio.emit('DeleteRecord', recordData["ID"])
    return {'message': '<server>deleteRecord success'}

@app.route("/display", methods=['GET'])
def display():
    data = tftRecord.SelectAll()
    return flask.render_template("display.html", data = data)

socketio.run(app)