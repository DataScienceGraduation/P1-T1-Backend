FROM python:3.11-alpine
LABEL authors="khaled"

COPY requirements.txt requirements.txt
RUN \
 curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.10.5.1-1_amd64.apk && \
 curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.10.1.1-1_amd64.apk && \
 sudo apk add --allow-untrusted msodbcsql17_17.10.5.1-1_amd64.apk && \
 sudo apk add --allow-untrusted mssql-tools_17.10.1.1-1_amd64.apk && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . /app
WORKDIR /app

EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]