from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import matplotlib.pyplot as plt


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


@app.route('/commits/')
def commits_graph():
    # Utilisez l'API GitHub pour obtenir la liste des commits
    github_api_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = urlopen(github_api_url)
    commits_data = json.loads(response.read().decode('utf-8'))

    # Analysez les données pour extraire les informations nécessaires
    commit_times = [commit['commit']['author']['date'] for commit in commits_data]
    commit_minutes = [extract_minutes(commit_time) for commit_time in commit_times]

    # Créez un graphique avec les données obtenues
    # (utilisez une bibliothèque comme matplotlib, plotly, etc.)

    # Retournez le résultat dans un template ou directement en JSON
    return jsonify({'commit_minutes': commit_minutes})

def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return minutes




if __name__ == "__main__":
  app.run(debug=True)
