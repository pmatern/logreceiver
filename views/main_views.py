from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('welcome.html', metadata={ 'title': 'Log Receiver Again', 'page': 'hi' })

@main.route('/broken')
def broken():
    return render_template('broken.html', metadata={ 'title': 'Log Receiver Again', 'page': '404' })
