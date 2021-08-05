from unittest import TestCase
from app import app
from flask import Flask, request, render_template, redirect, session, flash, make_response, jsonify
from boggle import Boggle

BOGGLE_GAME = Boggle()


class FlaskTests(TestCase):
    def test_index(self):
        """Tests front page of board"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Flask Boggle!</h1>', html)
    # TODO -- write tests for every view function / feature!

    def test_guess(self):
        """Tests guessing from post request"""
        with app.test_client() as client:
            res = client.get('/')
            with client.session_transaction() as change_session:
                change_session['board'] = [['A', 'N', 'J', 'Y', 'D'],
                                           ['V', 'X', 'V', 'M', 'K'],
                                           ['J', 'K', 'X', 'O', 'B'],
                                           ['R', 'K', 'Y', 'A', 'X'],
                                           ['E', 'W', 'O', 'T', 'I']]
            res = client.post('/', json={"guess": "tow"})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('ok', html)

    def test_guess_not_word(self):
        """Tests a word guess where the guess is not part of words dictionary"""
        with app.test_client() as client:
            res = client.get('/')
            with client.session_transaction() as change_session:
                change_session['board'] = [['A', 'N', 'J', 'Y', 'D'],
                                           ['V', 'X', 'V', 'M', 'K'],
                                           ['J', 'K', 'X', 'O', 'B'],
                                           ['R', 'K', 'Y', 'A', 'X'],
                                           ['E', 'W', 'O', 'T', 'I']]
            res = client.post('/', json={"guess": "fasdfasdf"})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('not-word', html)

    def test_guess_not_in_board(self):
        """Runs test where word is not part of board"""
        with app.test_client() as client:
            res = client.get('/')
            with client.session_transaction() as change_session:
                change_session['board'] = [['A', 'N', 'J', 'Y', 'D'],
                                           ['V', 'X', 'V', 'M', 'K'],
                                           ['J', 'K', 'X', 'O', 'B'],
                                           ['R', 'K', 'Y', 'A', 'X'],
                                           ['E', 'W', 'O', 'T', 'I']]
            res = client.post('/', json={"guess": "groovy"})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('not-on-board', html)

    def test_game_over(self):
        """Runs test for End-Game Route"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['times_played'] = 4
            res = client.post('/gameover', json={'high_score': '4'})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['times_played'], 5)
            self.assertEqual(session['high_score'], '4')
