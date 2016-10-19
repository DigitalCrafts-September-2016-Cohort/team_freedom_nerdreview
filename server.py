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
   cat_query = db.query('select * from main_cat')
   return render_template(
      '/categories.html',
      categories_list = cat_query.namedresult()
   )

@app.route('/categories/<cat_id>')
def render_sub_cats(cat_id):
   # Reduce reduncancy by joining tables and being more specific in our select
   cat_query = db.query('select * from main_cat')
   sub_cat_query = db.query('select product.name as prod_name, avg(review.rating) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join secondary_cat on secondary_cat.id = %s group by product.name' % cat_id)
   return render_template(
      '/sub_categories.html',
      cat_id = cat_id,
      categories_list = cat_query.namedresult(),
      sub_categories_list = sub_cat_query.namedresult()
   )

@app.route('/categories/<cat_id>/<sub_cat_id>')
def render_sub_cat_products(cat_id, sub_cat_id):
   # Reduce reduncancy by joining tables and being more specific in our select
   sub_cat_query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = %s' % cat_id)
   sub_cat_products_query = db.query('select product.name, product_uses_category.id from product_uses_category inner join product on product.id = product_uses_category.product_id where product_uses_category.secondary_cat_id = %s' % sub_cat_id)

   sub_cat_query = db.query('select product.name as prod_name, avg(review.rating) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join secondary_cat on secondary_cat.id = %s group by product.name' % cat_id)
   
   return render_template(
      '/sub_categories_products.html',
      cat_id = cat_id,
      sub_categories_list = sub_cat_query.namedresult(),
      sub_categories_products_list = sub_cat_products_query.namedresult()
   )

# Selects all of the names from the review table and renders them in the reviews.html page
@app.route('/reviews')
def render_reviews():
   # We can extract the rest of the data we need in the query later
   query = db.query('select product.name as prod_name, review.rating, users.name as user_name, review.id from review, product, users where review.product_id = product.id and review.user_id = users.id')
   return render_template(
      '/reviews.html',
      reviews_list = query.namedresult()
   )

@app.route('/reviews/<review_id>')
def render_individual_review(review_id):
    review_query = db.query("select product.name as prod_name, review.rating, review.date, users.name as user_name, review.id, review.review from review, product, users where review.product_id = product.id and review.user_id = users.id and review.id = '%s'" % review_id)
    return render_template(
      '/individual_review.html',
      review = review_query.namedresult()[0]
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
