import praw
try:
    import api.keys as keys
except:
    import keys

stream = praw.Reddit(client_id = keys.reddit_id, client_secret = keys.reddit_secret, user_agent=keys.reddit_user_agent)

def get_top_text(subreddit, number):
    message = ""
    try:
        for submission in stream.subreddit(subreddit).hot(limit=number):
            if not submission.stickied:
                message += "<b>" + submission.title + "</b>" + "\n" + submission.selftext + "\n\n\n"
        return message
    except:
        return "Api call failed, sorry"


def get_top_image(subreddit, number):
    images = []
    try:
        for submission in stream.subreddit(subreddit).hot(limit=number):
            if not submission.stickied:
                t = {"image": submission.url, "caption": submission.title}
                images.append(t)
        return images
    except:
        return ["Api call failed, sorry"]
