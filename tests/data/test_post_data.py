import pytest
from unittest.mock import patch
import pydantic

from src.models.post import Post
from src.data import post_data


@pytest.fixture
def mock_dynamo_client():
    with patch('src.data.post_data._table_client') as mock_client:
        yield mock_client


@pytest.fixture
def sample_post():
    return Post(
        author="test_author",
        body_html="<p>Test content</p>",
        category="test_category",
        image_url="https://example.com/image.jpg",
        permalink="https://reddit.com/r/test/123",
        title="Test Post"
    )


def test_create_post(mock_dynamo_client, sample_post):
    """Test creating a single post."""
    # Setup
    mock_dynamo_client.create_item.return_value = {"pk": sample_post.pk}

    # Execute
    result = post_data.create_post(sample_post)

    # Verify
    mock_dynamo_client.create_item.assert_called_once()
    create_args = mock_dynamo_client.create_item.call_args[0][0]
    assert create_args["author"] == "test_author"
    assert create_args["body_html"] == "<p>Test content</p>"
    assert create_args["category"] == "test_category"
    assert create_args["pk"].startswith("POST#")
    assert result == {"pk": sample_post.pk}


def test_delete_post(mock_dynamo_client):
    """Test deleting a post by ID."""
    # Setup
    post_id = "POST#123"
    mock_dynamo_client.delete_item.return_value = {"ResponseMetadata": {"RequestId": "test"}}

    # Execute
    result = post_data.delete_post(post_id)

    # Verify
    mock_dynamo_client.delete_item.assert_called_once_with(
        hash_key=post_id,
        sort_key=post_id
    )
    assert result == {"ResponseMetadata": {"RequestId": "test"}}


def test_batch_create_posts(mock_dynamo_client, sample_post):
    """Test creating multiple posts in batch."""
    # Setup
    posts = [sample_post, sample_post]  # Two identical posts for testing
    mock_dynamo_client.batch_write_items.return_value = {"UnprocessedItems": {}}

    # Execute
    result = post_data.batch_create_posts(posts)

    # Verify
    mock_dynamo_client.batch_write_items.assert_called_once()
    batch_items = mock_dynamo_client.batch_write_items.call_args[0][0]
    assert len(batch_items) == 2
    for item in batch_items:
        assert item["author"] == "test_author"
        assert item["category"] == "test_category"
        assert item["pk"].startswith("POST#")
    assert result == {"UnprocessedItems": {}}


def test_get_all_posts(mock_dynamo_client, sample_post):
    """Test retrieving all posts."""
    # Setup
    mock_posts = [sample_post.model_dump(mode='json')]
    mock_dynamo_client.get_all_table_items.return_value = mock_posts

    # Execute
    result = post_data.get_all_posts()

    # Verify
    mock_dynamo_client.get_all_table_items.assert_called_once()
    assert result == mock_posts
    assert len(result) == 1
    assert result[0]["author"] == "test_author"
    assert result[0]["category"] == "test_category"


def test_create_post_validates_data(mock_dynamo_client):
    """Test that invalid post data raises validation error."""
    with pytest.raises(pydantic.ValidationError):
        # Missing required fields should raise ValidationError when using model_validate
        Post.model_validate({"author": "test_author", "title": "Test Post"})


def test_get_post(mock_dynamo_client, sample_post):
    """Test retrieving a single post by id uses generated key and returns item."""
    # Arrange
    post_id = "123"
    expected_pk = Post.generate_key(obj_type='post', obj_id=post_id)
    expected_item = sample_post.model_dump(mode='json')
    mock_dynamo_client.get_item.return_value = expected_item

    # Act
    result = post_data.get_post(post_id)

    # Assert
    mock_dynamo_client.get_item.assert_called_once_with(hash_key=expected_pk, sort_key=expected_pk)
    assert result == expected_item
