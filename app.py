
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

cntr = []
ip = []
@app.route('/')
def sessions():
    if request.remote_addr not in ip:
        ip.append(str(request.remote_addr))
        print('.........')
    return render_template('index.html', value=0)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    global cntr
    global ip
    if request.remote_addr not in ip:
        ip.append(str(request.remote_addr))
        cntr.append(0)
    print('received my event: ', json, type(json))
    json = {'ip': ip, 'cntr': cntr}
    print(json['ip'])
    #print(json['cntr'], [json['ip'].index(str(request.remote_addr))])
    print(json['cntr'], json['ip'])
    try:
        json['cntr'][json['ip'].index(str(request.remote_addr))] += 1
    except IndexError:
        cntr.append(0)
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host='192.168.1.70')