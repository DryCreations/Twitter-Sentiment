# Twitter-Sentiment
Sentiment analysis of tweets. Project completed as part of Hack OH/IO 2020

# dotenv

create a .env file in the root of the project
```
TWITTER_CONSUMER_KEY=""
TWITTER_CONSUMER_SECRET=""
TWITTER_CALLBACK=""
SESSION_SECRET=""

```

# Setup
``` bash
# change directory into frontend
cd frontend

# install node modules
npm install

# build dist folder
npm run build

# change directory to root
cd ..

# setup venv
python3 -m venv env
env\\Scripts\\activate

# if the venv fails then run PowerShell as Admin and do
Set-ExecutionPolicy RemoteSigned

# python libraries
pip3 install -r requirements.txt
python3 setup.py

# run flask app
flask run
```
