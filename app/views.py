# app/views.py

from flask import flash, redirect, render_template, request, url_for

from app import app



@app.route('/')
def home():
    vars = {
        'title': 'This is the Home Page',
        'body': 'Blah blah blah. This is the body.'
    }
    
    return render_template('app/page.html', vars=vars)


@app.route('/debug/')
def debug():
    vars = {
        'title': 'This is the Home Page',
        'body': 'Blah blah blah. This is the body.'
    }
    
    return render_template('app/debug.html')


@app.errorhandler(404)
def handleBadRequest(err):
    return 'Error 404: page not found', 404


@app.errorhandler(500)
def handleInternalError(err):
    return 'Error 500: internal error', 500
