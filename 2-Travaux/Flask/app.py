from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/articles/', methods=['GET', 'POST'])
def articles():
    # Appel d 'api avec user
    id = request.form.get('user_id','0')
    url = "https://get-user-articles.azurewebsites.net/api/get-articles?user_id="
    url =  url + id
    response = requests.get(url)
    articles = response.json()
    return render_template("articles.html", articles = articles)

if __name__ == "__main__":
    app.run(debug=True)