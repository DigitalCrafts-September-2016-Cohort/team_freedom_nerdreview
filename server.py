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
    sub_cat_query = db.query('select product.name as prod_name, product.id as prod_id, round(avg(review.rating), 2) as avg_rating,  count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.main_cat_id = %s group by product.name, prod_id' % cat_id)
    return render_template(
        '/sub_categories.html',
        cat_id = cat_id,
        categories_list = cat_query.namedresult(),
        sub_categories_list = sub_cat_query.namedresult()
    )


@app.route('/categories/<cat_id>/<sub_cat_id>')
def render_sub_cat_products(cat_id, sub_cat_id):
    #Gets all the secondary categories in the main category
    sub_cat_query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = %s' % cat_id)

    #Gets all products in the secondary category with id = sub_cat_id
    ## THIS IS THE RIGHT ONE
    sub_cat_products_query = db.query('select product.name as prod_name, product.id as prod_id, round(avg(review.rating), 2) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.id = %s group by product.name, product.id order by prod_name' % sub_cat_id)


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
    product_reviews_summary_query = db.query('select count(review.id) as review_count, round(avg(review.rating), 2) as avg_rating from product inner join review on review.product_id = product.id and product.id = %s' % product_id)

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
# Redirects (refreshes the page) to this route every time a different option is selected from the sort element
@app.route('/reviews', methods=['POST', 'GET'])
def render_reviews():
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_high', 'rating_low']
    sort_choice_list_names = ['Rating (Highest to Lowest)', 'Rating (Lowest to Highest)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_high':
        sort_method = 'review.rating'
        direction = 'desc'
    elif sort_choice == 'rating_low':
        sort_method = 'review.rating'
        direction = ''
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'prod_name'
        direction = 'desc'

    #Use string substiution to run a SQL query for the selected sort choice
    sorted_review_query = db.query("select product.name as prod_name, review.rating, users.name as user_name, review.id from review, product, users where review.product_id = product.id and review.user_id = users.id order by %s %s" % (sort_method, direction))

    #Render reviews template again with the chosen sort order, passing through the sort choices zipped list, the current choice, and the reviews list
    return render_template(
        'reviews.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        reviews_list = sorted_review_query.namedresult(),
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
@app.route('/brands', methods = ['POST', 'GET'])
def render_brands():
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['name_za', 'num_prod_desc', 'num_prod_asc']
    sort_choice_list_names = ['Product Name (Z-A)', 'Number of Products (high to low)', 'Number of Products (low to high)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'name_za':
        sort_method = 'company.name'
        direction = 'desc'
    elif sort_choice == 'num_prod_desc':
        sort_method = 'prod_count'
        direction = 'desc'
    elif sort_choice == "num_prod_asc":
        sort_method = 'prod_count'
        direction = ''
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'company.name'
        direction = ''

    brand_query = db.query("select company.name as brand_name, company.id as brand_id, count(product.id) as prod_count from company inner join product on company.id = product.company_id group by brand_name, brand_id order by %s %s" % (sort_method, direction))

    return render_template(
        '/brands.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        brand_list = brand_query.namedresult()
    )


@app.route('/brands/<brand_id>')
def render_brand_prod(brand_id):
    brand_prod_query = db.query('select product.name as prod_name, product.id as prod_id from product inner join company on product.company_id = %s group by product.name, product.id' % brand_id)
    return render_template(
        '/brand_products.html',
        brand_prod_list = brand_prod_query.namedresult()
    )


# Users page
@app.route('/users')
def users():
    user_list = db.query("select * from users").namedresult()
    return render_template(
        '/users.html',
        user_list = user_list
    )


@app.route('/product_review')
def render_review():
    return render_template(
        '/add_product_review.html'
    )


# Route and method for the
@app.route('/add_product_review', methods=['POST'])
def add_review():
    main_cat_name = request.form.get('main_cat_name')
    second_cat_name = request.form.get('second_cat_name')
    product_name = request.form.get('product_name')
    rating = request.form.get('rating')
    review = request.form.get('review')
    company_name = request.form.get('company_name')
    # Checks the input against the main_cat table
    main_cat_check = db.query("select name, id from main_cat where main_cat.name = '%s'" % main_cat_name).namedresult()
    if main_cat_check:
        main_category_id = main_cat_check[0].id
    else:
        db.insert(
            'main_cat',
            name=main_cat_name,
        )
        main_cat_check = db.query("select * from main_cat where main_cat.name = '%s'" % main_cat_name).namedresult()
        main_category_id = main_cat_check[0].id
    # Checks the
    second_cat_check = db.query("select * from secondary_cat where secondary_cat.name = '%s'" % second_cat_name).namedresult()
    if second_cat_check:
        second_cat_id = second_cat_check[0].id
    else:
        db.insert(
            'secondary_cat',
            name=second_cat_name,
            main_cat_id=main_category_id
        )
        second_cat_check = db.query("select * from secondary_cat where secondary_cat.name = '%s'" % second_cat_name).namedresult()
        second_cat_id = second_cat_check[0].id

    company_check = db.query("select * from company where company.name = '%s'" % company_name).namedresult()
    if company_check:
        comp_id = company_check[0].id
    else:
        db.insert(
            'company',
            name=company_name
        )
        company_check = db.query("select * from company where company.name = '%s'" % company_name).namedresult()
        comp_id = company_check[0].id

    product_check = db.query("select * from product where product.name = '%s'" % product_name).namedresult()
    if product_check:
        prod_id = product_check[0].id
        db.insert(
            'product_uses_category',
            product_id=prod_id,
            secondary_cat_id=second_cat_id
        )
    else:
        db.insert(
            'product',
            name=product_name,
            company_id=comp_id
        )
        product_check = db.query("select product.id from product where product.name = '%s'" % product_name).namedresult()
        prod_id = product_check[0].id
        db.insert(
            'product_uses_category',
            product_id=prod_id,
            secondary_cat_id=second_cat_id
        )

    db.insert(
        'review',
        product_id=prod_id,
        rating=rating,
        review=review
    )
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
