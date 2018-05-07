import json
import os

import falcon
import psycopg2
import psycopg2.extras


class HealthHandler(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


class TodosHandler(object):

    def on_get(self, req, resp):
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM public.todo")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(todos, sort_keys=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        body = json.loads(req.req_body)
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor()
        cur.execute("INSERT INTO public.todo (title, status) VALUES ('{}', '{}')"
            .format(body['title'], body['status']))
        conn.commit()
        cur.close()
        conn.close()
        resp.status = falcon.HTTP_200
		
	    def on_put(self, req, resp, todoID=''):
        body = json.loads(req.req_body)
        todoID = str(todoID)
        if todoID.isdigit() is False:
            error_message = {'Error': 'ID is incorrect'}
            resp.body = json.dumps(error_message, sort_keys=False)
            resp.status = falcon.HTTP_404
        elif body is None:
            error_message = {'Error': 'Empty request'}
            resp.body = json.dumps(error_message, sort_keys=False)
        else:
            try:
                conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                         dbname=os.environ["DB_NAME"],
                                         user=os.environ["DB_USER"],
                                         password=os.environ["DB_PASSWORD"])
            except (Exception, psycopg2.DatabaseError) as e:
                print("cannot connect to database /n")
                print(e)
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("""UPDATE public.todo set title = '{}', status = {}, where id = {}""".format(body['title'],
                    body['status'], todoID))
            conn.commit()
            # conn.set_isolation_level(0)
            cur.execute("""SELECT * FROM public.todo where id = {}""".format(todoID))
            todos = cur.fetchone()
            resp.set_header('Content-Type', 'application/json')
            resp.body = json.dumps({'status': todos['status'][0]})
            cur.close()
            conn.close()
            resp.status = falcon.HTTP_200
