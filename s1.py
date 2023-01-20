from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def myapp():
    message = "To use this app: %s/add?x=value&y=value" % request.base_url
    return message

@app.route('/add')
def add():
    # Checking that both parameters have been supplied
    if not 'x' in request.args:
        return "x value is missing"
    if not 'y' in request.args:
        return "y value is missing"
    
    # Make sure they are numbers too
    try:
        x = float(request.args['x'])
        y = float(request.args['y'])
    except:
        return "x and y should be numbers"
    return str(x+y)