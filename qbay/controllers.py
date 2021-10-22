from flask import render_template, request, session, redirect
from qbay.models import User, Product
from qbay.backend import login, register, updateProduct, updateUser


from qbay import app

app.secret_key = 'KEY'


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner(*args, **kwargs):
        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user, *args, **kwargs)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    wrapped_inner.__name__ = inner_function.__name__
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # some fake product data
    products = [
        {'name': 'prodcut 1', 'price': 10},
        {'name': 'prodcut 2', 'price': 20}
    ]
    return render_template('index.html', user=user, products=products)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/update/<prodName>', methods=['GET'])
@authenticate
def update_get(user, prodName):
    # Get product by name and user
    product = Product.query.filter_by(productName=prodName, userId=user.id)\
                .one_or_none()
    # If product can't be found, display error
    if(product is None):
        return render_template("error.html", message="Product " + {prodName} +
                               " not found in your products")
    # If product can be found, display update page
    return render_template("product/update.html", message="", product=product)


@app.route('/update/<prodName>', methods=['POST'])
@authenticate
def update_post(user, prodName):
    # Get product by name and user
    product = Product.query.filter_by(productName=prodName, userId=user.id)\
                .one_or_none()
    # If product can't be found, display error
    if(product is None):
        return render_template("error.html", message="Product " + {prodName} +
                               " not found in your products")

    # Get inputs from request body
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('desc')

    # Convert price to float, if not possible then error
    try:
        price = float(price)
    except ValueError:
        return render_template("product/update.html",
                               message="Price should be a number",
                               product=product)
    message = ""
    # updateProduct will return true on success, and throw ValueError with
    #   message if inputs are invalid
    try:
        if(updateProduct(product.id, productName=name, price=price,
                         description=description)):
            #  Redirect since product name may have changed
            return redirect(f"/update/{product.productName}")
        message = "Unkown error occured"
    except Exception as err:
        message = err

    # Display page with error message on failure
    return render_template("product/update.html", message=message,
                           product=product)


@app.route('/update/<username>', methods=['GET'])
@authenticate
def update_get_user(user, username):
    # Get user by userID
    user = User.query.filter_by(userID=user.id).one_or_none()

    # If user cannot be found, display error
    if(user is None):
        return render_template("error.html", message="User " + {username} +
                               " not found in database")
    # If user can be found, display update page
    return render_template("user/update.html", message="", user=user)


@app.route('/update/<username>', methods=['POST'])
@authenticate
def update_post_user(user, username):
    # Get user by userID
    user = User.query.filter_by(userID=user.id).one_or_none()
    # If user cannot be found, display error
    if(user is None):
        return render_template("error.html", message="User " + {username} +
                               " not found in database")

    # Get inputs from request body
    username = request.form.get('username')
    shippingAddress = request.form.get('shippingAddress')
    postalCode = request.form.get('postalCode')

    # updateUser will return true on success
    try:
        if(updateUser(user.id, username=username,
                      shippingAddress=shippingAddress,
                      qpostalCode=postalCode)):
            return redirect(f"/update/{user.username}")
        message = "Unknown error occured"
    except Exception as err:
        message = err

    # Display page with error message on failure
    return render_template("user/update.html", message=message, user=user)
