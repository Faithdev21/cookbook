FROM python:3.9

WORKDIR /app

COPY README.md pyproject.toml poetry.lock ./

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY backend/test_project .

ENV DJANGO_SETTINGS_MODULE=test_project.settings

RUN python manage.py collectstatic \
    && cp -r /app/collected_static/. /static/

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "test_project.wsgi:application"]








