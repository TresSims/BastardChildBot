# TrainNewModel
A basic setup that will let you get tweets from a given set of users and then train a GPT2 model off of them.

## Setup
### Configuration
Configure your required users and training settings in

> /TrainNewModel/config.py.

Add twitter handles to user list, and select your training model and max training steps.

### Required Packages

- gpt-2-simple
- tensorflow v1.x

## Twitter content
The data used to train the GPT2 model here is based off of tweets. In order to download that data you will need access to a twitter developer account. Once you have a developer app setup, you will want to export your bearer token to your environment variables, as that is where the program looks for your token. To do this:

    export BEARER_TOKEN '<your_bearer_token>'
    

## Usage
After setting up config.py and ensuring you have the required packages installed, run

      python3 train.py

This will download your training data, if not already downloaded, and train the model.

# Bot Development In progress

In the future this repo will include a bot that can be added to twitch and discord that will generate messages based on your training data