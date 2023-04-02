from fastapi.testclient import TestClient
from pathlib import Path
from .main import app

client = TestClient(app)

def test_get_fen_code():
  _test_upload_file = Path('./app/media', 'test.jpeg')
  _files = {'upload_file': _test_upload_file.open('rb')}

  # response = client.post('/uploadfile', files=_files)
  response = client.post(
      "/upload_file", files={"file": ("filename", open('./app/media/test.jpeg', "rb"), "image/jpeg")}
  )
  assert response.status_code == 200