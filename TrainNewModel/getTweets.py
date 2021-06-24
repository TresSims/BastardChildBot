import requests
import os
import json
import sys

# Get OAuth V2 token from environment
def auth():
    return os.environ.get("BEARER_TOKEN")

# Find the user id based on the handle provided
def get_user_id(header, user):
    username = "usernames={}".format(user)
    user_fields = "user.fields=description,created_at"
    url="https://api.twitter.com/2/users/by?{}&{}".format(username, user_fields)
    response = connect_to_endpoint(url, header)
    return response["data"][0]["id"]

# Get as many tweets as twitter will allow in one request (100)
def get_timeline(header, user_id, filename, pagination_token=None):
    url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
    if pagination_token is None:
        params={"tweet.fields":"created_at,text","max_results":"100"}
    else:
        params={"tweet.fields":"created_at,text","max_results":"100","pagination_token":"{}".format(pagination_token)}
    response = connect_to_endpoint(url, header, params=params)

    # Write the recovered tweets to a file
    write_tweets(response["data"], filename)
    try:
        if response["meta"]["next_token"]:
            get_timeline(header, user_id, filename, pagination_token=response["meta"]["next_token"])
    except:
        return
        

# Write tweets to a file to be used in training
def write_tweets(tweets, filename):
    with open(filename, "a") as fp:
        for tweet in tweets:
            string = tweet["text"]
            if string.split(" ")[0] is "RT":
                continue
            fp.write("{}\n\n".format(tweet["text"]))

# Create OAuth header from token
def create_headers(bearer_token):
    headers={"Authorization":"Bearer {}".format(bearer_token)}
    return headers

# Make API request from twitter
def connect_to_endpoint(url, headers, params=None):
    if params is not None:
        response = requests.request("GET", url, headers=headers, params=params)
    else:
        response = requests.request("GET", url, headers=headers)
        
    print(response.status_code)
    if(response.status_code != 200):
       raise Exception(
           "Request returned an error: {} {}".format(
               response.status_code, response.text
               )
           )
   
    return response.json()

# Main entrypoint
def main(users, filename):
    if os.path.exists(filename): #overwrite already existing training files, to prevent duplicate entries
        os.remove(filename)
    bearer_token=auth()
    headers=create_headers(bearer_token)
    # for each requested user, get their tweet history
    for user in users:
        user_id = get_user_id(headers, user)
        get_timeline(headers, user_id, filename)
