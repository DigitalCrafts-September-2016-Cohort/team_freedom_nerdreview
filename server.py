from flask import Flask, render_template, request, redirect, session, flash
import pg

db = pg.DB(dbname='project_db')

app = Flask('NerdReview')

@app.route('/')
def display_page():
    return render_template('/homepage.html')

@app.route('/categories')
def render_categories():
    query = db.query('select * from main_cat')
    return render_template(
        '/categories.html',
        result_list = query.namedresult()
    )

@app.route('/review')
def render_reviews():
    # We can extract the rest of the data we need in the query later
    query = db.query('select * from review')
    return render_template(
        '/reviews.html',
        result_list = query.namedresult()
    )

@app.route('/companies')
def render_reviews():
    query = db.query('select * from company')
    return render_template(
        '/companies.html',
        result_list = query.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)
