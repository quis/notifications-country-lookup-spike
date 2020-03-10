import requests

from flask import Flask, Markup, render_template, request
from notifications_utils.countries import Country, CountryNotFoundError


app = Flask(__name__)


@app.route('/')
def hello():
    search_term = request.args.get('search_term', '')
    country = ''
    postage = ''
    result = ''

    if search_term:
        try:
            country = Country(search_term).canonical_name
            postage = Country(search_term).postage_zone
            result = Markup("""
                <p>✅</p>
                <p>We’d address this letter to <b>{}</b></p>
                <p>We’d charge for postage to <b>{}</b></p>
            """.format(
                country,
                postage,
            ))
        except CountryNotFoundError:
            result = Markup(
                '<p>⚠️</p><p>We don’t think {} is a country</p>'.format(search_term)
            )

    return render_template(
        'index.html',
        search_term=search_term,
        result=result,
        country=country,
        postage=postage,
    )


@app.route('/feedback', methods=['POST'])
def feedback():
    url = 'https://hookb.in/9XyoRoZZpPCLqyNYOaLp'

    data = {
        'search_term': request.form.get('search_term'),
        'country': request.form.get('country'),
        'postage': request.form.get('postage'),
        'feedback': request.form.get('feedback'),
    }

    r = requests.post(url, verify=False, json=data)
    return render_template(
        'thanks.html'
    )
