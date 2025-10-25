class Post:

    def __init__(self, data: dict):
        self.approved_at_utc = data.get('approved_at_utc')
        self.clicked = data.get('clicked')
        self.created_utc = data.get('created_utc')
        self.hidden = data.get('hidden')
        self.is_robot_indexable = data.get('is_robot_indexable')
        self.is_video = data.get('is_video')
        self.score = data.get('score')
        self.self_text = data.get('selftext')
        self.stickied = data.get('stickied')
        self.subreddit = data.get('subreddit')
        self.subreddit_name_prefixed = data.get('subreddit_name_prefixed')
        self.subreddit_subscribers = data.get('subreddit_subscribers')
        self.title = data.get('title')
