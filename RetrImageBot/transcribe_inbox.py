from re import compile
from requests import get
from sys import stdout
from praw.models import Message

from cv2 import error as cv2Error

from reading_image import read_img


def transcribe_inbox(reddit):
    for comment in reddit.inbox.unread():
        comment.mark_read()

        if isinstance(comment, Message):  # skipping pm's
            continue

        submission = comment.submission

        if submission.is_self:  # skipping text only submissions
            continue
        re_image = compile("\.(png)?(jpg)?$")

        if re_image.search(submission.url) == None:
            continue
        
        image = get(submission.url).content

        try:
            text = read_img(image)
        except cv2Error:
            continue

        # Replacing those chars becouse some fonts have "I" looking like one big stick
        if "code" not in comment.body:
            text = text.replace("|", "I")

        reply = f"""
I'm a bot and the text given bellow is my try at reading text in submission.\n
Text may differ from the one that on the image and may be full of cryptic stuff.\n
Downvote me if transcription is bad.

---

{text}

---

###### I'm bot that transcribes images for Reddit.You can volontueer for stuff that i don't know how to transcribe.\n
###### **[If you'd like more information on what we do and why we do it, click here!](https://www.reddit.com/r/TranscribersOfReddit/wiki/index)**
"""

        comment.reply(reply)
