import sentry_sdk
import os

from bottle import Bottle, request
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn="https://53de4295d9e64d9ca1bf707b7665592f@o431310.ingest.sentry.io/5382327",
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