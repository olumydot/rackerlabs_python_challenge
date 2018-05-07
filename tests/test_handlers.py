import unittest
from unittest import main
import urllib
import urllib.request
import falcon
from handlers import TodosHandler


class TestHandlers(unittest.TestCase):

    def test_onPut(self):

        data = {'title': 'unittest', 'status': 'passed OK'}
        data = urllib.parse.urlencode(data)
        req = urllib.request.Request('todos/1', data)
        resp = urllib.request.urlopen(req)
        exp = TodosHandler.on_put(req, resp, todoID=1)
        result = {'status': 'passed OK',}
        self.assertTrue(exp.json, result)
        self.assertTrue(exp.status, falcon.HTTP_200)


if __name__ == '__main__':
    main()
