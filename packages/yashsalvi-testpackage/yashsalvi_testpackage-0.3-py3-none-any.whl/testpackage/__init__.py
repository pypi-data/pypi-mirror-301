from flask import Flask, request

app = Flask('__main__')

@app.route('/')
def index():
    print("Done")
    return 'Done'

@app.route('/index/<username>')
def index1(username):
    print("index")
    print(username)
    return 'Hello '+str(username)

@app.route('/getName',methods=['GET','POST'])
def getName():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username)
    print(password)
    return 'Hello '+str(username)

if __name__ == '__main__':
    app.run(debug=True)
