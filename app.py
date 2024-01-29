import os
#from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue

#from models import Restaurant, Review, Thanks
from models import Thanks

from datetime import date
from dateutil.relativedelta import relativedelta

@app.route('/test', methods=['GET'])
def test():    
    return "this is test API which can return any data from database of get data to save in database"

#Save user thank
@app.route('/thanks', methods=['POST'])
def addThank(): 
    #Get input data from request      
    thank = Thanks()
    thank.createUser = request.values.get('create_user')
    thank.userFor = request.values.get('user_for')
    thank.thanksText = request.values.get('thanks_text')
    thank.createDate = date.today()
    db.session.add(thank)
    db.session.commit()
    return "thanks saved"


#Get all user thanks
@app.route('/thanks/<string:userid>', methods=['GET'])
def getThanksByUserId(userid):     
    userThanks = Thanks.query.where(Thanks.userFor == userid)
    return userThanks


#Get all user thanks
@app.route('/thanks/count/<string:userid>', methods=['GET'])
def getThanksCntByUserId(userid): 
   
    dateOneMonthBefore = date.today() - relativedelta(month=-1)
    dateOneYearBefore = date.today() - relativedelta(year=-1)

    allUsersThanks = userThanksTotalCnt = Thanks.query.where(Thanks.userFor == userid).count()
    monthUsersThanks = userThanksTotalCnt = Thanks.query.where(Thanks.userFor == userid).where(Thanks.createDate <= dateOneMonthBefore).count()
    yearUsersThanks = userThanksTotalCnt = Thanks.query.where(Thanks.userFor == userid).where(Thanks.createDate <=  dateOneYearBefore).count()

    thanksCnts = [monthUsersThanks, yearUsersThanks, allUsersThanks] 

    return thanksCnts

@app.route('/', methods=['GET'])
def index():
    # print('Request for index page received')
    # restaurants = Restaurant.query.all()
    # return render_template('index.html', restaurants=restaurants)
    return "API for UZMTO portal"


# @app.route('/<int:id>', methods=['GET'])
# def details(id):
#     restaurant = Restaurant.query.where(Restaurant.id == id).first()
#     reviews = Review.query.where(Review.restaurant == id)
#     return render_template('details.html', restaurant=restaurant, reviews=reviews)

# @app.route('/create', methods=['GET'])
# def create_restaurant():
#     print('Request for add restaurant page received')
#     return render_template('create_restaurant.html')

# @app.route('/add', methods=['POST'])
# @csrf.exempt
# def add_restaurant():
#     try:
#         name = request.values.get('restaurant_name')
#         street_address = request.values.get('street_address')
#         description = request.values.get('description')
#     except (KeyError):
#         # Redisplay the question voting form.
#         return render_template('add_restaurant.html', {
#             'error_message': "You must include a restaurant name, address, and description",
#         })
#     else:
#         restaurant = Restaurant()
#         restaurant.name = name
#         restaurant.street_address = street_address
#         restaurant.description = description
#         db.session.add(restaurant)
#         db.session.commit()

#         return redirect(url_for('details', id=restaurant.id))

# @app.route('/review/<int:id>', methods=['POST'])
# @csrf.exempt
# def add_review(id):
#     try:
#         user_name = request.values.get('user_name')
#         rating = request.values.get('rating')
#         review_text = request.values.get('review_text')
#     except (KeyError):
#         #Redisplay the question voting form.
#         return render_template('add_review.html', {
#             'error_message': "Error adding review",
#         })
#     else:
#         review = Review()
#         review.restaurant = id
#         review.review_date = datetime.now()
#         review.user_name = user_name
#         review.rating = int(rating)
#         review.review_text = review_text
#         db.session.add(review)
#         db.session.commit()

#     return redirect(url_for('details', id=id))

# @app.context_processor
# def utility_processor():
#     def star_rating(id):
#         reviews = Review.query.where(Review.restaurant == id)

#         ratings = []
#         review_count = 0
#         for review in reviews:
#             ratings += [review.rating]
#             review_count += 1

#         avg_rating = sum(ratings) / len(ratings) if ratings else 0
#         stars_percent = round((avg_rating / 5.0) * 100) if review_count > 0 else 0
#         return {'avg_rating': avg_rating, 'review_count': review_count, 'stars_percent': stars_percent}

#     return dict(star_rating=star_rating)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
