# put.io Interview Project

This article aims to document the case study in the recruitment process of put.io.

## Introduction
This application uploads a folder and its contents to your put.io account using the put.io API.

This application is containerized and deployed to Cloud Run. For more information, see the links below. 

[Google Cloud Run](https://cloud.google.com/sdk/gcloud/reference/run/deploy)

[Put.io API Reference](https://api.put.io)

[Working application link](https://putio-nh537hdurq-uc.a.run.app/)

## Dependencies

* [Python](https://www.python.org/) - Programming Language
* [Flask](https://flask.palletsprojects.com/) - The framework used
* [Pip](https://pypi.org/project/pip/) - Dependency Management
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/) - OAuth2 Authentication
* [werkzeug.secure_filename](https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.utils.secure_filename) - Processes a filename and returns a safe version of it

## Virtual environments

```bash
sudo apt-get install python-virtualenv
python3 -m venv venv
. venv/bin/activate
```
Install all project dependencies using:

```bash
pip install -r requirements.txt
```

## Deploying

After installing [Cloud SDK](https://cloud.google.com/sdk/docs/install), run the following command in the directory where the application is located.

```bash
gcloud run deploy
```

## How It Works

* Required modules are imported

```python
from flask import Flask, request, redirect, session, url_for, render_template
from requests_oauthlib import OAuth2Session
from werkzeug.utils import secure_filename
import os, io, re
```

* The information required to access the Put.io API is assigned to variables as follows.

```python
client_id = "***"
client_secret = "***"
authorization_base_url = 'https://api.put.io/v2/oauth2/authenticate/'
token_url = 'https://api.put.io/v2/oauth2/access_token/'
```

* The start page is rendered. When we reach the home page of the web application, we get information about the application and a button to log in to the Put.io account directs us to the login page.

```python
@app.route("/")
def index():
    return render_template("index.html")
```

* OAuth2 Authentication Flow

```python
@app.route("/login")
def login():
    client = OAuth2Session(client_id)
    authorization_url, state = client.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback", methods=["GET","POST"])
def callback():
    if request.method == "GET":
        client = OAuth2Session(client_id, state=session['oauth_state'], token='***')
        token = client.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url, include_client_id=True)
        session['oauth_token'] = token
        return redirect(url_for('upload'))
```
