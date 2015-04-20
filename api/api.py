#!flask/bin/python
from flask import Flask, jsonify, abort, request, Response, make_response, url_for
from flask_restful import reqparse
from bogglesolver.solve_boggle import SolveBoggle
from bogglesolver.load_english_dictionary import Edict
# from flask.ext.api import FlaskAPI

app = Flask(__name__, static_url_path = "")

edict = Edict()
edict.read_dictionary()
 

@app.errorhandler(400)
def bad_request(error=None):
    # TODO: Remove this if/else statement once converting to reqparse is complete
    if 'data' in dir(error):
        message = error.data['message']  # error is being generated from reqparse in flask-restful
    else:
        message = "Bad request"  # error is being generated from flask request.values[] and has no message
    message = {
        "status": 400,
        "message": message,
        'errors': ["Bad Request"]
    }
    return jsonify(message)

# @app.errorhandler(400)
# def bad_request(error):
#     print(error)
#     return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def generate_board(rows, columns):
    solver = SolveBoggle()
    solver.set_board(columns, rows)
    return ''.join(solver.boggle.boggle_array)

def get_board_response(rows, columns):
    board = generate_board(rows, columns)
    url = url_for("solution", rows=rows, columns=columns, board=board)
    return jsonify(dict(board=board, solution=url))

@app.route("/")
def play():
    rp = reqparse.RequestParser()
    rp.add_argument("rows", default=4, type=int, required=True)
    rp.add_argument("columns", default=4, type=int)
    req = rp.parse_args()
    return get_board_response(req["rows"], req["columns"])

@app.route("/<int:rows>/<int:columns>", methods=['GET'])
def get_board(rows, columns):
    return get_board_response(rows, columns)

@app.route("/<int:rows>/<int:columns>/<board>", methods=['GET'])
def solution(rows, columns, board):
    solver = SolveBoggle()
    solver.set_board(columns, rows, board)
    words = solver.solve(edict)
    return jsonify(dict(words=words))

@app.before_request
def log_request():
    if app.debug:
        print(request)
        print(request.values)

@app.after_request
def log_request(response):
    if app.debug:
        print("Response is: ")
        print(response)
        print("Data is:")
        print(response.data)
    return response
    
if __name__ == '__main__':
    app.run(debug = True)
