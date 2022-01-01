import praw



class RedditFetch():
    def __init__(self, key):
        self.stream = praw.Reddit(client_id = key["id"], client_secret = key["secret"], user_agent=key["user_agent"])

    def get_top(self, subreddit, number, return_type="text"):
        if return_type == "text":
            posts = []
            try:
                for submission in self.stream.subreddit(subreddit).top(limit=number):
                    p = {}
                    if not submission.stickied:
                        p["title"] = submission.title
                        p["content"] = submission.selftext
                        posts.append(p)
                return posts
            except:
                return []
        else:
            images = []
            try:
                for submission in self.stream.subreddit(subreddit).top(limit=number):
                    if not submission.stickied:
                        t = {"image": submission.url, "caption": submission.title}
                        images.append(t)
                return images
            except:
                return []


    def get_random_rising(self, subreddit, number, return_type="text"):
        if return_type == "text":
            posts = []
            try:
                for submission in self.stream.subreddit(subreddit).random_rising(limit=number):
                    p = {}
                    if not submission.stickied:
                        p["title"] = submission.title
                        p["content"] = submission.selftext
                        posts.append(p)
                return posts
            except:
                return []
        else:
            images = []
            try:
                for submission in self.stream.subreddit(subreddit).random_rising(limit=number):
                    if not submission.stickied:
                        t = {"image": submission.url, "caption": submission.title}
                        images.append(t)
                return images
            except:
                return []
