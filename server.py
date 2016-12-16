from flask import Flask, render_template, request, redirect, session, flash
import pg
from dotenv import load_dotenv, find_dotenv
import os
import datetime

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

db = pg.DB(
    dbname=os.environ.get('NERDREVIEW_PG_DBNAME'),
    host=os.environ.get('NERDREVIEW_PG_HOST'),
    user=os.environ.get('NERDREVIEW_PG_USERNAME'),
    passwd=os.environ.get('NERDREVIEW_PG_PASSWORD')
)

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('NerdReview', template_folder=tmp_dir)
app.secret_key = "bigbigbig"
# Renders the homepage at the root directory
@app.route('/')
def display_page():
    loggedin = False
    try:
        session['username']
        loggedin = True
    except:
        loggedin = False
    return render_template(
        '/homepage.html',
        loggedin = loggedin
        )

# Log In
@app.route('/log_in', methods=['POST'])
def submit_login():
   username = request.form.get('username')
   password = request.form.get('password')
   results = db.query("select * from users where user_name = $1", username).namedresult()
   if len(results) > 0:
       user = results[0]
       if user.password == password:
           session['username'] = user.user_name
        #    flash("Successfully Logged In")
           return redirect('/')
       else:
           flash("Wrong password - try again!")
           return redirect('/')
   else:
       flash("You don't have an account - sign up instead!")
       return redirect('/')

# Sign up
@app.route('/sign_up', methods=['POST'])
def submit_signup():
   name = request.form.get('name')
   username = request.form.get('username')
   password = request.form.get('password')
   try:
       db.insert('users', name=name, user_name=username, password=password)
       session['username'] = username
    #    flash('Sign Up Succesful')
       return redirect('/')
   except:
       flash('Sign Up Not Succesful')
       return redirect('/')

# Log out
@app.route('/log_out', methods=['POST'])
def log_out():
   del session['username']
   flash("Successfully Logged Out")
   return redirect('/')


# Selects all of the names from the category table and renders them in the categories.html page
@app.route('/categories')
def render_categories():
    cat_query = db.query('select * from main_cat')
    return render_template(
        '/categories.html',
        categories_list = cat_query.namedresult()
    )


