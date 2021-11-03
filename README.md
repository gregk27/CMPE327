# CMPE327 - 
![Tests](https://github.com/gregk27/CMPE327/actions/workflows/pytest.yml/badge.svg)
![Linting](https://github.com/gregk27/CMPE327/actions/workflows/style_check.yml/badge.svg)

## Meeting Notes
Notes for the stand-up meetings for A4 and later can be found in `.standups/`

## Code Format

All code in the repository should follow the [PEP8 standard](https://www.python.org/dev/peps/pep-0008/)

Github Actions will validate formatting using [Flake8](https://flake8.pycqa.org/en/latest/index.html#) on push.

## Code Tests

GitHub Actions will validate code by running Pytests for files in `qbay_test/` on push.

## [A0 - Team Contract](https://github.com/CISC-CMPE-327/Information-2021/blob/main/A0-contract.md)
Team formation completed. Team contract signed. [MIT License](https://github.com/gregk27/CMPE327/blob/master/LICENSE) chosen for repository.
The contract can be found here: [https://github.com/gregk27/CMPE327/blob/master/A0-contract.md](https://github.com/gregk27/CMPE327/blob/master/A0-contract.md)

## [A1 - Entities](https://github.com/CISC-CMPE-327/Information-2021/blob/main/A1-entities.md)
Elect Gregory Kelly as Scrum Master. 

Add `A1-entities.py` (renamed to `qbay/models.py` in A2).  
This file includes entities (data base models) for the qBay application. qBay is a similar application to eBay used for C2C online shopping.  
At this point in time, the client did not know what constraints they would like, so the attributes per entity reflect as many as the team could think of. The entities are: User, Product, Sessions, Transaction, and Review.

Testing at this stage is only to pass linting.

## [A2 - Backend](https://github.com/CISC-CMPE-327/Information-2021/blob/main/A2-backend.md)
At this point of time, the client has clarified the entities' requirements and have requested for 4 entities (User, Product, Transactoin, and Review) with specific attributes.

These specifications are included in `qbay/models.py` as functions, specifically for user registration, user login, update user profile, product creation, and update product.  
Tests for these functions are included in `qbay_test/test_models.py` (renamed to `qbay_test/test_backend.py`).

Testing at this stage includes passing the linting and pytests.

## [A3 - Front end](https://github.com/CISC-CMPE-327/Information-2021/blob/main/A3-Frontend.md)
The team has decided to create a web interface for the front end.

Split `qbay/models.py` to `qbay/models.py` (only contains the entities) and `qbay/backend.py` (only contains the functions)

Add `qbay/templates/` (provided front end code; additional pages created) and `qbay/controllers.py` (HTTP routes interface).  
The pages for the front end include: user login, user registration, user profile update, user home page, product creation, and product update.

Testing for this stage includes passing the linting and front end runs without error.