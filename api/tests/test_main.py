import pytest
from unittest.mock import MagicMock, patch

mock_redis = MagicMock()
mock_redis.ping.return_value = True

with patch("redis.Redis", return_value=mock_redis):
    from fastapi.testclient import TestClient
    import main
    main.r = mock_redis

client = TestClient(main.app)


def test_create_job_returns_job_id():
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = True
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_job_returns_status():
    mock_redis.hgetall.return_value = {"status": "queued", "created_at": "123"}
    response = client.get("/jobs/some-job-id")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"


def test_get_job_not_found_returns_404():
    mock_redis.hgetall.return_value = {}
    response = client.get("/jobs/does-not-exist")
    assert response.status_code == 404
