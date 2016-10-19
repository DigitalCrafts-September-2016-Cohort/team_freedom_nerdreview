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
   cat_query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = %s' % cat_id)
   sub_cat_query = db.query('select product.id as prod_id, product.name as prod_name, avg(review.rating) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join secondary_cat on secondary_cat.id = %s group by product.name, product.id' % cat_id)

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
   sub_cat_products_query = db.query('select product.id as prod_id, product.name as prod_name, avg(review.rating) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.id = %s group by product.name, product.id order by prod_name' % sub_cat_id)

   return render_template(
      '/sub_categories_products.html',
      cat_id = cat_id,
      sub_categories_list = sub_cat_query.namedresult(),
      sub_categories_products_list = sub_cat_products_query.namedresult()
   )


#Displays a page for a single product, navbar menu stays the same
@app.route('/products/<product_id>')
def disp_individual_product(product_id):
    # Gets the main category id number for the product
    main_cat = db.query('select main_cat.id as main_id from product inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id inner join main_cat on secondary_cat.main_cat_id = main_cat.id and product.id = %s' % product_id).namedresult()[0].main_id

    #Gets all the secondary categories in the main category (above)
    parent_categories_list = db.query('select secondary_cat.id as sub_cat_id, secondary_cat.name as cat_name from secondary_cat where secondary_cat.main_cat_id = %s' % main_cat)

    #Gets the individual product
    product_query = db.query('select * from product where product.id = %s' % product_id)

    #Gets the summary stats (count, avg rating) for all the product (see above) reviews
    product_reviews_summary_query = db.query('select count(review.id) as review_count, avg(review.rating) as avg_rating from product inner join review on review.product_id = product.id and product.id = %s' % product_id)

    #Gets all the reviews for the indiviudal product from above
    reviews_query = db.query('select review.id as review_id from product inner join review on product.id = review.product_id and product.id = %s' % product_id)

    return render_template(
    'individual_product.html',
    cat_id = main_cat,
    parent_categories = parent_categories_list.namedresult(),
    product = product_query.namedresult()[0],
    product_summary = product_reviews_summary_query.namedresult()[0],
    reviews_list = reviews_query.namedresult()

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

@app.route('/icon')
def icon():
   return render_template(
      '/icon.html'
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

# Users page
@app.route('/users')
def users():
   user_list = db.query("select * from users").namedresult()
   return render_template(
      '/users.html',
      user_list = user_list
   )

if __name__ == '__main__':
   app.run(debug=True)
