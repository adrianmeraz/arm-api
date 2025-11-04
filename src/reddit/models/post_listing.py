from src.reddit.models.post import Post as RedditPost

class PostListing:
    class Data:
        def __init__(self, data: dict):
            self.children = [RedditPost(post['data']) for post in data.get('children', [])]
            self.dist = data.get('dist', 0)
            self.modhash = data.get('modhash')
            self.after = data.get('after')
            self.before = data.get('before')

    def __init__(self, data: dict):
        self.kind = data.get('kind')
        self.data = PostListing.Data(data.get('data'))

    @property
    def posts(self) -> list[RedditPost]:
        return self.data.children
