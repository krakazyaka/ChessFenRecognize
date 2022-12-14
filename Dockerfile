FROM python:3.7

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install python-multipart

#
COPY  . .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]