import json

class Book():
    def insertBooks(author,title):
        author = str(author)
        title = str(title)

        f = open("books.json", "r+")
        contents = f.readlines()
        f.close()

        jsonStr = json.dumps(Book.getBooks())
        jsonDict = json.loads(jsonStr)

        for bookElement in jsonDict:
            if bookElement.get('author') == author and bookElement.get('title') == title:
                error_message = {"error": "Another book with similar title and author already exists."}
                jsonObject = json.dumps(error_message)
                json_response = json.loads(jsonObject)
                return json_response, 400
            else:
                pass

        if len(contents) == 0: # ID initial value check
            id = 1

        else:
            lastJson = json.loads(contents[(len(contents)-1)])
            id = lastJson["id"] + 1

        jsonString = {"id": id, "author": author, "title": title}
        jsonObject = json.dumps(jsonString)
        f = open("books.json" , "a+")
        f.write(jsonObject + "\n")
        f.close()
        contents = Book.getBooks()
        return contents[len(contents) - 1]

    def getBooks():
        f = open("books.json", "r+")
        contests = f.readlines()
        jsonList = []
        for i in range (0, len(contests)):
            jsonList.append(json.loads(contests[i]))
        return jsonList

    def deleteBookList():
        f = open("books.json","w+")
        f.truncate()

    def getBookWithID(id):
        jsonStr = json.dumps(Book.getBooks())
        jsonDict = json.loads(jsonStr)
        jsonElementDict = {}

        for jsonElement in jsonDict:
            if id == jsonElement.get('id'):
                jsonElementDict = jsonElement

        return jsonElementDict