# put.io Interview Project

This article aims to document the case study in the recruitment process of put.io.

## Introduction
This application uploads a folder and its contents to your put.io account using the put.io API.

This application is containerized and deployed to Cloud Run. For more information, see the links below. 

[Google Cloud Run](https://cloud.google.com/sdk/gcloud/reference/run/deploy)
[Put.io API Reference](https://api.put.io)

## Dependencies

* [Python](https://www.python.org/) - Programming Language
* [Flask](https://flask.palletsprojects.com/) - The framework used
* [Pip](https://pypi.org/project/pip/) - Dependency Management
* [requests-oauthlib](https://pypi.org/project/requests-oauthlib/) - OAuth2 Authentication

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

## Usage

https://putio-nh537hdurq-uc.a.run.app/
