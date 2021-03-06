from qbay.models import db, User, Product, Session
from validate_email import validate_email
from uuid import uuid4
import datetime as dt
import hashlib
import json
import re


'''
This file defines functions to interface with the data models
'''


def login(email, password, ip):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        A session for the user on the current machine, None if login fails
    '''
    # Validate inputs before proceeding
    if len(email) == 0 \
       or not validate_email(email) \
       or not validatePswd(password):
        return None

    matches = User.query.filter_by(email=email).all()
    user = None
    # Check results for a password match
    for m in matches:
        # Extract salt from string
        salt = m.password.split(":")[0]
        # Hash input with salt and compare to target
        if(m.password == salt + ":"
           + hashlib.sha512((password + salt).encode('utf-8')).hexdigest()):
            user = m
            break
    if user is None:
        return None

    time = dt.datetime.now()
    s = Session(user=user, userId=user.id, ipAddress=ip,
                sessionId=str(uuid4()),
                # Session expires after a year
                expiry=dt.datetime(time.year+1, time.month, time.day))
    db.session.add(s)
    db.session.commit()
    return s


def validatePswd(password):
    '''
    Validatation of password
      Parameters:
        password (string): user password
      Returns:
        True if input password matches all required critera, otherwise False
    '''
    specialChars = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                    '(', ')', '_', '-', '+', '=', '{', '[', '}', ']',
                    '|', '\\', ':', ';', '"', '\'', '<', ',', '>', '.',
                    '?', '/']

    if len(password) < 6:
        print("Password must be at least 6 characters")
        return False

    if not any(char.isupper() for char in password):
        print('Password must contain at least one uppercase letter')
        return False

    if not any(char.islower() for char in password):
        print('Password must contain at least one lowercase letter')
        return False

    if not any(char in specialChars for char in password):
        print('Password must contain at least one special character')
        return False

    return True


def validateUser(username):
    '''
    Validatation of username
      Parameters:
        username (string): user name
      Returns:
        True if input username matches all required critera, otherwise False
    '''
    if len(username) < 3:
        print("Username must be at least 3 character")
        return False

    if len(username) > 20:
        print("Username exceeded characters. Maximum allowed is 20.")
        return False

    # Username must be alphamerical, whitepsace in prefix or suffix not allowed
    if (not username.replace(" ", "").isalnum() or username[0] == " "
            or username[-1] == " "):
        return False

    return True


def validateEmail(email):
    '''
    Validatation of email
      Parameters:
        email (string): user email
      Returns:
        True if input email follows addr-spec defined in RFC 5322 and if email
        is unique, otherwise False
    '''
    if len(email) == 0:
        return False

    if not validate_email(email):
        return False

    # check email exists in database
    exists = User.query.filter_by(email=email).all()
    if len(exists) > 0:
        return False

    return True


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    if validateEmail(email) and validateUser(name) and validatePswd(password):
        # create a new user
        salt = uuid4()
        # Generate string from salt and hashed password
        hashed = str(salt) + ":" + hashlib.sha512((password + str(salt))
                                                  .encode('utf-8')).hexdigest()
        user = User(id=str(uuid4()), username=name, email=email,
                    password=hashed, balance=100, shippingAddress="",
                    postalCode="")
        # add it to the current database session
        db.session.add(user)
        # actually save the user object
        db.session.commit()
        return True

    return False


def queryUser(email, attribute, value):
    '''
    Check if specified user attribute matches expected value
      Parameters:
        email (string):     user email
        attribute (string)  user dbColumn
        value (string)      user attribute value
      Return: True if query matches value
    '''
    user = User.query.filter_by(email=email).all()
    # stringify user object
    temp = str(user[0])
    # create JSON object
    access = json.loads(temp)
    if access[attribute] == value:
        return True

    return False


def validateProductParameters(productName, description, price,
                              last_modified_date, owner_email,
                              ignoreEmail=False, exceptions=False):
    """
    Create a Product
      Parameters:
        productName (string):           product name
        description (string):           product description
        price (float):                  product price
        last_modified_date (DateTime):  product object last modified date
        owner_email:                    product owner's email
        ignoreEmail:                    flag to bypass email check,
                                            for updateProduct
        exceptions:                    flag for if exceptions should be raised

      Returns:
        True if product parameters are vaild, otherwise False
    """
    # If the title without spaces is not alphanumeric-only,
    # or begins or ends in a space
    # or is longer than 80 chars, return False
    if (not productName.replace(" ", "").isalnum() or
            productName[0] == " " or
            productName[-1] == " " or
            len(productName) > 80):
        if(exceptions):
            raise ValueError(f"Invalid name {productName}")
        return False

    # If description is less than 20 or greater than 20
    # or length of description is less than or equal to length of title,
    # return False
    if ((len(description) < 20 or len(description) > 2000) or
            len(description) <= len(productName)):
        if(exceptions):
            raise ValueError("Invalid description length")
        return False

    # Check acceptable price range [10, 10000]
    if (price < 10.0 or price > 10000.0):
        if(exceptions):
            raise ValueError(f"Invalid price {price}")
        return False

    # Check acceptable last_modified_date range
    if (last_modified_date <= dt.datetime(2021, 1, 2) or
            last_modified_date >= dt.datetime(2025, 1, 2)):
        if(exceptions):
            raise ValueError("Invalid last modified date "
                             + str(last_modified_date))
        return False

    # Check if owner email is null
    if (owner_email == "" or owner_email is None):
        if(exceptions):
            raise ValueError(f"Invalid owner email {owner_email}")
        return False

    # Check if owner of the corresponding product exists
    owner = User.query.filter_by(email=owner_email).all()
    if (len(owner) == 0 and not ignoreEmail):
        if(exceptions):
            raise ValueError(f"Owner does not exist {owner_email}")
        return False

    # Check if user has already used this title
    userProducts = Product.query.filter_by(ownerEmail=owner_email,
                                           productName=productName).all()
    print(userProducts)
    if (len(userProducts) >= 1):
        if(exceptions):
            raise ValueError(f"User already has product {productName}")
        return False

    return True


def createProduct(productName, description, price, owner_email,
                  last_modified_date=dt.datetime.now()):
    """
    Create a Product
      Parameters:
        productName (string):           product name
        description (string):           product description
        price (float):                  product price
        last_modified_date (DateTime):  product object last modified date
        owner_email:                    product owner's email
      Returns:
        True if product creation succeeded, otherwise False
    """
    if(not validateProductParameters(productName, description, price,
                                     last_modified_date, owner_email,
                                     False, True)):
        return False

    # Get the owner to obtain their id
    owner = User.query.filter_by(email=owner_email).first()

    # Create a new product
    product = Product(id=str(uuid4()),
                      productName=productName,
                      description=description,
                      price=price,
                      lastModifiedDate=last_modified_date,
                      userId=owner.id,
                      ownerEmail=owner_email
                      )

    # Add it to the current database session
    db.session.add(product)

    # Save the product object
    db.session.commit()

    return True


def updateProduct(productId, **kwargs):
    '''
    Update an existing product
      Parameters:
        productId (string): ID of the product being updated
        any named parameters corresponding to properties of Product model
      returns:
        True on update success, False on failure
    '''
    product = Product.query.filter_by(id=productId).first()
    if product is None:
        return False

    # If the product name is unchanged, then make sure the owner email is
    # not in database so duplicate check passes
    owner_email = product.user.email
    if('productName' in kwargs
       and kwargs['productName'] == product.productName):
        owner_email = "invalid"

    # Check that parameters are valid, use defaults which are when not provided
    if not validateProductParameters(
        productName=kwargs.get('productName', product.productName),
        description=kwargs.get('description', product.description),
        price=kwargs.get('price', product.price),
        last_modified_date=kwargs.get('lastModifiedDate', dt.datetime.now()),
        owner_email=owner_email,  # Need email for duplicate checking
        ignoreEmail=True,  # Email cannot be changed so don't validate it
        exceptions=True  # Throw exceptions for frontend error message
    ):
        return False

    # Update price if it's higher
    if 'price' in kwargs:
        if(kwargs['price'] > product.price):
            product.price = kwargs['price']
        kwargs.pop('price')

    # Update name if it's alphanumeric and under 80 chars
    if 'productName' in kwargs:
        # TODO: Take name validation from creation function
        product.productName = kwargs['productName']
        kwargs.pop('productName')

    # Update description if it's within size limits
    if 'description' in kwargs:
        desc = kwargs['description']
        if(len(desc) >= 20 and len(desc) <= 2000
           and len(desc) > len(product.productName)):
            product.description = desc
        kwargs.pop('description')

    # Check price is in range
    if 'price' in kwargs:
        price = kwargs['price']
        if(price >= 10 and price <= 10000):
            product.price = price
        kwargs.pop('price')

    # Assign remaining properties directly
    for key, val in kwargs.items():
        # Some properties cannot be chagned
        if key == 'userId' or key == 'ownerEmail' \
          or key == 'lastModifiedDate' or key == "id":
            continue
        # If there's no special condition, just update directly
        elif key in kwargs:
            setattr(product, key, val)

    product.lastModifiedDate = dt.datetime.now()
    db.session.commit()
    return True


def validateShippingAddress(shippingAddress, strictCapitalization=False):
    """
    Validation of shippingAddress
      Parameters:
        shippingAddress (string): user shipping address
      returns:
        True on validation success, False on failure
    """
    #  Check if shipping address is empty
    if len(shippingAddress) == 0:
        return False

    # Check if shipping address is alphanumeric
    if not shippingAddress.replace(" ", "").isalnum():
        return False

    return True


def validatePostalCode(postalCode):
    """
    Validation of postalCode
      Parameters:
        postalCode (string): user postal code
      returns:
        True on validation success, False on failure
    """
    # If the format does not match a standard Canadian postal code
    # Regex doesn't like being broken, so line exceeds 80 character limit
    if not re.match(r"[ABCEGHJKLMNPRSTVXY][0-9]+[ABCEGHJKLMNPRSTVWXYZ[0-9]+[ABCEGHJKLMNPRSTVWXYZ][0-9]+", postalCode): # NOQA
        return False

    return True


def updateUser(userID, **kwargs):
    """
    Update an existing user
        Parameter:
            userId (string): ID of the user being updated
            any named parameters corresponding to properties of User model
        Returns:
            True if update is a success, otherwise False
    """
    userUpdate = User.query.filter_by(id=userID).first()
    if userUpdate is None:
        return False

    username = kwargs.get('username', userUpdate.username)
    # Check if username has been used before
    usernameUnique = User.query.filter(User.username == username)\
                               .filter(User.id != userID).all()
    print(usernameUnique)

    if 'username' in kwargs:
        # Check if username is valid
        if validateUser(username) and len(usernameUnique) < 1:
            # Update username if valid
            userUpdate.username = kwargs['username']
        else:
            raise ValueError("Invalid Username")
        kwargs.pop('username')

    shippingAddress = kwargs.get('shippingAddress',
                                 userUpdate.shippingAddress)

    if 'shippingAddress' in kwargs:
        # Check if ShippingAddress is valid
        if validateShippingAddress(shippingAddress):
            # Update Shipping Address
            userUpdate.shippingAddress = kwargs['shippingAddress']
        else:
            raise ValueError("Invalid shipping address")
        kwargs.pop('shippingAddress')

    postalCode = kwargs.get('postalCode', userUpdate.postalCode)

    if 'postalCode' in kwargs:
        # Check if postalCode is a valid Canadian postal code
        if validatePostalCode(postalCode):
            # Update postalCode
            userUpdate.postalCode = kwargs['postalCode']
        else:
            raise ValueError("Invalid postal code")
        kwargs.pop('postalCode')

    db.session.commit()
    return True


def purchaseProduct(userID, productID):
    """
    Have a user purchase a product
    If the user has sufficient funds, they will be transferred to the product's
    owner, and the product will be marked as sold
        Parameter:
            userID: ID of user buying the product
            productId: ID of the product being sold
        Returns:
            Nothing
        Throws:
            ValueError with error message on failure
    """
    # Get the user and product
    user = User.query.filter_by(id=userID).first()
    product = Product.query.filter_by(id=productID).first()

    # Make sure the user isn't buying their own product
    if(user.id == product.user.id):
        raise ValueError("You cannot buy your own products")

    # Check that the user can afford the product
    if(user.balance < product.price):
        raise ValueError("You cannot afford the product")

    # Transfer funds and mark as sold
    product.user.balance += product.price
    product.buyer = user
    product.buyerId = user.id
    user.balance -= product.price
    product.sold = True
    db.session.commit()
    return True
