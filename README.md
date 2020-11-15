# Twitter-Sentiment
Sentiment analysis of tweets. Project completed as part of Hack OH/IO 2020

This branch contains the progress made across the entire 42 hour hackathon period. I branched off so we could easily see the orginal project as we move on with the project and get it into a more finalized state.

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

#you may want to create a virtual environment as well

# python libraries
pip3 install -r requirements.txt
python3 setup.py

# run flask app
flask run
```
