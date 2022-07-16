from tokenize import Number
from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
import json
from uuid import UUID


# mockData
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is ..'},
    {'id': 2, 'title': 'view', 'body': 'View is ..'},
    {'id': 3, 'title': 'Model', 'body': 'Model is ..'},
]

# db(postgres connection)
connection = psycopg2.connect(host='localhost', dbname='mvp',
                              user='postgres', password='postgres', port=5432)

cursor = connection.cursor()


def uuid_convert(o):
    if isinstance(o, UUID):
        return o.hex


def find_user_rfqs(request, quotation_user_id):
    postgreSQL_select_Query = f'''
        select cr.id as "id", cr.seq as "seq" from capa_rfq cr
        inner join capa_quotation_user cqu on cqu.id = cr.quotation_user_id 
        where cr.quotation_user_id  = '{quotation_user_id}'
        limit 1;
    '''

    cursor.execute(postgreSQL_select_Query)

    fetch_user_rfq_list = cursor.fetchall()

    ol = ''

    for rfqInfo in fetch_user_rfq_list:
        # json 변환 test
        jsonStr = json.dumps(rfqInfo, indent=4, default=uuid_convert)

        ol += f'<li>{rfqInfo[0]}</li><li>{rfqInfo[1]}</li>'

    return HttpResponse(f'''
    <html>
        <head>
            <meta charset="utf-8">
            <title>My test page</title>
        </head>
        <body>
            <p>This is my page</p>
            {ol}
        </body>
        </html>
    ''')


def page_fun():
    global topics
    ol = ''

    for topic in topics:
        print('topic', topic)
        ol += f'<li><a href="read/{topic["id"]}/">{topic["title"]}</a></li>'

    return ol


def index(request):

    return HttpResponse(f'''
        <html >
        <head >
            <meta charset = "utf-8" >
            <title > My test page < /title >
        </head >
        <body >
            <p > This is my page < /p >
            <ol >
            {page_fun()}
            </ol >
        </body >
        </html >
        ''')


def create(request):
    return HttpResponse('create!')


def read(request, id):
    global topics
    for topic in topics:
        if topic['id'] == int(id):
            return HttpResponse(f'''{topic["body"]}!''')
