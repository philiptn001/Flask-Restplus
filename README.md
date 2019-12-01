# Flask-Restplus
Project to learn REST services which allows developers to build lightweight and scalable web services.

Process:
* Get a Book by its ID
* Removing a Book by its ID
* Update Book Information
* Get a List of Books
* Add a new Book
* Improving Swagger Documentation

Steps:

##1
* Create a flask-restplus application
* Read the dataset using Pandas as a global variable
* Drop the unnecessary columns and apply all cleansing techniques
* Set the index of the loaded dataframe to be the "Identifier" column. This will help us to find books with their ids
* Replace the spaces in the column names
* Create a Resource class and implement its "get" method. The method must accept "id" as an input and return the book matching the id by querying the dataframe or by index . The response must be a JSON.
* When there is no book matching the id, the method must return a proper message and HTTP response code .
* Run the application and browse http://127.0.0.1:5000/ to test the endpoint. The given URL will show an automatically generated swagger doc for your application; you can use the swagger doc to test your API

##2
* Add a new method called delete to your resource class, delete the given book by its id and return a proper message indicating that the given id has been removed
* When there is no book matching the id, the method must return a proper message and HTTP response code.
* Run the application and browse http://127.0.0.1:5000/ to test the endpoint. Test your API to see if it works properly.

##3
* Add a new method called "put" to your resource class:
* Using the expect() decoder, specify an example payload for the endpoint
* Check if the given book identifier exists, and return a proper message if it does not exist
* Get the payload of request
* Iterate over the key-values of the payload and update the dataframe
* Return error messages if the input includes unexpected keys
* Run the application and browse http://127.0.0.1:5000/ to test the endpoint. Test your API to see if it works properly.

##4
* Create a new resource class and add a new method called get to your resource class
* The method must return all books in the dataset which can be ordered (ascending or descending order) by any of columns. Use query parameters to pass the column name and order type
* You need to use a decorator called expect() which accepts a request parser as input; this will automatically help flask-restplus to generate appropriate swagger doc which includes inputs for query parameters
* Run the application and browse http://127.0.0.1:5000/ to test the endpoint. Test your API to see if it works properly.

##5
* Create a new method named "post". Details of a new book should be posted via request payload.
* The endpoint must return appropriate error message if the given id (book identifier) already exists in the dataset
* Iterate over the key-values of the payload and update the dataframe
* Return error messages if the input includes unexpected keys
* Run the application and browse http://127.0.0.1:5000/ to test the endpoint. Test your API to see if it works properly.

##6
* When creating an instance of API class, specify the title, description, default namespace, and version of the API.
* Use @api.response to indicate which HTTP response code does each method returns and what they mean
* Use @api.param to add descriptions for the parameters
* Use @api.doc to add descriptions for API methods