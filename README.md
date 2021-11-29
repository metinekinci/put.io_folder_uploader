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

### Virtual environments

```
$ sudo apt-get install python-virtualenv
$ python3 -m venv venv
$ . venv/bin/activate
```
Install all project dependencies using:

```
$ pip install -r requirements.txt
```

## Deploying

After installing [Cloud SDK](https://cloud.google.com/sdk/docs/install), run the following command in the directory where the application is located.

```
$ gcloud run deploy
```
