#import gpt_2_simple as gpt2
import os
import requests

import getTweets
import config

model_name = config.model
steps = config.steps

filename = config.users[0]
for user in config.users[1:]:
        filename += "+{}".format(user)
filename += ".txt"

if not os.path.isdir(os.path.join("models", model_name)):
    gpt2.download_gpt2(model_name=model_name)

if not os.path.isfile(filename):
    getTweets.main(config.users, filename)


sess = gpt2.start_tf_sess()
fpt.finetune(sess,
             filename,
             model_name=model_name,
             steps=steps)

gpt2.generate(sess)
