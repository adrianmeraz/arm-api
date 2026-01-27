import pytest
from src.adapters.post import PostAdapter
from src.reddit.models.post import Post as RedditPost


def test_to_ddb_post_full_data():
    """Test conversion with all fields populated."""
    reddit_data = {
        'id': 'abc123',
        'author': 'test_user',
        'selftext_html': '<p>test body</p>',
        'subreddit': 'testsubreddit',
        'preview': {
            'images': [{
                'source': {
                    'url': 'https://test.com/image.jpg'
                }
            }]
        },
        'locked': True,
        'permalink': '/r/testsubreddit/comments/abc123/test_post',
        'title': 'Test Post'
    }

    reddit_post = RedditPost(reddit_data)
    ddb_post = PostAdapter.to_ddb_post(reddit_post)

    # Basic post fields
    assert ddb_post.obj_type == 'POST'
    assert ddb_post.author == 'test_user'
    assert ddb_post.body_html == '<p>test body</p>'
    assert ddb_post.category == 'testsubreddit'
    assert ddb_post.image_url == 'https://test.com/image.jpg'
    assert ddb_post.is_locked is True
    assert ddb_post.permalink == 'https://reddit.com/r/testsubreddit/comments/abc123/test_post'
    assert ddb_post.title == 'Test Post'

    # Base model fields
    assert ddb_post.pk.startswith('POST#')
    assert ddb_post.sk == ddb_post.pk
    assert isinstance(ddb_post.created_at_utc, int)
    assert isinstance(ddb_post.modified_at_utc, int)
    assert ddb_post.is_deleted is False
    assert ddb_post.expires_at is None


def test_to_ddb_post_minimal_data():
    """Test conversion with minimal required fields."""
    reddit_data = {
        'id': 'abc123',
        'author': 'test_user',
        'locked': False,
        'subreddit': 'testsubreddit',
        'permalink': '/r/testsubreddit/comments/abc123/test_post',
        'title': 'Test Post'
    }

    reddit_post = RedditPost(reddit_data)
    ddb_post = PostAdapter.to_ddb_post(reddit_post)

    assert ddb_post.body_html == ''  # Empty string fallback
    assert ddb_post.image_url == ''  # Empty string fallback
    assert ddb_post.is_locked is False  # Model default
    assert ddb_post.pk.startswith('POST#')
    assert ddb_post.sk == ddb_post.pk


def test_to_ddb_post_no_preview():
    """Test conversion when preview data is missing."""
    reddit_data = {
        'id': 'abc123',
        'author': 'test_user',
        'selftext_html': '<p>test body</p>',
        'subreddit': 'testsubreddit',
        'locked': False,
        'permalink': '/r/testsubreddit/comments/abc123/test_post',
        'title': 'Test Post'
    }

    reddit_post = RedditPost(reddit_data)
    ddb_post = PostAdapter.to_ddb_post(reddit_post)

    assert ddb_post.image_url == ''  # Empty string when no preview


def test_to_ddb_post_empty_preview():
    """Test conversion when preview exists but has no images."""
    reddit_data = {
        'id': 'abc123',
        'author': 'test_user',
        'locked': False,
        'subreddit': 'testsubreddit',
        'preview': {'images': []},  # Empty images list
        'permalink': '/r/testsubreddit/comments/abc123/test_post',
        'title': 'Test Post'
    }

    reddit_post = RedditPost(reddit_data)
    ddb_post = PostAdapter.to_ddb_post(reddit_post)

    assert ddb_post.image_url == ''  # Empty string when no images


def test_to_ddb_post_sanitize_fields():
    """Test that HTML and URLs are properly handled."""
    reddit_data = {
        'id': 'abc123',
        'author': 'test_user',
        'locked': False,
        'selftext_html': None,  # Test None handling
        'subreddit': 'testsubreddit',
        'permalink': '/r/testsubreddit/comments/abc123/test&amp;post',  # HTML encoded
        'title': 'Test Post'
    }

    reddit_post = RedditPost(reddit_data)
    ddb_post = PostAdapter.to_ddb_post(reddit_post)

    assert ddb_post.body_html == ''  # None converted to empty string
    assert ddb_post.permalink.startswith('https://reddit.com/')  # Proper URL prefix
