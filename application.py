from flask import render_template, Flask
from views import main
#import newrelic.agent
import os
import socket

#if socket.gethostname() == 'jcint-soa-kegbot-dev.phx1.jivehosted.com':
#    newrelic.agent.initialize('/opt/group_hug/newrelic.ini', environment='production')
#else:
#    newrelic.agent.initialize('%s/newrelic.ini' % os.environ['GH_HOME'], environment='development')


app = Flask('log_receiver_again')
app.config.from_object('config')

app.register_blueprint(main)

app.debug = False
@app.errorhandler(503)
def service_unavailable(error):
    return render_template('broken.html', metadata={
            'title': 'Log Receiver Again',
            'page': '503',
        }), 503

@app.errorhandler(404)
def not_found(error):
    return render_template('broken.html', metadata={
            'title': 'Log Receiver Again',
            'page': '404',
        }), 404

# thanks http://stackoverflow.com/questions/13317536
@app.route('/help')
def list_routes():
    from flask import url_for, make_response
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:30s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    response = make_response('\n'.join(sorted(output)))
    response.headers["content-type"] = "text/plain"
    return response
