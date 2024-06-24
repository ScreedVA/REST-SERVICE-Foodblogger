# Food Blogger 😋 - Python Rest Service Blog Application
> Backend application built with the Flask framework

## Table of Contents
- Introduction
- Features
- Installation
- Usage
- Contact Info
- Dependencies

## Introduction
The Python Rest Service utilizes Flask decorators to initialize routes for api end points through out the application, linking api routes and json based data. 

## Features
- GET methods for full data of a particular category
- GET methods which retrive specific data based on some criteria
- POST methods for creating users and blog posts
- PUT methods for editing users and blog posts
- DELETE methods for images, users and posts

## Installation

Clone repository
```bash (In Terminal)
git clone https://github.com/ScreedVA/REST-SERVICE-Foodblogger.git
```

Move into repository directory
```bash (In Terminal)
cd REST-SERVICE-Foodblogger
```

Create virtual environement
```bash (In Terminal)
python -m venv .venv
```

Activate virtual environemnt
```bash (In Terminal)
.venv\Scripts\activate
```

Install pip if nessasary
```bash (In Terminal)
python -m pip install --upgrade pip
```

Install project dependencies
```bash (In Terminal)
pip install -r requirements.txt
```

## Usage
Simply run the application and open [localhost:5000](http://127.0.0.1:5000) on your browser
```bash (In Terminal)
python main.py
```

To perform the unit test for this application simply run
```bash (In Terminal)
python unit_test_create_post.py
```


## Contact Info
[LinkedIn Profile](https://www.linkedin.com/in/christian-damete-yeboa-bb79442a3/)

## Dependancies
```bash
alembic==1.13.1
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
greenlet==3.0.3
iniconfig==2.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
Mako==1.3.3
MarkupSafe==2.1.5
packaging==24.1
pluggy==1.5.0
pytest==8.2.2
SQLAlchemy==2.0.30
typing_extensions==4.11.0
Werkzeug==3.0.3
```

## References
> This application uses prototyping example data for posts inpired from food forums online, are from the following citations, (in-text citations included in data output for posts)

Ma, N., Geary-Meyer, A., & Bettes, K. (2024, April 2). 25 best restaurants in Berlin, by local foodies. Time Out Berlin. https://www.timeout.com/berlin/restaurants/best-restaurants-in-berlin 
Qween City. (2019, August 11). Food Review: All of the desserts! https://qweencity.com/food-review-all-of-the-desserts/ 
The 15 best places for breakfast food in Berlin. Foursquare. (n.d.). https://foursquare.com/top-places/berlin/best-places-breakfast-food 


