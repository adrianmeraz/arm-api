class Post:

    class Preview:
        def __init__(self, data: dict):
            self.images = [Post.Preview.Image(image) for image in data.get('images', [])]

        class Source:
            def __init__(self, data: dict):
                self.url = data.get('url')
                self.width = data.get('width')
                self.height = data.get('height')

        class Image:
            def __init__(self, data: dict):
                self.source = Post.Preview.Source(data.get('source', {}))
                self.resolutions = [Post.Preview.Source(res) for res in data.get('resolutions', [])]
                self.variants = data.get('variants', {})
                self.id = data.get('id')

        @property
        def all_image_sources(self):
            return [image.source.url for image in self.images]

    def __init__(self, data: dict):
        self.approved_at_utc = data.get('approved_at_utc')
        self.author = data.get('author')
        self.clicked = data.get('clicked')
        self.created_utc = data.get('created_utc')
        self.hidden = data.get('hidden')
        self.id = data.get('id')
        self.is_robot_indexable = data.get('is_robot_indexable')
        self.is_video = data.get('is_video')
        self.num_comments = data.get('num_comments')
        self.permalink = data.get('permalink')
        self.preview = Post.Preview(data.get('preview', {}))
        self.score = data.get('score')
        self.self_text = data.get('selftext')
        self.stickied = data.get('stickied')
        self.subreddit = data.get('subreddit')
        self.subreddit_name_prefixed = data.get('subreddit_name_prefixed')
        self.subreddit_subscribers = data.get('subreddit_subscribers')
        self.title = data.get('title')
        self.ups = data.get('ups')
        self.url = data.get('url')
