from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def make_comment_payload(obj_id: str = "c1", post_id: str = "p1"):
    return {
        "obj_id": obj_id,
        "post_id": post_id,
        "author": "user1",
        "body_html": "<p>hi</p>",
        "parent_id": f"POST#{post_id}",
        "permalink": "/r/test/comment/c1"
    }


@patch("src.data.comment_data.get_post_comments")
def test_read_comments(mock_get_all):
    mock_get_all.return_value = [make_comment_payload("c1"), make_comment_payload("c2")]

    resp = client.get("/post/p1/comment")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["author"] == "user1"


@patch("src.data.comment_data.create_comment")
def test_create_comment(mock_create):
    payload = make_comment_payload()
    mock_create.return_value = payload

    resp = client.post("/post/p1/comment", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["author"] == payload["author"]
    assert data["obj_id"] == payload["obj_id"]


@patch("src.data.comment_data.delete_comment")
def test_delete_comment(mock_delete):
    mock_delete.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    resp = client.delete("/post/p1/comment/c1")
    assert resp.status_code == 200
    data = resp.json()
    assert "ResponseMetadata" in data


@patch("src.data.comment_data.delete_all_comments")
def test_delete_all_comments(mock_delete_all):
    mock_delete_all.return_value = None

    resp = client.delete("/post/p1/comment")
    assert resp.status_code == 200
    assert resp.text == "null"
