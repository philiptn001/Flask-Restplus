import pandas as pd
from flask import Flask, request
from flask_restplus import Resource, Api, fields, reqparse, inputs
import json

app = Flask(__name__)
api = Api(app,
        default="Books", #swagger default namespace
        title="Book Dataset", #swagger title
        description="Flask-Restplus using book dataset ") #swagger description

#Book model expected as input
book_model = api.model('Book', {
    'Flickr_URL': fields.String,
    'Publisher': fields.String,
    'Author': fields.String,
    'Title': fields.String,
    'Date_of_Publication': fields.Integer,
    'Identifier': fields.Integer,
    'Place_of_Publication': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in book_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)

@api.route('/books')
class Bookslist(Resource):

    @api.response(200, 'Sucessful')
    @api.doc(description='Get all books')
    def get(self):
        args = parser.parse_args()

        #reading the input from user
        order = args.get('order')
        ascending = args.get('ascending', True)

        if order:
            df.sort_values(by=order, implace=True, ascending=ascending)
        
        json_str = df.to_json(orient='index')

        ds = json.loads(json_str)  # str json to real json

        final_ds = []

        for idx in ds:
            book = ds[idx]
            book['Identifier'] = int(idx)
            final_ds.append(book)

        return final_ds

    @api.response(201, 'Book created successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description= "Add a new book")
    @api.expect(book_model, validate=True)
    def post(self):
        book = request.json
        print(book['Identifier'])
        if 'Identifier' not in book:
            return {"message": "Missing Identifier"}, 400

        id = book['Identifier']

        if id in df.index:
            return{"message": "Identifier already exist in book dataset"}

        for key in book:
            if key not in book_model.keys():
                return {"message": "{} is invalid".format(key)}, 400
            df.loc[id,key] = book[key]

        return {"message": "Book {} is created".format(id)}, 201

@api.route('/books/<int:id>')
@api.param('id', 'The Book identifier')
class Books(Resource):
    @api.response(404, 'Book not found')
    @api.response(200, 'Book data retrieved Successfully')
    @api.doc(description="Get a book by its ID")
    def get(self,id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        
        book = dict(df.loc[id])
        return book

    @api.response(404, 'Book was not found')
    @api.response(200, 'Book data deleted Successfully')
    @api.doc(description="Delete a book by its ID")
    def delete(self,id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        df.drop(id, inplace=True)
        return {"Message": "Book {} is removed.".format(id)},200

    @api.response(404, 'Book not found')
    @api.response(400, 'Validation Error')
    @api.response(200, 'Book got updated Successfully')
    @api.expect(book_model, validate=True)
    @api.doc(description="Update a book by its ID")
    def put(self,id):
        if id not in df.index:
            api.abort(404, "Book {} doesn't exist".format(id))
        
        # get the payload and convert it into json
        book = request.json

        # Book ID cannot be changed
        if 'identifier' in book and id != book['identifier']:
            return{"Message": "identifier cannot be changed".format(id)},400

        # update the values
        for key in book:
            if key not in book_model.keys():
                #unexpected column
                return {"message" : "Identifier cannot be changed".format(i)},400
            df.loc[id,key] = book[key]

        return {"Message": "Book {} has been successfully updated.".format(id)},200

if __name__ == '__main__':
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    csv_file = "Books.csv"
    df = pd.read_csv(csv_file)

    # drop unnecessary columns
    df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date

    # replace spaces in the name of columns
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # set the index column; this will help us to find books with their ids
    df.set_index('Identifier', inplace=True)

    # run the application
    app.run(debug=True)