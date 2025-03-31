import pytest
from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

clien = TestClient(app)
def test_return_healthcheck():
    respose = clien.get("/healthy")
    assert respose.status_code == status.HTTP_200_OK
    assert respose.json() == {"status" : "healthy"}