import sys,os

sys.path.insert(0, '/var/www/html/')
from project import app as application
root_path = os.path.dirname(os.path.abspath(__file__))

'''def application(environ, start_response):
    application.root_path = '/var/www/html/'
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    status = '200 OK'
    output = 'Hello Udacity! '+os.getcwd()
    output = 'Hello Udacity! '+current_app.root_path
    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
'''