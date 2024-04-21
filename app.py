from __future__ import print_function
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify , session
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
fname = quote_plus('dbadmin')
password = quote_plus('dbImp!14@2')
url = 'mongodb://%s:%s@172.18.17.236:27017/' % (fname, password) #172.18.17.236 #78.38.35.219
client = MongoClient(url)


db = client['400463108']
collection_Users = db['Users']
collection_Products = db['Products_forSale']
collection_Orders = db['Orders']
collection_Reviews = db['ProductReviews']
@app.route('/')
def index():
    return render_template("signUp.html")


@app.route('/signup', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        email = request.form.get('Email')
        Store_address = request.form.get('Store_address')
        name = str(first_name) + " " + str(last_name)
        # print(first_name, last_name)
        new_user = {
            "Name": name,
            "Username": username,
            "Password": password,
            "Email": email,
            "Store_address": Store_address,
            "Phone_number": phone_number
        }
        collection_Users.insert_one(new_user)
        return redirect(url_for('index'))
    return render_template('signUp.html')


@app.route('/check-username', methods=['POST'])
def check_username():
    username = request.json.get('username')
    existing_user = collection_Users.find_one({'Username': username})
    return jsonify({'available': existing_user is None})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    pipeline = [
        {
            '$match': {
                'Username': username,
                'Password': password
            }
        },
  		{
            '$project':{
				'_id': 0,
                'Username': 1,
                'Password': 1
            }
        }
    ]
    user = list(collection_Users.aggregate(pipeline))
    if user:
        current_User = str(user[0]['Username'])
        print("user entered :" + current_User)
        session['username'] = current_User
        return jsonify({'message': 'Successful'})
    else:
        return jsonify({'error': 'Invalid username or password'})

@app.route('/loginPage', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('loginPage.html')


@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
    if 'username' in session:
        current_user = session['username']
        return render_template('mainPage.html', username=current_user)
    else:
        return redirect(url_for('login_page'))

@app.route('/product_list', methods=['GET'])
def product_list():
    if request.method == 'GET':
        products = list(collection_Products.find())
        # jaye aggregate ..
        print(session['username'])
    return render_template("productList.html",products=products)

@app.route('/product_page', methods=['POST'])
def product_page():
    if request.method == 'POST':
        print(session['username'])
        id = int(request.form.get('product_id'))
        product_info = collection_Products.find_one({'Product_ID': id})
        print(product_info)
        return render_template("productPage.html", product=product_info)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        Name = request.form.get('Name')
        Categorie = request.form.get('Categorie')
        Color = request.form.get('Color')
        Weight = float(request.form.get('Weight'))
        Additional_description = request.form.get('Additional_description')
        Price = float(request.form.get('Price'))
        Quantity = int(request.form.get(('Quantity')))

        var_max = list(db.Products_forSale.aggregate([
            {
                '$group': {
                    '_id': None,
                    'maxProductID': {'$max': '$Product_ID'}
                }
            }
        ]))
        max_Product_ID = int(var_max[0]['maxProductID'])

        collection_Users.update_one(
            {"Username": session['username']},
            {
                "$push": {
                    "Products_for_sale": {
                        "p_name": Name,
                        "p_categorie": Categorie,
                        "price": Price,
                        "Quantity": Quantity,
                        "Product_ID": max_Product_ID + 1
                    }
                }
            }
        )
        var_name = list(db.Users.aggregate([
            {
                '$match': {
                    'Username': session['username'],
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'Name': 1
                }
            }
        ]))
        userFullname = var_name[0]['Name']
        print(userFullname)

        new_product = {
          "Product_ID": max_Product_ID + 1,
          "Name": Name,
          "Categorie": Categorie,
          "Color": Color,
          "Weight": Weight,
          "Quantity": Quantity,
          "Additional_description": Additional_description,
          "Seller": {
            "s_name": userFullname,
            "s_username": session['username']
          },
          "Price": Price
        }
        collection_Products.insert_one(new_product)

        return redirect(url_for('mainPage'))
    return render_template('addProduct.html')



@app.route('/purchase_product', methods=['POST'])
def purchase_product():
    data = request.get_json()
    product_id = int(data.get('product_id'))
    p_name = data.get('p_name')
    p_categorie = data.get('p_categorie')
    p_color = data.get('p_color')
    p_weight = data.get('p_weight')
    p_price = float(data.get('p_price'))
    p_seller = data.get('p_seller')
    p_points = data.get('p_points')
    p_quantity = int(data.get('p_quantity'))
    Quantity_purchase = int(data.get('Quantity_purchase'))
    final_quantity = p_quantity - Quantity_purchase

    seller_username = list(collection_Users.aggregate([
        {
            "$unwind": "$Products_for_sale"
        },
        {
            "$match": {
                "Products_for_sale.Product_ID": product_id
            }
        },
        {
            "$project": {
                "_id": 0,
                "Username": 1
            }
        }
    ]))

    if Quantity_purchase <= p_quantity:
        if seller_username[0]['Username'] == session['username']:
            return jsonify({'error': 'You Cant Buy from yourSelf !!'})
        else :
            collection_Products.update_one(
                {"Product_ID": product_id},
                {
                    "$set": {
                        "Quantity": final_quantity
                    }
                }
            )
            print("seller username is :")
            print(seller_username)
            collection_Users.update_one(
                {"Username": session['username']},
                {
                    "$push": {
                        "Purchased_products": {
                            "p_name": p_name,
                            "seller_name": p_seller,
                            "seller_id": seller_username[0]['Username'],
                            "Quantity": Quantity_purchase,
                            "total_price": p_price * float(Quantity_purchase),
                            "Product_ID": product_id
                        }
                    }
                }
            )
            collection_Users.update_one(
                {
                    "Username": seller_username[0]['Username'],
                    "Products_for_sale.Product_ID": product_id
                },
                {
                    "$set": {
                        "Products_for_sale.$.Quantity": final_quantity
                    }
                }
            )
            new_order = {
                "User_ID": session['username'],
                "Seller_ID": seller_username[0]['Username'],
                "Product_ID": product_id,
                "Total_price": p_price * float(Quantity_purchase),
                "Quantity_Purchased": Quantity_purchase,
                "Purchase_date": datetime.today(),
            }
            collection_Orders.insert_one(new_order)
            return jsonify({'message': 'Successful'})
    else:
        return jsonify({'error': 'We do not have as many products as you want to buy !!'})


@app.route('/user_panel', methods=['GET','POST'])
def user_panel():
    if request.method == 'GET':
        user_info = list(db.Users.aggregate([
            {
                '$match': {
                    'Username': session['username'],
                }
            }
        ]))
        # jaye aggregate ..
        return render_template("userPanel.html",user_info=user_info)
    else:
        data = request.get_json()
        password = str(data.get('password'))
        Email = str(data.get('Email'))
        phone_number = str(data.get('phone_number'))
        store_address = str(data.get('store_address'))

        collection_Users.update_one(
            {'Username': session['username']},
            {
                '$set': {
                    'Email': Email,
                    'Password': password,
                    'Phone_number': phone_number,
                    'Store_address': store_address
                }
            }
        )
        return redirect(url_for('user_panel'))
    return render_template('userPanel.html')


@app.route('/users_SaleList', methods=['GET'])
def users_SaleList():
    username = session['username']
    user_products_for_sale = list(db.Users.aggregate([
        {'$match': {'Username': username}},
        {'$unwind': '$Products_for_sale'},
        {'$project': {'_id': 0, 'Products_for_sale': 1}},
        {'$limit': 10}
    ]))
    return render_template("users_saleList.html", sales_list=user_products_for_sale , user = session['username'])


@app.route('/user_PurchaseList', methods=['GET'])
def user_PurchaseList():
    username = session['username']
    purchase_list = list(collection_Orders.aggregate([
          {
             "$skip": 0
          },
          {
             "$limit": 10
          },
          {
             "$match": {"User_ID": username}
          },
          {
            "$lookup": {
              "from": "Products_forSale",
              "localField": "Product_ID",
              "foreignField": "Product_ID",
              "as": "product"
            }
          },
          {
            "$unwind": "$product"
          },
          {
            "$lookup": {
              "from": "Users",
              "localField": "User_ID",
              "foreignField": "Username",
              "as": "user"
            }
          },
          {
            "$unwind": "$user"
          },
          {
            "$project": {
              "_id": 0,
              "Product_ID": "$Product_ID",
              "order_time": "$Purchase_date",
              "product_name": "$product.Name",
              "product_categorie": "$product.Categorie",
              "product_color": "$product.Color",
              "seller_name": "$product.Seller.s_name",
              "quantity_ordered": "$Quantity_Purchased",
              "total_price": "$Total_price"
            }
          }
    ]))
    return render_template("user_PurchaseList.html", purchase_list = purchase_list , user = username)


@app.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.get_json()
    product_id = data.get('Product_ID')
    if not product_id:
        return jsonify({"success": False, "message": "Product ID is missing."})
    try:
        collection_Users.update_one(
            {'Username': session['username']},
            {'$pull': {'Products_for_sale': {'Product_ID': int(product_id)}}}
        )
        collection_Products.delete_one({'Product_ID': int(product_id)})
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



@app.route('/show_RatePage', methods=['POST'])
def show_RatePage():
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        session['product_id'] = product_id
        print("this is product Id")
        print(product_id)
        product_info = collection_Products.find_one({"Product_ID": product_id})
        #jaye aggregate
        return render_template('rate_ProductPage.html', product=product_info)


@app.route('/rate_ProductPage', methods=['GET', 'POST'])
def rate_ProductPage():
    if request.method == 'POST':
        product_id = int(request.form.get('product_id'))
        product_name = str(request.form.get('product_name'))
        comment = str(request.form.get('Comment'))
        rate = int(request.form.get('Rate'))
        username = session['username']

        user_info = list(collection_Users.aggregate([
            {"$match": {"Username": username}},
            {"$project": {"_id": 0, "Name": 1}}
        ]))
        name = user_info[0]['Name']

        # Check if user has already commented and rated for this product or not
        product_info = list(collection_Products.aggregate([
            {"$match": {"Product_ID": product_id}},
            {"$unwind": "$Points_and_Comments"},
            {"$match": {"Points_and_Comments.username": username}},
            {"$limit": 1},
            {"$project": {"_id": 1}}
        ]))
        if product_info:
            return jsonify({'error': 'User already commented and rated for this product'})
        else :
            collection_Products.update_one(
                {"Product_ID": product_id},
                {
                    "$push": {"Points_and_Comments": {
                                'username': username,
                                'name': name,
                                'comment': comment,
                                'rate': rate
                                }
                             }
                })
            collection_Reviews.insert_one(
                {
                    'Username': username,
                    'Name': name,
                    'Product_ID': product_id,
                    'Product_name': product_name,
                    'Review_text': comment,
                    'rate': rate,
                    'Review_date': datetime.today()
                }
            )
            return jsonify({'message': 'Review submitted Successfully'})

        return redirect(url_for('rate_ProductPage'))



if __name__ == '__main__':
    app.run()
