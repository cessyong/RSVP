from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from flask import flash
import database as db
import authentication
import logging
import pymongo
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', page="Privacy")

@app.route('/services')
def services():
    service_list = db.get_services()
    return render_template('services.html', page="Services",service_list=service_list)



# VENUE
@app.route('/VENUES')
def venue():
    venue_list = db.get_venues()
    return render_template('venue.html', page="Venue",venue_list=venue_list)

# CATERING
@app.route('/CATERING')
def catering():
    caterer_list = db.get_caterers()
    return render_template('catering.html', page="Catering",caterer_list=caterer_list)

# DOCU
@app.route('/DOCUMENTATION')
def docu():
    docu_list = db.get_docus()
    return render_template('docu.html', page="Documentation",docu_list=docu_list)



# VENUES
@app.route('/venuedetails')
def venuedetails():
    code = request.args.get('code', '')
    venue = db.get_venue(int(code))
    return render_template('venuedetails.html', code=code,venue=venue)

# CATERING
@app.route('/cateringdetails')
def cateringdetails():
    code = request.args.get('code', '')
    caterer = db.get_caterer(int(code))
    return render_template('cateringdetails.html', code=code,caterer=caterer)

# DOCUS
@app.route('/documentationdetails')
def documentationdetails():
    code = request.args.get('code', '')
    docu = db.get_docu(int(code))
    return render_template('documentationdetails.html', code=code,docu=docu)



@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")


@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html', page="My Account")


@app.route('/login' , methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    
    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        flash("Invalid username or password. Please try again.")
        return  render_template('login.html')


# REMOVE SESSION POP CART
@app.route('/logout')
def logout():
    session.pop("user",None)
    return redirect('/')


# CHANGE TO FAVORITES HAHU
@app.route('/favorites')
def favorites():
    return render_template('cart.html')

@app.route('/addtofaves', methods = ['POST', ])
def addtofaves():
    code = request.form.get('code')
    company = db.get_company(int(code))
    item=dict()
# A click to add a product translates to a quantity of 1 for now
    item["code"] = company["code"]
    item["name"] = company["name"]
    item["prices"] = company["prices"]
    item["services"] = company["services"]
    item["image"] = company["image"]
    
    
    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/favorites')

# HIDE UPDATE
@app.route('/updatefaves', methods = ['POST', ])
def updatefaves():
    request_type = request.form.get('submit')
    code = request.form.get('code')
    company = db.get_company(int(code))
    cart = session["cart"]
    
    #Update quantity of item in cart
    if request_type == "Update":
        quantity = int(request.form.get("quantity"))
        cart[code]["qty"] = quantity
        cart[code]["subtotal"] = quantity * product["price"]
        
    elif request_type == 'Remove':
        del cart[code]
        
    session["cart"] = cart
    
    return redirect('/favorites')

    
@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/change', methods = ['GET', 'POST'])
def change():
    oldpass = request.form.get("old")
    newpass1 = request.form.get("new1")
    newpass2 = request.form.get("new2")
    user = session["user"]
    username = user["username"]
    userpass = user["password"]

    if oldpass == userpass and newpass1 == newpass2:
        change_now = db.change_db(username, newpass1)
        change_error = "Password successfully changed."
        return render_template('changepassword.html', change_error=change_error)
    
    elif oldpass != userpass:
        change_error = "The current password is incorrect."
        return render_template('changepassword.html', change_error=change_error)
    
    else:
        change_error = "The passwords entered do not match."
        return  render_template('changepassword.html', change_error=change_error)