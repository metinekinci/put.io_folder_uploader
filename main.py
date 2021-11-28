from flask import Flask, request, redirect, session, url_for, render_template
from requests_oauthlib import OAuth2Session
from werkzeug.utils import secure_filename
import os, io, re

client_id = "5487"
client_secret = "5M4BAC5P4XG7CF6CVQN3"
authorization_base_url = 'https://api.put.io/v2/oauth2/authenticate/'
token_url = 'https://api.put.io/v2/oauth2/access_token/'

created_folders = {}

UPLOAD_FOLDER = '.'
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    client = OAuth2Session(client_id)
    authorization_url, state = client.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback", methods=["GET","POST"])
def callback():
    if request.method == "GET":
        client = OAuth2Session(client_id, state=session['oauth_state'], token='KG5BAPVQ3WX22VMB3WXC')
        token = client.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url, include_client_id=True)
        session['oauth_token'] = token
        return redirect(url_for('upload'))

def splitter(arg):
    return re.split("_",arg)
def join(arg):
    return "_".join(arg)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    if request.method == "POST":
        root_folder = request.form["folderName"]
        client = OAuth2Session(client_id, token=session['oauth_token'])
        api_response = client.post('https://api.put.io/v2/files/create-folder',data={"name":root_folder})
        created_folders[root_folder] = api_response.json()["file"]["id"]
        files = request.files.getlist('files[]')
        for file in files:
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], splitter(file_name)[-1]))
            with io.open(splitter(file_name)[-1], 'rb') as f:
                files = {"file":(splitter(file_name)[-1],f)}
                if "_".join(splitter(file_name)[:-1]) in created_folders:
                    client.post('https://upload.put.io/v2/files/upload', data={"parent_id":created_folders["_".join(splitter(file_name)[:-1])]}, files=files)
                else:
                    for i in range(1,len(splitter(file_name))+1):
                        if join(splitter(file_name)[0:-i]) in created_folders:
                            for j in splitter(file_name)[-i:-1]:
                                api_response = client.post('https://api.put.io/v2/files/create-folder',data={"name":j,"parent_id":created_folders[join(splitter(file_name)[0:-i])]})
                                i -= 1
                                created_folders[join(splitter(file_name)[0:-i])] = api_response.json()["file"]["id"]
                                break
                            client.post('https://upload.put.io/v2/files/upload', data={"parent_id":api_response.json()["file"]["id"]}, files=files)
                                

                os.remove(splitter(file_name)[-1])
        return "Done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
