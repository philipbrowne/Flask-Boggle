from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, flash, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
app.config['TESTING'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
toolbar = DebugToolbarExtension(app)

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

BOGGLE_GAME = Boggle()
words = BOGGLE_GAME.words


@app.route('/', methods=['GET'])
def index():
    """Show Homepage for Flask Boggle"""
    board = BOGGLE_GAME.make_board()
    session['board'] = board
    if 'high_score' in session and type(session['high_score']) is int:
        high_score = session['high_score']
    else:
        session['high_score'] = 0
        high_score = 0
    if 'times_played' in session:
        times_played = session['times_played']
    else:
        session['times_played'] = 0
        times_played = 0
    return render_template('index.html', board=board, high_score=high_score, times_played=times_played)


@app.route('/', methods=['POST'])
def make_guess():
    """Evaluates word submitted by Input and returns whether word is valid and part of current board"""
    guess = request.json.get('guess').lower()
    board = session.get('board')
    if board:
        response = {'result': BOGGLE_GAME.check_valid_word(board, guess)}
    else:
        return 'Sorry no board!'
    return jsonify(response)


@app.route('/gameover', methods=['POST'])
def end_game():
    """Receives updated high score and number of times played after game has finished"""
    session['high_score'] = request.json.get('high_score')
    session['times_played'] += 1
    print(session['high_score'])
    print(session['times_played'])
    response = {
        'times_played': session['times_played'],
        'high_score': session['high_score'],
    }
    return jsonify(response)
