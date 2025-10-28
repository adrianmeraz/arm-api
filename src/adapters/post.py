from src.models.post import Post
from src.reddit.models.post import Post as RedditPost

class PostAdapter:
    @classmethod
    def to_ddb_post(cls, r_post: RedditPost) -> Post:
        """Convert a Reddit post object to a DynamoDB post dictionary."""
        ddb_post = {
            'pk': f"POST#{r_post.id}",
            'sk': f"POST#{r_post.id}",
            'obj_type': 'POST',
            'author': r_post.author,
            'body_html': r_post.self_text_html or '',
            'category': r_post.subreddit,
            'image_url': r_post.preview.all_unescaped_image_sources[0] if r_post.preview.all_unescaped_image_sources else '',
            'is_locked': r_post.locked,
            'permalink': f"https://reddit.com{r_post.permalink}",
            'title': r_post.title,
        }
        return Post(**ddb_post)
