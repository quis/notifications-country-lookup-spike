import json
import http.client
import requests
from urllib.parse import quote_plus
from flask import Flask, Markup, render_template, request, redirect
from notifications_utils.countries import Country, CountryNotFoundError


app = Flask(__name__)


@app.route('/')
def hello():
    search_term = request.args.get('search_term', '')
    country = ''
    postage = ''
    result = ''
    found = False

    try:
        country = Country(search_term).canonical_name
        postage = Country(search_term).postage_zone
        found = True
    except CountryNotFoundError:
        pass

    return render_template(
        'index.html',
        search_term=search_term,
        result=result,
        country=country,
        postage=postage,
        found=found,
    )


@app.route('/feedback', methods=['POST'])
def feedback():
    url = 'https://engc9uzcryg3gfu.m.pipedream.net'

    data = {
        'search_term': request.form.get('search_term'),
        'country': request.form.get('country'),
        'postage': request.form.get('postage'),
        'feedback': request.form.get('feedback'),
    }

    requests.post(url, verify=False, json=data)

    return redirect('/thanks')


@app.route('/thanks', methods=['GET'])
def thanks():
    return render_template(
        'thanks.html'
    )
