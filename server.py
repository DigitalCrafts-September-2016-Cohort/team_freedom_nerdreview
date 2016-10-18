from flask import Flask, render_template, request, redirect, session, flash
import pg

db = pg.DB(dbname='project_db')

app = Flask('NerdReview')

# Renders the homepage at the root directory
@app.route('/')
def display_page():
    return render_template('/homepage.html')

# Selects all of the names from the category table and renders them in the categories.html page
@app.route('/categories')
def render_categories():
    query = db.query('select * from main_cat')
    return render_template(
        '/categories.html',
        result_list = query.namedresult()
    )

@app.route('/categories/<sub_cat>')
def render_sub_cats(sub_cat):
    query = db.query('select product.name from product_uses_category inner join products on product_uses_category.product_id = product.id')


# Selects all of the names from the review table and renders them in the reviews.html page
@app.route('/reviews')
def render_reviews():
    # We can extract the rest of the data we need in the query later
    query = db.query('select * from review')
    return render_template(
        '/reviews.html',
        result_list = query.namedresult()
    )

# Selects all of the names from the company table and renders them in the companies.html page
@app.route('/companies')
def render_companies():
    query = db.query('select * from company')
    return render_template(
        '/companies.html',
        result_list = query.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)
