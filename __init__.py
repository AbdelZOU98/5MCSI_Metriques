from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3



app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # COMMENT

@app.route("/contact/")
def MaPremiereAPI():
    #return "<h2>Ma page de contact</h2>"
    return render_template('contact_form.html')
    

@app.route('/paris/')
def meteo2():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = datetime.utcfromtimestamp(list_element.get('dt')).strftime('%Y-%m-%d %H:%M:%S')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return render_template('histog.html', results=results)


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme2/")
def mongraphique2():
    return render_template("histog.html")


if __name__ == "__main__":
  app.run(debug=True)
