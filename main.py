from flask import Flask, render_template, request, Response  #, jsonify
from flask_cors import CORS
from ua_parser import user_agent_parser
import time
import json
from replit import db
import random
import string

app = Flask('app')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def serial():
    e = ''
    for i in range(50):
        e += random.choice(string.ascii_letters + string.digits)
    return e


template_json = {
    'app_id': serial(),
    'private_key': serial(),
    'app_name': 'My Epic App Name',
    'app_user_hits': [],
    'app_hits': {
        'Chrome': 0,
        'Edge': 0,
        'Safari': 0,
        'Firefox': 0
    },
    'app_pass': 'bababooey'
}


# return  user_agent_parser.Parse(request.headers.get('User-Agent'))["user_agent"]["family"]
@app.route('/')
def hello_world():
    return render_template('landing.html')


@app.route('/get', methods=["GET", "POST"])
def get():
    if request.method == 'POST':
        new_app = template_json
        new_app['app_id'] = request.values.get('apikey')
        new_app['private_key'] = serial()
        new_app['app_name'] = request.values.get('app_name')
        new_app['app_pass'] = request.values.get('password')

        db[new_app['app_id']] = json.dumps(new_app)

        message = "New api key activated! Now use your new api key: <b>" + new_app[
            'app_id'] + "</b> and password to log in! (note: you will need that api key to log in so you better save it)"

        return message
    else:
        return render_template('get.html', apikey=serial())


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/loginapi', methods=['POST'])
def login_api():
    time.sleep(0.2)  # it goes too fast lmao

    # return db[json.loads(request.data)["key"]]
    try:
        if json.loads(db[json.loads(
                request.data)["key"]])['app_pass'] == json.loads(
                    request.data)["password"]:

            load = json.loads(db[json.loads(request.data)["key"]])

            load['app_pass'] = 'ha you thought'

            return {'status': True, 'load': load}
        else:
            return {'status': False}
    except:
        return {'status': False}


@app.route('/loginkey', methods=['POST'])
def login_key():
    key = str(json.loads(request.data)["key"])
    

    allkeys = list(db.keys())
    e = []

    for i in allkeys:
      if json.loads(db[i])['private_key'] == key:
        load = json.loads(db[i])

        load['app_pass'] = 'ha you thought'

        return {'status': True, 'load': load}
    return {'status': False}


@app.route('/collect/v1/<apikey>')
def collect(apikey):
    try:
        user_agent = user_agent_parser.Parse(
            request.headers.get('User-Agent'))["user_agent"]["family"]

        load = json.loads(db[apikey])

        # load['app_user_hits'] = []

        if request.headers['X-Replit-User-Id']:
            if request.headers['X-Replit-User-Name'] not in load[
                    'app_user_hits']:
                load['app_user_hits'].append(
                    request.headers['X-Replit-User-Name'])

        load['app_hits'][user_agent] += 1

        db[apikey] = json.dumps(load)
        return 'var cknanalytics_' + str(apikey) + '_res = {status: true};'
        # return res

    except:
        return Response('var cknanalytics_' + str(apikey) +
                        '_res = {status: false};',
                        mimetype='application/javascript')


@app.route('/help')
def help():
    return render_template('help.html',
                           user_id=request.headers['X-Replit-User-Id'],
                           user_name=request.headers['X-Replit-User-Name'],
                           user_roles=request.headers['X-Replit-User-Roles'])


@app.route('/badge/<apikey>')
def badge(apikey):
    return render_template('badge.html')


app.run(host='0.0.0.0', port=8080, debug=True)



needed_flask = [
	"Flask",
	"render_template",
	"redirect",
	"url_for",
	"request"
]
for needed_import in needed_flask:
	exec(f"from flask import {needed_import}")

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("layout.html")

@app.route("/")
def festivals():
	return render_template("landing.html")

@app.route("/")
def geography():
	return render_template("help.html")

@app.route("/")
def facts():
	return render_template("get.html")

@app.route("/")
def facts():
	return render_template("badge.html")

@app.route("/")
def facts():
	return render_template("dashboard.html")

@app.route("/sources/<page>")
def sources(page):
	page = page.lower()
	if page == "all":
		return render_template("sources.html")
	elif page == "geography":
		return render_template("sources/geography.html")
	elif page in ["home", "index"]:
		return render_template("sources/index.html")
	elif page in ["list-of-cities", "list_of_cities"]:
		return render_template("sources/list_of_cities.html")
	elif "fact" in page:
		return render_template("sources/facts.html")
	elif "festival" in page:
		return render_template("sources/festivals.html")
	else:
		return render_template("404.html")

@app.route("/sources/")
def sources_no_arg():
	return redirect(url_for("sources", page="all"))

@app.route("/list-of-cities/")
def list_of_cities():
	return render_template("list_of_cities.html")
@app.route("/list_of_cities")
def list_of_cities_underscores():
	return redirect(url_for("list_of_cities"))

@app.route("/weblinks/")
def weblinks():
	return render_template("weblinks.html")
@app.route("/web-links/")
def web_links():
	return redirect(url_for("weblinks"))
@app.route("/web_links/")
def web_links_():
	return redirect(url_for("weblinks"))

@app.route("/about/")
def about_us():
	return render_template("about_us.html")
@app.route("/about_us/")
def about_us_():
	return redirect(url_for("about_us"))
@app.route("/about-us/")
def about_us__():
	return redirect(url_for("about_us"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8080)


'''
<link rel="icon"
      type="image/ico"
      href="static/favicon.ico">
'''