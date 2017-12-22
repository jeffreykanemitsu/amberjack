#!/usr/bin/python3
"""Flask web application"""
from flask import abort, Flask, redirect
from models import storage
from models.website import Website
app = Flask('web_flask')

@app.route('/<string:short_url>', methods=['GET'], strict_slashes=False)
def get_redirection(short_url):
    """redirect to long url"""
    website = storage.get("Website", short_url)
    if website is None:
        abort(404)
    return redirect(website.name, 301)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