@app.route('/categories/<cat_id>', methods = ['POST', 'GET'])
def render_sub_cats(cat_id):
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_asc',
                        'name_az',
                        'name_za']

    sort_choice_list_names = ['Rating (low to high)',
                              'Product Name (A-Z)',
                              'Product Name (Z-A)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_asc':
        sort_method = 'query.avg_rating'
        direction = 'asc'
    elif sort_choice == 'name_az':
        sort_method = 'prod_name_upper'
        direction = 'asc'
    elif sort_choice == 'name_za':
        sort_method = 'prod_name_upper'
        direction = 'desc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'query.avg_rating'
        direction = 'desc'


    # Reduce reduncancy by joining tables and being more specific in our select
    cat_query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = $1', cat_id)

    sub_cat_query = db.query('select distinct query.prod_id, upper(query.prod_name) as prod_name_upper, query.prod_name as product_name, query.review_count, query.avg_rating from (select product_uses_category.secondary_cat_id as sub_cat_id, count(review.product_id) as review_count, product.name as prod_name, product.id as prod_id, round(avg(review.rating), 2) as avg_rating from review inner join product on product.id = review.product_id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.main_cat_id = %s group by prod_name, prod_id, product_uses_category.secondary_cat_id) query order by %s %s' % (cat_id, sort_method, direction))



    return render_template(
        '/sub_categories.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        cat_id = cat_id,
        categories_list = cat_query.namedresult(),
        sub_categories_list = sub_cat_query.namedresult()
    )


@app.route('/categories/<cat_id>/<sub_cat_id>', methods=['POST','GET'])
def render_sub_cat_products(cat_id, sub_cat_id):
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_asc',
                        'name_az',
                        'name_za']

    sort_choice_list_names = ['Rating (low to high)',
                              'Product Name (A-Z)',
                              'Product Name (Z-A)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_asc':
        sort_method = 'avg_rating'
        direction = 'asc'
    elif sort_choice == 'name_az':
        sort_method = 'prod_name_upper'
        direction = 'asc'
    elif sort_choice == 'name_za':
        sort_method = 'prod_name_upper'
        direction = 'desc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'avg_rating'
        direction = 'desc'


    #Gets all the secondary categories in the main category
    sub_cat_query = db.query('select * from secondary_cat where secondary_cat.main_cat_id = $1' , cat_id)

    #Gets all products in the secondary category with id = sub_cat_id
    ## THIS IS THE RIGHT ONE
    sub_cat_products_query = db.query('select product.name as prod_name, upper(product.name) as prod_name_upper, product.id as prod_id, round(avg(review.rating), 2) as avg_rating, count(review.product_id) as review_count from review inner join product on product.id = review.product_id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.id = $1 group by product.name, product.id order by $2 %s' % direction, sub_cat_id, sort_method)


    return render_template(
        '/sub_categories_products.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        cat_id = cat_id,
        sub_cat_id = sub_cat_id,
        sub_categories_list = sub_cat_query.namedresult(),
        sub_categories_products_list = sub_cat_products_query.namedresult()
    )


#Displays a page for a single product, navbar menu stays the same
@app.route('/products/<product_id>', methods = ['POST','GET'])
def disp_individual_product(product_id):
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_low',
                        'date_desc',
                        'date_asc']

    sort_choice_list_names = ['Rating (low to high)',
                              'Date (new to old)',
                              'Date (old to new)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_low':
        sort_method = 'rating'
        direction = 'asc'
    elif sort_choice == 'date_desc':
        sort_method = 'review_date'
        direction = 'desc'
    elif sort_choice == 'date_asc':
        sort_method = 'review_date'
        direction = 'asc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'rating'
        direction = 'desc'

    # Gets the main category id number for the product
    main_cat = db.query('select main_cat.id as main_id from product inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id inner join main_cat on secondary_cat.main_cat_id = main_cat.id where product.id = $1' , product_id).namedresult()[0].main_id

    #Gets all the secondary categories in the main category (above)
    parent_categories_list = db.query('select secondary_cat.id as sub_cat_id, secondary_cat.name as cat_name from secondary_cat where secondary_cat.main_cat_id = $1' , main_cat)

    #Gets the individual product
    product_query = db.query('select * from product where product.id = $1' , product_id)
    company = product_query.namedresult()[0]
    company_id=company.company_id

    #Gets the summary stats (count, avg rating) for all the product (see above) reviews
    product_reviews_summary_query = db.query('select count(review.id) as review_count, round(avg(review.rating), 2) as avg_rating from product inner join review on review.product_id = product.id and product.id = $1' , product_id)

    #Gets all the reviews for the indiviudal product from above
    reviews_query = db.query('select review.id as review_id, review.rating as rating, date(review.date) as review_date, users.user_name from product inner join review on product.id = review.product_id inner join users on users.id = review.user_id and product.id = $1 order by $2 %s' % direction , product_id, sort_method)

    return render_template(
        'individual_product.html',
        cat_id = main_cat,
        parent_categories = parent_categories_list.namedresult(),
        product = product_query.namedresult()[0],
        company_id=company_id,
        product_summary = product_reviews_summary_query.namedresult()[0],
        reviews_list = reviews_query.namedresult(),
        sort_choices = sort_choices,
        current_sort = sort_choice
    )


# Selects all of the names from the review table and renders them in the reviews.html page
# Redirects (refreshes the page) to this route every time a different option is selected from the sort element
@app.route('/reviews', methods=['POST', 'GET'])
def render_reviews():
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_low',
                        'prod_name_az',
                        'prod_name_za',
                        'date_desc',
                        'date_asc']

    sort_choice_list_names = ['Rating (low to high)',
                              'Product Name (A-Z)',
                              'Product Name (Z-A)',
                              'Date (new to old)',
                              'Date (old to new)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_low':
        sort_method = 'rating'
        direction = 'asc'
    elif sort_choice == 'prod_name_az':
        sort_method = 'prod_name_upper'
        direction = 'asc'
    elif sort_choice == 'prod_name_za':
        sort_method = 'prod_name_upper'
        direction = 'desc'
    elif sort_choice == 'date_desc':
        sort_method = 'review_date'
        direction = 'desc'
    elif sort_choice == 'date_asc':
        sort_method = 'review_date'
        direction = 'asc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'rating'
        direction = 'desc'

    #Use string substiution to run a SQL query for the selected sort choice
    sorted_review_query = db.query("select product.name as prod_name, upper(product.name) as prod_name_upper, review.rating, users.user_name as user_name, review.id, date(review.date) as review_date from review, product, users where review.product_id = product.id and review.user_id = users.id order by $1 %s" % direction, sort_method)
    #Render reviews template again with the chosen sort order, passing through the sort choices zipped list, the current choice, and the reviews list
    return render_template(
        'reviews.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        reviews_list = sorted_review_query.namedresult(),
    )

# Click and go back to the homepage
@app.route('/icon')
def icon():
    return render_template(
        '/icon.html'
    )

# It renders to the individual review page
@app.route('/reviews/<review_id>')
def render_individual_review(review_id):
    review_query = db.query("select product.id as prod_id, product.name as prod_name, review.rating, review.user_id as user_id,date(review.date) as review_date, users.user_name as user_name, review.id, review.review from review, product, users where review.product_id = product.id and review.user_id = users.id and review.id = $1" , review_id)

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
        sort_method = 'brand_name_upper'
        direction = 'desc'
    elif sort_choice == 'num_prod_desc':
        sort_method = 'prod_count'
        direction = 'desc'
    elif sort_choice == "num_prod_asc":
        sort_method = 'prod_count'
        direction = 'asc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'brand_name_upper'
        direction = 'asc'

    brand_query = db.query("select company.name as brand_name, upper(company.name) as brand_name_upper, company.id as brand_id, count(product.id) as prod_count from company inner join product on company.id = product.company_id group by brand_name, brand_id order by $1 %s" % direction ,sort_method)

    return render_template(
        '/brands.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        brand_list = brand_query.namedresult()
    )

#
@app.route('/brands/<brand_id>', methods=['POST','GET'])
def render_brand_prod(brand_id):
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['rating_asc',
                        'name_az',
                        'name_za']

    sort_choice_list_names = ['Rating (low to high)',
                              'Product Name (A-Z)',
                              'Product Name (Z-A)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'rating_asc':
        sort_method = 'avg_rating'
        direction = 'asc'
    elif sort_choice == 'name_az':
        sort_method = 'prod_name_upper'
        direction = 'asc'
    elif sort_choice == 'name_za':
        sort_method = 'prod_name_upper'
        direction = 'desc'
    else:
        #Default or fall back sort method (not dependent on drop-down)
        sort_method = 'avg_rating'
        direction = 'desc'

    brand_prod_query = db.query("select product.id as prod_id, upper(product.name) as prod_name_upper, product.name as prod_name, round(avg(review.rating), 2) as avg_rating, count(review.id) as review_count from company inner join product on company.id = product.company_id inner join review on product.id = review.product_id where company.id = $1 group by prod_id, prod_name order by $2 %s" % direction, brand_id, sort_method)

    # brand_prod_query = db.query('select product.name as prod_name, product.id as prod_id from product inner join company on product.company_id = $1 group by product.name, product.id' % brand_id)

    return render_template(
        '/brand_products.html',
        brand_id = brand_id,
        sort_choices = sort_choices,
        current_sort = sort_choice,
        brand_prod_list = brand_prod_query.namedresult()
    )


# Users page and drop down sort bar.
@app.route('/users', methods = ['POST','GET'])
def users():
    #Defines 2 iterable lists for sort choices: one for the value attributes from form and one for the names to display
    sort_choice_list = ['name_za',
                        'num_reviews_desc',
                        'num_reviews_asc']

    sort_choice_list_names = ['User Name (Z-A)',
                              'Num of Reviews (high to low)',
                              'Num of Reviews (low to high)']
    #Zips the two lists together so that we can iterate over the corresponding pairs
    sort_choices = zip(sort_choice_list, sort_choice_list_names)

    # Get the selected sort choice, 'prod_name' if none is selected
    # Two string variables are assigned for each possible choice, they will be substitued into the SQL query below
    sort_choice = request.form.get('sortby')
    if sort_choice == 'name_za':
        sort_method = 'user_name_upper'
        direction = 'desc'
    elif sort_choice == 'num_reviews_desc':
        sort_method = 'review_count'
        direction = 'desc'
    elif sort_choice == 'num_reviews_asc':
        sort_method = 'review_count'
        direction = 'asc'
    else:
        #Fall back sort method
        sort_method = 'user_name_upper'
        direction = 'asc'

    user_list = db.query("select users.id as user_id, upper(users.user_name) as user_name_upper, users.user_name as user_name, count(review.id) as review_count from review inner join users on users.id = review.user_id group by users.id, users.user_name order by $1 %s" % direction, sort_method).namedresult()
    return render_template(
        '/users.html',
        sort_choices = sort_choices,
        current_sort = sort_choice,
        user_list = user_list
    )
# It renders to the individual user page
@app.route('/users/<user_id>')
def render_individual_user(user_id):

    review_list = db.query("select product.name as prod_name, review.id as review_id, review.rating as review_rate, date(review.date) as review_date, users.id as users_id from product inner join review on product.id = review.product_id inner join users on users.id = review.user_id where users.id = $1 order by review.date" , user_id)
    user = db.query("select users.id as user_id, users.user_name as user_name, count(review.id) as review_count from review inner join users on users.id = review.user_id where users.id = $1 group by users.id, users.user_name" , user_id).namedresult()[0]
    print review_list
    return render_template(
        '/individual_user.html',
        reviews = review_list.namedresult(),
        user = user
    )

# It redirects to the page where the things that you reviewed
@app.route('/loggedin_userpage/<user_name>')
def render_user_from_login(user_name):

    user = db.query("select users.id as user_id, users.user_name as user_name from users where users.user_name = $1" , user_name).namedresult()[0]

    user_id=user.user_id

    return redirect(
        '/users/%s' % user_id
    )

# New review
@app.route('/product_review_new', methods=['POST', 'GET'])
def render_review_new():
    #Taking main category choice and returning list of secondary categories to be displayed in next drop down
    main_cat_list = db.query('select name from main_cat').namedresult()
    current_main_cat = request.form.get('main_cat_name')
    new_main_cat = request.form.get('new_main_cat')

    if new_main_cat is not None:
        current_main_cat = new_main_cat
    else:
        current_main_cat = request.form.get('main_cat_name')

    if new_main_cat is None:
        new_main_cat = current_main_cat


    print current_main_cat
    print new_main_cat

    if current_main_cat is None:
        sec_cat_list = []
    elif current_main_cat == 'none':
        sec_cat_list = []
    else:
        sec_cat_list = db.query("select secondary_cat.name as sec_cat_name, secondary_cat.id as sec_cat_id, main_cat.name as main_cat_name, main_cat.id as main_cat_id from secondary_cat inner join main_cat on secondary_cat.main_cat_id = main_cat.id where main_cat.name = $1" , current_main_cat).namedresult()

    #Taking secondary category choice and returning list of brands to be displayed in next drop down
    new_sec_cat = request.form.get('new_sec_cat')
    if new_sec_cat is not None:
        current_secondary_cat = new_sec_cat
    else:
        current_secondary_cat = request.form.get('sec_cat_name')

    if new_sec_cat is None:
        new_sec_cat = current_secondary_cat

    if current_secondary_cat is None:
        brand_list = []
    elif current_secondary_cat == 'none':
        brand_list = []
    else:
        brand_list = db.query("select distinct company.name as brand_name from company inner join product on product.company_id = company.id inner join product_uses_category on product.id = product_uses_category.product_id inner join secondary_cat on product_uses_category.secondary_cat_id = secondary_cat.id where secondary_cat.name = $1" , current_secondary_cat).namedresult()

    #Taking brand choice and returning list of products to be displayed in next drop down
    new_brand = request.form.get('new_brand')
    if new_brand is not None:
        current_brand = new_brand
    else:
        current_brand = request.form.get('company_name')

    if new_brand is None:
        new_brand = current_brand

    if current_brand is None:
        product_list = []
    elif current_brand == 'none':
        product_list = []
    else:
        product_list = db.query("select product.name as product_name from product inner join company on product.company_id = company.id where company.name = $1" , current_brand).namedresult()

    new_product = request.form.get('new_product')
    if new_product is not None:
        current_product = new_product
    else:
        current_product = request.form.get('product_name')

    if new_product is None:
        new_product = current_product

    return render_template(
        '/product_review_new.html',
        main_cat_list = main_cat_list,
        current_main_cat = current_main_cat,
        sec_cat_list = sec_cat_list,
        current_secondary_cat = current_secondary_cat,
        brand_list = brand_list,
        current_brand = current_brand,
        product_list = product_list,
        current_product = current_product,
        new_main_cat = new_main_cat,
        new_sec_cat = new_sec_cat,
        new_brand = new_brand,
        new_product = new_product
    )



@app.route('/product_review', methods=['POST', 'GET'])
def render_review():
    main_cat_query = db.query('select name from main_cat').namedresult()
    second_cat_query = db.query('select name from secondary_cat').namedresult()
    product_query = db.query('select name from product').namedresult()
    company_query = db.query('select name from company').namedresult()
    customize_main_cat = request.form.get('customize_main_cat')
    customize_second_cat = request.form.get('customize_second_cat')
    customize_product = request.form.get('customize_product')
    customize_company = request.form.get('customize_company')
    return render_template(
        '/product_review.html',
        customize_main_cat=customize_main_cat,
        customize_second_cat=customize_second_cat,
        customize_product=customize_product,
        customize_company=customize_company,
        main_cat_list=main_cat_query,
        second_cat_list=second_cat_query,
        product_list=product_query,
        company_list=company_query
    )



# Route and method for adding a new product review
@app.route('/add_product_review', methods=['POST'])
def add_review():
    # Reqests the needed information from the form in /product_review
    main_cat_name = request.form.get('main_cat_name')
    second_cat_name = request.form.get("sec_cat_name")
    product_name = request.form.get('product_name')
    rating = request.form.get('rating')
    review = request.form.get('review')
    company_name = request.form.get('company_name')
    print second_cat_name

    # Checks the input against values in the main_cat table. If the query doesn't find a match, a new entry is added.
    main_cat_check = db.query("select name, id from main_cat where main_cat.name = $1" , main_cat_name).namedresult()
    if main_cat_check:
        main_category_id = main_cat_check[0].id
    else:
        db.insert(
            'main_cat',
            name=main_cat_name,
        )
        main_cat_check = db.query("select name, id from main_cat where main_cat.name = $1" , main_cat_name).namedresult()
        main_category_id = main_cat_check[0].id
    print main_category_id
    # Checks the input against values in the secondary_cat table. If the query doesn't find a match, a new entry is added.
    second_cat_check = db.query("select * from secondary_cat where secondary_cat.name = $1" , second_cat_name).namedresult()
    if second_cat_check:
        second_cat_id = second_cat_check[0].id
    else:
        db.insert(
            'secondary_cat',
            name=second_cat_name,
            main_cat_id=main_category_id
        )
        second_cat_check = db.query("select * from secondary_cat where secondary_cat.name = $1" , second_cat_name).namedresult()
        second_cat_id = second_cat_check[0].id

    # Checks the input against values in the company table. If the query doesn't find a match, a new entry is added.
    company_check = db.query("select * from company where company.name = $1" , company_name).namedresult()
    if company_check:
        comp_id = company_check[0].id
    else:
        db.insert(
            'company',
            name=company_name
        )
        company_check = db.query("select * from company where company.name = $1" , company_name).namedresult()
        comp_id = company_check[0].id

    # Checks the input against values in the product table. If the query doesn't find a match, a new entry is added.
    # Once the entry is added into product table, that product information and the prior secondary_cat.id are added to the product_uses_category table
    product_check = db.query("select * from product where product.name = $1" , product_name).namedresult()
    if product_check:
        prod_id = product_check[0].id
    else:
        db.insert(
            'product',
            name=product_name,
            company_id=comp_id
        )
        product_check = db.query("select product.id from product where product.name = $1" , product_name).namedresult()
        prod_id = product_check[0].id
        db.insert(
            'product_uses_category',
            product_id=prod_id,
            secondary_cat_id=second_cat_id
        )

    # Finally, a new review is created based off of the information from the form that has been filtered and inserted through the database
    if session['username']:
        session_un = session['username']
        userid_query = db.query("select * from users where users.user_name = $1" , session_un).namedresult()
    user_id=userid_query[0].id
    now = datetime.datetime.now()
    db.insert(
        'review',
        product_id=prod_id,
        rating=rating,
        review=review,
        date=now.strftime("%Y-%m-%d"),
        user_id=user_id
    )
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
