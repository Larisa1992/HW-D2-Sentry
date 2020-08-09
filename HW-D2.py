import sentry_sdk
import os

from bottle import Bottle, request
from sentry_sdk.integrations.bottle import BottleIntegration

from dotenv import load_dotenv
load_dotenv()

sentry_sdk.init(
    dsn=os.environ['DSN_ENV'],
    integrations=[BottleIntegration()]
)

app = Bottle()

@app.route("/")
def index():
    html = """
<!doctype html>
<html lang="en">
  <head>
    <title>Логирование в Sentry</title>
  </head>
  <body>
    <div class="container">
      <p>Ответ по пути /</p>
    </div>
  </body>
</html>
"""
    return html

@app.route('/success')  
def success():  
    return  "запрос успешен"
  
@app.route('/fail')  
def fail():  
    raise RuntimeError("There is an error!") 

if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)
