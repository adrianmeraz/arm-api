import html

class Post:

    class Preview:
        def __init__(self, data: dict):
            self.images = [Post.Preview.Image(image) for image in data.get('images', [])]

        class Source:
            def __init__(self, data: dict):
                self.url = data.get('url')
                self.width = data.get('width')
                self.height = data.get('height')

            @property
            def unescaped_url(self):
                return html.unescape(self.url) if self.url else None

        class Image:
            def __init__(self, data: dict):
                self.source = Post.Preview.Source(data.get('source', {}))
                self.resolutions = [Post.Preview.Source(res) for res in data.get('resolutions', [])]
                self.variants = data.get('variants', {})
                self.id = data.get('id')

        @property
        def all_unescaped_image_sources(self):
            return [image.source.unescaped_url for image in self.images]

    def __init__(self, data: dict):
        self.archived = data.get('archived')
        self.approved_at_utc = data.get('approved_at_utc')
        self.author = data.get('author')
        self.banned_by = data.get('banned_by')
        self.clicked = data.get('clicked')
        self.created_utc = data.get('created_utc')
        self.hidden = data.get('hidden')
        self.id = data.get('id')
        self.is_robot_indexable = data.get('is_robot_indexable')
        self.is_video = data.get('is_video')
        self.locked = data.get('locked')
        self.num_comments = data.get('num_comments')
        self.permalink = data.get('permalink')
        self.post_hint = data.get('post_hint')
        self.preview = Post.Preview(data.get('preview', {}))
        self.score = data.get('score')
        self.self_text = data.get('selftext')
        self.self_text_html = data.get('selftext_html')
        self.stickied = data.get('stickied')
        self.subreddit = data.get('subreddit')
        self.subreddit_name_prefixed = data.get('subreddit_name_prefixed')
        self.subreddit_subscribers = data.get('subreddit_subscribers')
        self.title = data.get('title')
        self.ups = data.get('ups')
        self.url = data.get('url')

    @property
    def full_permalink(self) -> str:
        return f'https://reddit.com{self.permalink}'

    @property
    def is_active(self):
        return all([
            not self.banned_by,
            not self.locked,
            not self.hidden,
            self.is_robot_indexable,
        ])