#
FROM python:3.10
#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
COPY  ./interfaces /code/interfaces
#
COPY ./models /code/models
#
COPY ./capra_control.py /code/capra_control.py
#
COPY ./main.py /code/main.py
#
EXPOSE 8000
#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]