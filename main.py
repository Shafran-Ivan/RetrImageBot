from transcribe_inbox import transcribe_inbox
from praw import Reddit
from time import sleep

reddit = Reddit("bot1", user_agent="RetrImageBot by u\TovarischKaras")

while True:

    transcribe_inbox(reddit)

    sleep(60)