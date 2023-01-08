FROM python:alpine3.15

RUN pip install flask requests flask_sqlalchemy

COPY . /app

EXPOSE 5000

WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "coffee_shop_api/main.py" ]