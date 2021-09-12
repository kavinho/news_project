from typing import get_args
import motor.motor_tornado
import tornado
import tornado.web
from search_handler import SearchHandler
from service import SearchService
import settings
from query_builder import build_mongo_query

def get_app(mongo_url, query_builder):

    mongo_items = motor.motor_tornado.MotorClient(mongo_url,serverSelectionTimeoutMS=1000).items

    application = tornado.web.Application([
        (r'/find', SearchHandler, {'search_service': SearchService(mongo_items ,query_builder)})
    ])

application = get_app(settings.MONGO_URI, build_mongo_query)

server = tornado.httpserver.HTTPServer(application)
server.bind(settings.APP_PORT)

# To Forks one process per CPU. server.start(0)
server.start()

print("whirling tornado on {}".format(settings.APP_PORT))
tornado.ioloop.IOLoop.current().start()
