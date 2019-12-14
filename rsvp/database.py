import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

services_db = myclient["services"]

companies_db = myclient["companies"]

allcompanies_db = myclient["allcompanies"]

order_management_db = myclient["order_management"]


# COMPANIES
def get_company(code):
    allcompanies_coll = allcompanies_db["allcompanies"]
    
    company = allcompanies_coll.find_one({"code":code})
    
    return company

def get_companies():
    company_list = []
    
    allcompanies_coll = allcompanies_db["allcompanies"]
    
    for a in allcompanies_coll.find({}):
        company_list.append(a)
        
    return company_list


# VENUES
def get_venue(code):
    venues_coll = companies_db["venues"]
    
    venue = venues_coll.find_one({"code":code})
    
    return venue

def get_venues():
    venue_list = []
    
    venues_coll = companies_db["venues"]
    
    for v in venues_coll.find({}):
        venue_list.append(v)
        
    return venue_list

# CATERING
def get_caterer(code):
    catering_coll = companies_db["catering"]
    
    caterer = catering_coll.find_one({"code":code})
    
    return caterer

def get_caterers():
    caterer_list = []
    
    catering_coll = companies_db["catering"]
    
    for c in catering_coll.find({}):
        caterer_list.append(c)
        
    return caterer_list

# DOCU
def get_docu(code):
    docus_coll = companies_db["docus"]
    
    docu = docus_coll.find_one({"code":code})
    
    return docu

def get_docus():
    docu_list = []
    
    docus_coll = companies_db["docus"]
    
    for d in docus_coll.find({}):
        docu_list.append(d)
        
    return docu_list



# SERVICES
def get_service(id):
    services_coll = services_db["services"]
    
    service = services_coll.find_one({"serviceid":serviceid})
    
    return service

def get_services():
    service_list = []
    
    services_coll = services_db["services"]
    
    for s in services_coll.find({}):
        service_list.append(s)
        
    return service_list


def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user


def change_db(username, new1):
    pw_coll = order_management_db['customers']
    customer = {"username":username}
    changepw = {"$set": {"password":new1}}
    pw_coll.find_one_and_update(customer, changepw)