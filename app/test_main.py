from fastapi.testclient import TestClient
from pathlib import Path
from .main import app

client = TestClient(app)

def test_get_fen_code():
  # _test_upload_file = Path('./app/media', 'test.jpeg')
  # _files = {'upload_file': _test_upload_file.open('rb')}

  # response = client.post('/uploadfile', files=_files)
  response = client.get(
      # "/fen", files={"file": ("filename", open('./app/media/test.jpeg', "rb"), "image/jpeg")}
      "/fen?code=a672f54f-37d4-4c81-87d6-4d95786483a7"
  )
  assert response.status_code == 200
  assert response.json == {
    "1b1b2k1-K2B1q2-R3B2p-3b1NR1-5p2-3N4-8-5N2"
  }