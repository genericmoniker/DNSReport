FROM python:3.7.4-slim-buster

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --user --upgrade pip
RUN pip install --user poetry

COPY . .

RUN /home/appuser/.local/bin/poetry install --no-dev -v 

CMD ["python", "./src/main.py"]
