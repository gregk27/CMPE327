from flask import render_template, request, session, redirect
from qbay.models import User, Product, Session
from qbay.backend import (login, register, validateEmail,
                          validateUser, validatePswd,
                          createProduct, updateProduct, updateUser)
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
            sessionId = session['logged_in']
            ip = str(request.remote_addr)
            try:
                # Get the sessionId
                sessionObj = Session.query.filter_by(sessionId=sessionId,
                                                     ipAddress=ip
                                                     ).one_or_none()
                # Get the user id associated with the session
                user = User.query.filter_by(id=sessionObj.userId).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user, *args, **kwargs)
            except Exception as e:
                print(e)
                return redirect('/login')
        else:
            # else, redirect to the login page
            return redirect('/login')
    wrapped_inner.__name__ = inner_function.__name__
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST', 'GET'])
def login_form():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = str(request.remote_addr)
    userSession = login(email, password, ip)
    if userSession:
        session['logged_in'] = userSession.sessionId
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
        return render_template('login.html', message="Incorrect "
                                                     "email or password")


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
        {'name': 'product 1', 'description': 'product desc 1', 'price': 10},
        {'name': 'product 2', 'description': 'product desc 2', 'price': 20}
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
            if validateEmail(email) is False:
                error_message = ("Registration Failed. Invalid email or"
                                 " already in use.")
            if validateUser(name) is False:
                error_message = "Registration Failed. Invalid username."
            if validatePswd(password) is False:
                error_message = "Registration Failed. Invalid password."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login', code=302)


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/product/create', methods=['GET'])
@authenticate
def createProduct_get(user):
    # Display create product page
    return render_template('product/create.html', message='')


@app.route('/product/create', methods=['POST'])
@authenticate
def createProduct_post(user):

    # Get inputs from request body
    name = request.form.get('name')
    description = request.form.get('desc')
    price = request.form.get('price')

    # Convert price to float, if not possible then error
    try:
        price = float(price)
    except ValueError:
        return render_template("product/create.html",
                               message="Price should be a number")

    # Error message
    error_message = None

    # createProduct will return true on success, and throw ValueError with
    # message if inputs are invalid
    try:
        if(createProduct(productName=name, price=price,
                         description=description, owner_email=user.email)):
            # Redirect to homepage
            return redirect("/")
        error_message = "Unknown error occurred"
    except Exception as err:
        error_message = err

    # Display page with error message on failure
    return render_template("product/create.html", message=error_message)


@app.route('/product/update/<prodName>', methods=['GET'])
@authenticate
def updateProduct_get(user, prodName):
    # Get product by name and user
    product = Product.query.filter_by(productName=prodName, userId=user.id)\
                .one_or_none()
    # If product can't be found, display error
    if(product is None):
        return render_template("error.html", message="Product " + {prodName} +
                               " not found in your products")
    # If product can be found, display update page
    return render_template("product/update.html", message="", product=product)


@app.route('/product/update/<prodName>', methods=['POST'])
@authenticate
def updateProduct_post(user, prodName):
    # Get product by name and user
    product = Product.query.filter_by(productName=prodName, userId=user.id)\
                .one_or_none()
    # If product can't be found, display error
    if(product is None):
        return render_template("error.html", message="Product " + {prodName} +
                               " not found in your products")

    # Get inputs from request body
    name = request.form.get('name')
    description = request.form.get('desc')
    price = request.form.get('price')

    # Convert price to float, if not possible then error
    try:
        price = float(price)
    except ValueError:
        return render_template("product/update.html",
                               message="Price should be a number",
                               product=product)

    error_message = None

    # updateProduct will return true on success, and throw ValueError with
    # message if inputs are invalid
    try:
        if(updateProduct(product.id, productName=name, price=price,
                         description=description)):
            #  Redirect since product name may have changed
            return redirect(f"/update/{product.productName}")
        error_message = "Unknown error occurred"
    except Exception as err:
        error_message = err

    # Display page with error message on failure
    return render_template("product/update.html", message=error_message,
                           product=product)


@app.route('/user/modify', methods=['GET'])
@authenticate
def update_get_user(user):
    # If user can be found, display update page
    return render_template("user/update.html", message="", user=user)


@app.route('/user/modify', methods=['POST'])
@authenticate
def update_post_user(user):
    # Get inputs from request body
    username = request.form.get('username')
    shippingAddress = request.form.get('shippingAddress')
    postalCode = request.form.get('postalCode')

    # updateUser will return true on success
    try:
        if(updateUser(user.id, username=username,
                      shippingAddress=shippingAddress,
                      postalCode=postalCode)):
            return redirect("/user/modify")
        message = "Unknown error occured"
    except Exception as err:
        message = err

    # Display page with error message on failure
    return render_template("user/update.html", message=message, user=user)
