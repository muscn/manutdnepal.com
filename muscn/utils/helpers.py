import facebook
from django.conf import settings

def facebook_api():
    graph = facebook.GraphAPI(access_token=settings.FB_ACCESS_TOKEN, version='2.5')
    return graph

def insert_row(ws, row, args):
    for i, value in enumerate(args):
        cell = ws.cell(row=row, column=i + 1)
        cell.value = value
    return row + 1