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

@app.route('/categories/<cat_id>')
def render_sub_cats(cat_id):
    query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = %s' % cat_id)
    return render_template(
        '/sub_categories.html',
        result_list = query.namedresult()
    )

@app.route('/categories/<cat_id>/<sub_cat_id>')
def render_sub_cat_products(sub_cat_id):
    query = db.query('select * from products where products.secondary_cat_id = %s' % sub_cat_id)
    return render_template(
        '/sub_categories_products.html',
        result_list = query.namedresult()
    )

# Selects all of the names from the review table and renders them in the reviews.html page
@app.route('/reviews')
def render_reviews():
    # We can extract the rest of the data we need in the query later
    query = db.query('select * from review')
    return render_template(
        '/reviews.html',
        result_list = query.namedresult()
    )

# Selects all of the names from the company table and renders them in the brands.html page
@app.route('/brands')
def render_brands():
    query = db.query('select * from company')
    return render_template(
        '/brands.html',
        result_list = query.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)
