from Book import Book
import requests
import json

BASE = "http://127.0.0.1:5000"

class TestCases():

    def test_beforeTestCheckEmptyStore(self): # Verify that the API starts with an empty store.
        Book.deleteBookList()
        response = requests.get(BASE + "/api/books/")
        if len(response.json()) == 0 and response.status_code == 200:
            assert True
        else:
            assert False

    def test_verifyAuthorField(self): # author field is required
        test_data = '{"title": "Reliability of late night deployments"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        json_object = json.loads(data)

        if response.status_code == 400:
            responseMessage = json_object['error']
            if responseMessage == "Field 'author' is required":
                assert True
            else:
                assert False
        else:
            assert False

    def test_verifyTitleField(self): # title field is required
        test_data = '{"author": "John Smith"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        json_object = json.loads(data)

        if response.status_code == 400:
            responseMessage = json_object['error']
            if responseMessage == "Field 'title' is required":
                assert True
            else:
                assert False
        else:
            assert False

    def test_idFieldisReadOnly(self): # Verify that the id field is read−only.
        test_data = '{"id": "5"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/5", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        json_object = json.loads(data)
        if response.status_code == 400:
            responseMessage = json_object['error']
            if responseMessage == "ID Field is read-only":
                assert True
            else:
                assert False
        else:
            assert False

    def test_emptyAuthorField(self): # Verify that author cannot be empty.
        test_data = '{"author": "", "title": "SRE 101"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        response_json_object = json.loads(data)
        if response.status_code == 400:
            responseMessage = response_json_object['error']
            if responseMessage == "Field 'author' cannot be empty":
                assert True
            else:
                assert False
        else:
            assert False

    def test_emptyTitleField(self): # Verify that title cannot be empty.
        test_data = '{"author": "John Smith", "title": ""}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        response_json_object = json.loads(data)
        if response.status_code == 400:
            responseMessage = response_json_object['error']
            if responseMessage == "Field 'title' cannot be empty":
                assert True
            else:
                assert False
        else:
            assert False

    def test_emptyAuthorAndTitleField(self): # Verify that author and title cannot be empty.
        test_data = '{"author": "", "title": ""}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        response_json_object = json.loads(data)
        if response.status_code == 400:
            responseMessage = response_json_object['error']
            if responseMessage == "Fields 'author' and 'title' cannot be empty":
                assert True
            else:
                assert False
        else:
            assert False

    def test_createNewBook(self): # Verify that you can create a new book via PUT.
        author = "John Smith"
        title = "SRE 101"
        test_data = '{"author": "' + author + '", "title": "' + title + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        response_json_object = json.loads(data)
        response_get_created_book = requests.get(BASE + "/api/books/" + str(response_json_object['id']))
        data = json.dumps(response_get_created_book.json(), indent=4)
        response_get_created_book_object = json.loads(data)
        if response.status_code == 200: # The book should be returned in the response. (Control Requirement)
            if response_json_object['author'] == author and response_json_object['title'] == title:
                assert True
            else:
                assert False
        if response_get_created_book.status_code == 200: # GET on /api/books/<book_id>/ should return the same book.(Control Requirement)
            if response_json_object['author'] == response_get_created_book_object['author'] and response_json_object['title'] == response_get_created_book_object['title']:
                assert True
            else:
                assert False

    def test_checkCreateDuplicateBook(self): # Verify that you cannot create a duplicate book.
        author = "John Smith"
        title = "SRE 101"
        test_data = '{"author": "' + author + '", "title": "' + title + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        data = json.dumps(response.json(), indent=4)
        response_json_object = json.loads(data)
        if response.status_code == 400:
            responseMessage = response_json_object['error']
            if responseMessage == "Another book with similar title and author already exists.":
                assert True
            else:
                assert False
        else:
            assert False

    def test_CheckMultipleBookList(self):
        author = "Jane Archer"
        title = "DevOps is a lie"
        test_data = '{"author": "' + author + '", "title": "' + title + '"}'
        headers = {"Content-Type": "application/json"}
        response = requests.put(BASE + "/api/books/", data=test_data, headers=headers)
        response_get_books = requests.get(BASE + "/api/books/")
        data = json.dumps(response_get_books.json(), indent=4)
        response_json_object = json.loads(data)
        if str(response_json_object) == "[{'id': 1, 'author': 'John Smith', 'title': 'SRE 101'}, {'id': 2, 'author': 'Jane Archer', 'title': 'DevOps is a lie'}]":
            assert True
        else:
            assert False

    def test_getBookWithID(self):
        response_get_book = requests.get(BASE + "/api/books/2")
        data = json.dumps(response_get_book.json(), indent=4)
        response_json_object = json.loads(data)
        if response_json_object.get('id') == 2 and response_json_object.get('author') == 'Jane Archer' and response_json_object.get('title') == 'DevOps is a lie':
            assert True
        else:
            assert False




