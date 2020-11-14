# Twitter-Sentiment
Sentiment analysis of tweets. Project completed as part of Hack OH/IO 2020


# Setup
``` bash
# setup venv
py -m venv env
env\\Scripts\\activate

# if the venv fails then run PowerShell as Admin and do
Set-ExecutionPolicy RemoteSigned

# python libraries
pip3 install -r requirements.txt

# run flask app
set FLASK_APP=app
flask run
```