#!/usr/bin/python3
"""Flask web application"""
from flask import abort, Flask, jsonify, make_response, redirect, render_template, request
from models import storage
from models.website import Website
app = Flask('web_flask')

@app.route('/', methods=['GET'], strict_slashes=False)
@app.route('/<string:short_url>', methods=['GET'], strict_slashes=False)
def get_redirection(short_url=None):
    """redirect to long url"""
    if not short_url:
        return "<h1> HELLO WORLD</h1>"
    website = storage.get("Website", short_url)
    if website is None:
        abort(404)
    name = website.name
    if "http://" not in name and "https://" not in name:
        name = "http://" + name
    return redirect(name, 301)

@app.route('/', methods=['POST'], strict_slashes=False)
def post_new_site():
    """post a new website"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    website = storage.get_short("Website", request.get_json().get("name"))
    if website is None:
        website = Website(**request.get_json())
        website.save()
    return make_response(jsonify(website.to_dict()), 201)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
