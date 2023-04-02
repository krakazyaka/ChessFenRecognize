from fastapi.testclient import TestClient
from pathlib import Path
from .main import app

client = TestClient(app)

def test_get_fen_code():
  _test_upload_file = Path('./media', 'test.jpeg')
  _files = {'upload_file': _test_upload_file.open('rb')}

  response = client.post('/uploadfile', files=_files)

  assert response.status_code == 200