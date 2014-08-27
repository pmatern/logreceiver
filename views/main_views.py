from flask import Blueprint, render_template, redirect, url_for
from integrations.static.Tools import Tools
from HugUtils.grouphug_constants import GroupHugPages

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('kpi.overview'))

@main.route('/broken')
def broken():
    return render_template('broken.html', metadata=GroupHugPages.metadata_404())


@main.route('/tools')
def tools():
    print Tools.tools()
    return render_template('tools.html', metadata=Tools().metadata(), tools=Tools().tools())

@main.route('/nigeme/<word>')
def nige_me(word="boners"):
    text = word
    return render_template('nigel.html', text=text)

@main.route('/magic')
def changelog():
    lines = Gitlog().get_log()
    return render_template('changelog.html', name='Changelog', lines=lines)
