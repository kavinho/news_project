import tornado
from tornado.web import RequestHandler
from service import SearchService

class SearchHandler(RequestHandler):

    def initialize(self, search_service: SearchService):
        self.search_service = search_service     

    async def get(self):
        await self.do_find()

    async def do_find(self):

        self.set_header('Content-Type', 'application/json')
        query = self.get_query_argument("query", "")

        if query == "":
            self.set_status(400)
            self.finish({"reason": "missing 'query' parameter"})
        else:    
            self.write({"results": await self.search_service.find(query)})
