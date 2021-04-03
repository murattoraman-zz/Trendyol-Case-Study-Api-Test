import flask
from flask import abort
from flask import request
from flask_restful import Api, Resource
import json

from pyasn1.compat.octets import null

from Book import Book

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

class MockAPI():

    @app.route('/api/books/', methods=['GET'])
    def getBooks():
        jsonBookList = json.dumps(Book.getBooks(),indent=4)
        app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
        app.logger.debug('Response : %s', jsonBookList)
        return jsonBookList

    @app.route('/api/books/', methods=['PUT'])
    def putInsertBook():
        try:
            json_request = json.loads(request.data.decode("utf-8"))
            author = json_request['author']
            title = json_request['title']
            if len(author) != 0 and len(title) != 0:
                app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
                return Book.insertBooks(author, title)
            elif len(author) == 0 and len(title) != 0:
                data_set = {"error": "Field 'author' cannot be empty"}
                json_dump = json.dumps(data_set)
                json_response = json.loads(json_dump)
                app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
                app.logger.debug('Response : %s', json_response)
                return json_response, 400
            elif len(author) != 0 and len(title) == 0:
                data_set = {"error": "Field 'title' cannot be empty"}
                json_dump = json.dumps(data_set)
                json_response = json.loads(json_dump)
                app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
                app.logger.debug('Response : %s', json_response)
                return json_response, 400
            elif len(author) == 0 and len(title) == 0:
                data_set = {"error": "Fields 'author' and 'title' cannot be empty"}
                json_dump = json.dumps(data_set)
                json_response = json.loads(json_dump)
                app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
                app.logger.debug('Response : %s', json_response)
                return json_response, 400
            else:
                app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
                return 500

        except KeyError as ke:
            data_set = {"error" : "Field " + str(ke) + " is required"}
            json_dump = json.dumps(data_set)
            json_response = json.loads(json_dump)
            app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
            app.logger.debug('Response : %s', json_response)
            return json_response, 400

    @app.route('/api/books/<int:id>', methods=['PUT'])
    def invalidPutRequest(id):
        data_set = {"error": "ID Field is read-only"}
        json_dump = json.dumps(data_set)
        json_response = json.loads(json_dump)
        app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
        app.logger.debug('Response : %s', json_response)
        return json_response, 400

    @app.route('/api/books/<int:id>', methods=['GET'])
    def getBookWithID(id):
        data_set = {"error": "Given ID does not exist"}
        json_dump = json.dumps(data_set)
        json_error_response = json.loads(json_dump)

        jsonBookItem = json.dumps(Book.getBookWithID(id), indent=4)
        json_response = json.loads(jsonBookItem)
        if len(json_response) == 0:
            app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
            app.logger.debug('Response : %s', json_error_response)
            return json_error_response, 404
        else:
            app.logger.debug('Request Body: %s', request.get_data().decode("utf-8"))
            app.logger.debug('Response : %s', json_response)
            return json_response, 200

if __name__ == "__main__":
    app.run(debug=True)