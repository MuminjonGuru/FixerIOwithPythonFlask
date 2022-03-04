from flask import Flask, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


#################################
#         Real time rates       #
#################################
@app.route('/result/<string:usd_aud>/<string:usd_eur>/<string:usd_gbp>')
def latest_results(usd_aud, usd_eur, usd_gbp):
    return "<h3>USDAUD: {};  <br>USDEUR: {}; <br>USDGBP: {}</h3>".format(usd_aud, usd_eur, usd_gbp)


@app.route('/latest', methods=['GET', 'POST'])
def latest():
    if request.method == 'GET':
        return '''<h1>Please fill out the parameters</h1>
                    <form method="POST" action="/latest">
                    <input type="text" name="acc_key" value="39d5f311be0b4839650bab0c13fc220d">
                    <input type="text" name="currencies" value="AUD,EUR,GBP">                
                    <input type="submit" value="Request">
                </form>'''
    else:
        acc_key = request.form['acc_key']
        currencies = request.form['currencies']

        req = requests.get('http://data.fixer.io/api/latest?access_key=' + acc_key + '&symbols=' + currencies)
        response = req.json()

        usd_aud = response['rates']['AUD']
        usd_eur = response['rates']['EUR']
        usd_gbp = response['rates']['GBP']

        return redirect(url_for('latest_results', usd_aud=usd_aud, usd_eur=usd_eur, usd_gbp=usd_gbp))


#################################
#         Conversion            #
#################################
@app.route('/result/<string:from_c>/<string:to_c>/<string:amount>/<string:rate>/<string:result>')
def result_conversion(from_c, to_c, amount, rate, result):
    return "<h3>From: {};  <br>To: {}; <br>Amount: {}; <br> Result: {}; <br> Rate: {};</h3>" \
        .format(from_c, to_c, amount, result, rate)


@app.route('/conversion', methods=['GET', 'POST'])
def conversion():
    if request.method == 'GET':
        return '''<h1>Please fill out the parameters</h1>
                    <form method="POST" action="/conversion">
                    <input type="text" name="acc_key" value="39d5f311be0b4839650bab0c13fc220d">
                    <input type="text" name="from" value="from">
                    <input type="text" name="to" value="to">
                    <input type="text" name="amount" value="amount">
                    <input type="submit" value="Request">
                </form>'''
    else:
        acc_key = request.form['acc_key']
        from_c = request.form['from']
        to_c = request.form['to']
        amount = request.form['amount']

        req = requests.get(
            'http://data.fixer.io/api/convert?access_key=' + acc_key + '&from=' + from_c
            + "&to=" + to_c + "&amount=" + amount)
        response = req.json()

        rate = response['info']['rate']
        result = response['result']

        return redirect(
            url_for('result_conversion', from_c=from_c, to_c=to_c, amount=amount, rate=rate, result=result))


if __name__ == '__main__':
    app.run()
