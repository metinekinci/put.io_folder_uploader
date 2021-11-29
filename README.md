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

* Redirects to the "/upload" page for uploading files after OAuth2 authentication.

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

* On the Upload page, there is a button to select the folder to upload. Then the file upload process is started with the Submit button. The files uploaded on this page are transferred to the backend under the name of the input tag, namely files[].

```html
<input type="file" onchange="selectFolder(event)" name="files[]" multiple="true" autocomplete="off" webkitdirectory directory required>
```

```python
files = request.files.getlist('files[]')
```

---
**NOTE**

For the content to be uploaded to be a folder, "webkitdirectory directory" must be added to the input tag.

---

* The string at index 0 of the array formed by separating the directory name of one of the files uploaded with javascript with slash can be accepted as the root directory. (e.g. "uploaded-folder/sub-folder/sub-sub-folder" => ["uploaded-folder","sub-folder","sub-sub-folder"][0] = "uploaded-folder"

```html
<script type="text/javascript">
function selectFolder(e) {
    let theFiles = e.target.files;
    let relativePath = theFiles[0].webkitRelativePath;
    let folder = relativePath.split("/");
    let folderName = document.getElementById("folderName")
    folderName.value = folder[0]
}
</script>
```
* Get root folder's name
```python
root_folder = request.form["folderName"]
```
* The root folder is created in the Put.io account and the ID of the created folder is stored in the dictionary of created folders.

```python
api_response = client.post('https://api.put.io/v2/files/create-folder',data={"name":root_folder})
created_folders[root_folder] = api_response.json()["file"]["id"]
```

* Directory names separated by secure_filename with slash are formatted to be separated by underscore.(e.g. "root-folder/folder/file" => "root-folder_folder_file")To save files with filenames, the file directories are separated by underscores. The last element in the resulting list is equal to the file name.(e.g. ["root-folder", "folder", "file"][-1] = "file"). The files are saved on the server under these file names.

```python
def splitter(arg):
    return re.split("_",arg)
def join(arg):
    return "_".join(arg)
```

```python
file_name = secure_filename(file.filename)
file.save(os.path.join(app.config['UPLOAD_FOLDER'], splitter(file_name)[-1]))
```

* The names and IDs of created folders are stored in a dictionary called created_folders. When a new file is to be uploaded, the previously created top-level root directory of the directory where the file is located is searched. After the root directory is found, subfolders are created under that directory and the file upload process is completed.

```python
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
```
* The saved file is deleted from the server.

```python
os.remove(splitter(file_name)[-1])
```
## Conclusion

This application has two weaknesses. First, if the folder name contains underscores, the application will not work properly. This is because a folder is separated from the folder in its parent directory by an underscore. However, this problem can be fixed if a slash is used as a separator in file names. Secondly, an empty folder cannot be resolved in the folder that is loaded in the HTML page.
