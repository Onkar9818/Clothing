from flask import Flask, make_response, redirect,render_template, request, session,url_for,flash, jsonify
from mysql.connector import MySQLConnection
from flask_bcrypt import Bcrypt
import json
from urllib.parse import quote
import locale
import uuid

app=Flask(__name__)
bcrypt = Bcrypt(app)
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

config = {
	"host": "localhost",
	"user": "root",
	"password": "",
	"port": 3307,
	"database": "clothing_store",
	"charset": "utf8mb4",
	"collation": "utf8mb4_unicode_ci"
}

cnx=MySQLConnection(**config)
app.secret_key='Cloth'
app.jinja_env.filters['urlquote'] = lambda u: quote(str(u)) if u else ''
app.jinja_env.filters['currency_format'] = lambda v: locale.currency(v, grouping=True) if v else ''

@app.context_processor
def inject_cart_and_user():
	cursor = cnx.cursor(buffered=True, dictionary=True)
	query = "SELECT id,title FROM tbl_categories"
	cursor.execute(query)
	categories = cursor.fetchall()
	cursor.close()
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
		user = session['user']
		params = (user['id'],)
		cursor.execute(query, params)
		cartData = cursor.fetchone()
		cursor.close()
		if cartData != None:
			data = len(json.loads(cartData['product_info']))
		else:
			data = 0
		return dict(categories = categories, cartCount = data, user = user)
	else:
		return dict(categories = categories)

@app.route('/', methods=['GET'])
def home():
	cursor = cnx.cursor(dictionary=True)
	query = "SELECT p.id, p.name as title, p.thumbnail, COUNT(DISTINCT s.size) as variants, s.price FROM tbl_products p RIGHT JOIN tbl_specifications s ON s.pid = p.id GROUP BY p.name"
	cursor.execute(query)
	products = cursor.fetchall()
	return render_template('home.html', products = products)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		if request.form.get('email') != None and request.form.get('password'):
			cursor = cnx.cursor(dictionary=True)
			email = request.form.get("email")
			password = request.form.get("password")
			query = "SELECT secret, id, CONCAT(fname, ' ', lname) as name FROM tbl_users WHERE email = %s"
			params = (email,)
			cursor.execute(query, params)
			data = cursor.fetchone()
			if bcrypt.check_password_hash(data['secret'], password):
				session['user'] = dict(email = email, id = data['id'], name = data['name'])
				return jsonify({'status': True})
			else:
				return jsonify({'status': False, 'message': 'Invalid credentials'})
		else:
				return jsonify({'status': False, 'message': 'Invalid data'})
	else:
		if session.get('user'):
			return redirect('/shop')
		else:
			return render_template('login.html')
		
@app.route('/sign-up', methods=['GET'])
def sign_up():
	if session.get('user'):
		return redirect('/profile')
	else:
		return render_template('signup.html')
	
@app.route('/register', methods=['POST'])
def register():
	if session.get('user'):
		return jsonify({'status': True, 'message': "Invalid operation."})
	else:
		firstName=request.form.get("first-name")
		lastName=request.form.get("last-name")
		email=request.form.get("email")
		password=request.form.get("password")
		confirmPassword=request.form.get("confirm-password")

		if firstName != None and firstName.strip() != '' and lastName != None and lastName.strip() != '' and email != None and email.strip() != '' and password != None and password.strip() != '' and confirmPassword != None and confirmPassword.strip() != '':
			if password == confirmPassword:
				cursor=cnx.cursor(dictionary=True)
				query = "SELECT COUNT(id) as count FROM tbl_users WHERE email = %s"
				params = (email,)
				cursor.execute(query, params)
				data = cursor.fetchone()
				if data != None:
					if int(data['count']) > 0:
						return jsonify({'status': False, 'message': "User already exists with this email address."})
				hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
				cursor=cnx.cursor(dictionary=True)
				query="INSERT INTO tbl_users (fname,lname,email,secret) VALUES (%s,%s,%s,%s)"
				val=(firstName,lastName,email,hashed_password)
				cursor.execute(query,val)
				cnx.commit()
				affected_rows = cursor.rowcount
				cursor.close()
				if affected_rows > 0:
					cursor=cnx.cursor(dictionary=True)
					query = "SELECT id, CONCAT(fname, ' ', lname) as name FROM tbl_users WHERE email = %s"
					params = (email,)
					cursor.execute(query, params)
					data = cursor.fetchone()
					session['user'] = dict(email = email, id = data['id'], name = data['name'])
				return jsonify({'status': True if affected_rows > 0 else False, 'message': "Registration successful" if affected_rows > 0 else "Failed to register."})
			else:
				return jsonify({'status': False, 'message': "Password do not match"})
		else:
			return jsonify({'status': False, 'message': "Invalid request."})
		
@app.route('/profile', methods=['GET'])
def profile():
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("SELECT COUNT(id) as addressCount from tbl_addresses WHERE user_id = %s", (session['user']['id'], ))
		addressCount = cursor.fetchone()['addressCount']
		cursor.close()
		user = {'name': session['user']['name'], 'email': session['user']['email']}
		addressCount = int(addressCount)
		if addressCount > 0:
			cursor = cnx.cursor(dictionary=True)
			cursor.execute("SELECT * from tbl_addresses WHERE user_id = %s", (session['user']['id'], ))
			addresses = cursor.fetchall()
			cursor.close()
			return render_template('profile.html', user = user, addressCount = addressCount, addresses= addresses)
		return render_template('profile.html', user = user, addressCount = addressCount)
	else:
		return redirect('/login')

@app.route('/add-address', methods=['POST'])
def add_address():
	if session.get('user'):
		title = request.form['address_title']
		full = request.form['address_full']
		city = request.form['address_city']
		state = request.form['address_state']
		pincode = request.form['address_pincode']
		contact = request.form['address_contact']
		if title.strip() != '' and full.strip() != '' and city.strip() != '' and state.strip() != '' and pincode.strip() != '' and contact.strip() != '':
			cursor = cnx.cursor(dictionary=True, buffered=True)
			query = "INSERT INTO tbl_addresses (title, full, city, state, pincode, contact, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			params = (title, full, city, state, pincode, contact, session['user']['id'])
			cursor.execute(query, params)
			cnx.commit()
			count = cursor.rowcount
			cursor.close()
			return jsonify({"status": True if count > 0 else False, "message": "Address added." if count > 0 else "Failed to add address."})
	else:
		return make_response(jsonify({"status": False, "message": "You must be logged in."})), 401

@app.route('/shop', methods=['GET'])
def shop():
	category = request.args.get('category')
	cursor = cnx.cursor(dictionary=True)
	if category != None and str(category).strip() != '':
		category = int(category)
		query = "SELECT p.id, p.name as title, p.thumbnail, COUNT(DISTINCT s.size) as variants, s.price FROM tbl_products p RIGHT JOIN tbl_specifications s ON s.pid = p.id WHERE category = %s GROUP BY p.name"
		cursor.execute(query, (category, ))
	else:
		query = "SELECT p.id, p.name as title, p.thumbnail, COUNT(DISTINCT s.size) as variants, s.price FROM tbl_products p RIGHT JOIN tbl_specifications s ON s.pid = p.id GROUP BY p.name"
		cursor.execute(query)
	products = cursor.fetchall()
	cursor.close()
	return render_template('shop.html', products = products)

@app.route('/product/<int:product_id>', methods=['GET'])
def product(product_id):
	cursor = cnx.cursor(dictionary=True)
	query = "SELECT id, name as title, description, thumbnail FROM tbl_products WHERE id = %s"
	cursor.execute(query, (product_id, ))
	product = cursor.fetchone()
	cursor.close()
	if len(product) > 0:
		colors = [{"name": "Blue", "value": "blue"},{"name": "Black", "value": "black"},{"name": "Brown", "value": "brown"},{"name": "Red", "value": "red"}]
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT id, size FROM tbl_specifications WHERE pid = %s"
		cursor.execute(query, (product_id, ))
		variants = cursor.fetchall()
		return render_template('product.html', product = product, variants = variants, colors = colors)
	
@app.route('/get-product-price', methods =['POST'])
def get_product_price():
	spec = request.form.get('spec-id')
	if spec != None and spec.strip() != '':
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT quantity, price FROM tbl_specifications WHERE id = %s"
		cursor.execute(query, (spec, ))
		variant = cursor.fetchone()
		if variant != None:
			return jsonify({"status": True, "qnt": variant['quantity'], "amt": locale.currency(variant['price'], grouping=True)})
		else:
			return jsonify({"status": False, "message": "Product variant unavailable"})
	else:
		return jsonify({"status": False, "message": "Invalid request"})

@app.route('/cart', methods=['GET'])
def cart():
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
		params = (session['user']['id'],)
		cursor.execute(query, params)
		data = cursor.fetchone()
		if data != None:
			product_info = json.loads(data['product_info'])
			cursor.close()
			if len(product_info) > 0:
				cursor = cnx.cursor(dictionary=True, buffered=True)
				cursor.execute("SELECT COUNT(id) as addressCount from tbl_addresses WHERE user_id = %s", (session['user']['id'], ))
				addressCount = cursor.fetchone()['addressCount']
				products = []
				for p in product_info:
					query = "SELECT p.id, p.name as title, p.thumbnail, s.size, s.price, s.quantity as stock FROM tbl_products p INNER JOIN tbl_specifications s ON s.pid = p.id WHERE s.id = %s"
					params = (p['spec'],)
					cursor.execute(query, params)
					product = cursor.fetchone()
					product['spec'] = p['spec']
					product['color'] = p['color']
					product['qnt'] = p['qnt']
					products.append(product)
				cursor.close()
				return render_template('cart.html', cartProducts = products, addressCount = addressCount)
			else:
				return render_template('cart.html', cartProducts = 0)
		else:
			return render_template('cart.html', cartProducts = 0)
	else:
		return redirect('/login')
	
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
	if session.get('user'):
		variant = request.form.get('variant')
		color = request.form.get('color')
		if variant != None and variant.strip() != '' and color != None and color.strip() != '':
			cursor = cnx.cursor(dictionary=True, buffered=True)
			query = "SELECT quantity FROM tbl_specifications WHERE id = %s"
			cursor.execute(query, (variant, ))
			specs = cursor.fetchone()
			if specs != None:
				if int(specs['quantity']) > 0:
					cartItem = {'spec': variant, 'color': color}
					query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
					params = (session['user']['id'], )
					cursor.execute(query, params)
					products = cursor.fetchone()
					if products != None:
						products = json.loads(products['product_info'])
						idx = next((i for i, item in enumerate(products) if int(item["spec"]) == int(cartItem['spec']) and item['color'] == cartItem['color']), None)
						if idx != None:
							product = products[idx]
							product['qnt'] = int(product['qnt']) + 1
							products[idx] = product
						else:
							cartItem['qnt'] = 1
							products.append(cartItem)
						query = "UPDATE tbl_cart SET product_info = %s WHERE user_id = %s"
						params = (json.dumps(products), session['user']['id'])
						cursor.execute(query, params)
						cnx.commit()
					else:
						query = "INSERT INTO tbl_cart (product_info, user_id) VALUES (%s, %s)"
						cartItem['qnt'] = 1
						product = json.dumps([cartItem])
						params = (product, session['user']['id'])
						cursor.execute(query, params)
						cnx.commit()
					return jsonify({"status": True if cursor.rowcount > 0 else False, "message": "Added to cart." if cursor.rowcount > 0 else "Failed to add to cart."})
				else:
					return jsonify({"status": False, "message": "Product currently unavailable."})
			else:
				return jsonify({"status": False, "message": "Something went wrong."})
	else:
		return make_response(jsonify({"status": False, "message": "You must be logged in."})), 401
	
@app.route('/get-calc-product-price', methods=['POST'])
def get_calc_product_price():
	spec = request.form.get('spec-id')
	color = request.form.get('color')
	qnt = int(request.form.get('quantity'))
	if spec != None and spec.strip() != '' and color != None and color.strip() != '' and qnt > 0:
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT quantity, price FROM tbl_specifications WHERE id = %s"
		cursor.execute(query, (spec, ))
		variant = cursor.fetchone()
		if variant != None:
			if qnt <= int(variant['quantity']):
				query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
				cursor.execute(query, (session['user']['id'], ))
				products = cursor.fetchone()
				if products != None:
					products = json.loads(products['product_info'])
					idx = next((i for i, item in enumerate(products) if int(item["spec"]) == int(spec) and item['color'] == color), None)
					if idx != None:
						product = products[idx]
						product['qnt'] = qnt
						products[idx] = product
						query = "UPDATE tbl_cart SET product_info = %s WHERE user_id = %s"
						cursor.execute(query, (json.dumps(products), session['user']['id']))
						cnx.commit()
						if cursor.rowcount > 0:
							price = qnt * variant['price']
							return jsonify({"status": True, "price": locale.currency(price, grouping=True)})
						else:
							return jsonify({"status": False, "message": "Cart not updated"})
					else:
						return jsonify({"status": False, "message": "Product not found"})
				else:
					return jsonify({"status": False, "message": "Something went wrong"})
			else:
				return jsonify({"status": False, "message": "Invalid product quantity"})
		else:
			return jsonify({"status": False, "message": "Product variant unavailable"})
	else:
		return jsonify({"status": False, "message": "Invalid request"})

@app.route('/remove-cart-item', methods =['POST'])
def removeFromCart():
	spec = int(request.form['spec'])
	color = request.form['color']
	cursor = cnx.cursor(dictionary=True)
	query = "SELECT product_info as products FROM tbl_cart WHERE user_id = %s"
	cursor.execute(query, (session['user']['id'],))
	productInfo = cursor.fetchone()
	if productInfo != None:
		productInfo = json.loads(productInfo['products'])
		idx = next((i for i, item in enumerate(productInfo) if int(item["spec"]) == spec and item['color'] == color), None)
		if(idx != None):
			if len(productInfo) == 1:
				query = "DELETE FROM tbl_cart WHERE user_id = %s"
				val=(session['user']['id'],)
				cursor.execute(query, val)
				cnx.commit()
			else:
				del productInfo[idx]
				info = json.dumps(productInfo)
				query = "UPDATE tbl_cart SET product_info = %s WHERE user_id = %s"
				val=(info, session['user']['id'])
				cursor.execute(query, val)
				cnx.commit()
			if(cursor.rowcount > 0):
				cursor.close()
				result={'status': True, 'message': 'Removed from cart'}
			else:
				cursor.close()
				result={'status': False, 'message': 'Failed to remove from cart'}
		else:
			cursor.close()
			result={'status': False, 'message': 'Item not found'}
	else:
		cursor.close()
		result={'status': False, 'message': 'Your cart is empty'}
	return jsonify(result)

@app.route('/checkout', methods =['GET'])
def checkout():
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True, buffered=True)
		query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
		params = (session['user']['id'],)
		cursor.execute(query, params)
		data = cursor.fetchone()
		if data != None:
			product_info = json.loads(data['product_info'])
			cursor.execute("SELECT * from tbl_addresses WHERE user_id = %s", (session['user']['id'], ))
			addresses = cursor.fetchall()
			products = []
			grandTotal = 0.0
			for p in product_info:
				query = "SELECT p.id, p.name as title, p.thumbnail, s.size, s.price FROM tbl_products p INNER JOIN tbl_specifications s ON s.pid = p.id WHERE s.id = %s"
				params = (p['spec'],)
				cursor.execute(query, params)
				product = cursor.fetchone()
				product['spec'] = p['spec']
				product['color'] = p['color']
				product['qnt'] = p['qnt']
				product['total'] = round(product['price'] * p['qnt'])
				grandTotal += float(product['total'])
				products.append(product)
			cursor.close()
			return render_template('checkout.html', products = products, addresses = addresses, grandTotal = round(grandTotal))
		else:
			return redirect('/shop')
	else:
		return redirect('/login')
	
@app.route('/order', methods=['GET'])
def order():
	if session.get('user'):
		payment_method = request.args.get('payment_method')
		ship_to = request.args.get('ship_to')
		if payment_method != None and payment_method.strip() != '' and ship_to != None and ship_to.strip() != '':
			payment_method = "Pay On Delivery" if payment_method == "pod" else "UPI"
			ship_to = int(ship_to)
			order_id = str(uuid.uuid1())
			cursor = cnx.cursor(dictionary=True, buffered=True)
			query = "SELECT product_info FROM tbl_cart WHERE user_id = %s"
			params = (session['user']['id'],)
			cursor.execute(query, params)
			data = cursor.fetchone()
			if data != None:
				product_info = json.loads(data['product_info'])
				cursor.execute("SELECT title, full, city, state, pincode, contact from tbl_addresses WHERE user_id = %s and id = %s", (session['user']['id'], ship_to))
				address = cursor.fetchone()
				if address != None:
					products = []
					grandTotal = 0.0
					for p in product_info:
						query = "SELECT p.id, p.name as title, p.thumbnail, s.size, s.price, s.id as specid FROM tbl_products p INNER JOIN tbl_specifications s ON s.pid = p.id WHERE s.id = %s"
						params = (p['spec'],)
						cursor.execute(query, params)
						product = cursor.fetchone()
						product['spec'] = p['spec']
						product['color'] = p['color']
						product['qnt'] = p['qnt']
						product['total'] = round(product['price'] * p['qnt'])
						grandTotal += float(product['total'])
						products.append(product)
					query = "INSERT INTO tbl_orders (order_no, order_user, order_total, order_shipto, order_payment_mode) VALUES (%s, %s, %s, %s, %s)"
					params = (order_id, session['user']['id'], grandTotal, ship_to, payment_method)
					cursor.execute(query, params)
					if cursor.rowcount > 0:
						oid = cursor._last_insert_id
						if oid != None:
							query = "INSERT INTO tbl_order_details (order_id, product_id, product_quantity, product_color, product_total) VALUES (%s, %s, %s, %s, %s)"
							query2 = "UPDATE tbl_specifications SET quantity = quantity - %s WHERE id = %s"
							for product in products:
								params = (oid, product['spec'], product['qnt'], product['color'], product['total'])
								cursor.execute(query, params)
								cursor.execute(query2, (int(product['qnt']), product['spec']))
							query = "DELETE FROM tbl_cart WHERE user_id = %s"
							cursor.execute(query, (session['user']['id'],))
							cnx.commit()
							cursor.close()
							return render_template('order.html', order_id = order_id)
						else:
							return render_template('order-error.html')
					else:
						return render_template('order-error.html')
				else:
					return render_template('order-error.html')
			else:
				return redirect('/shop')
		else:
			return render_template('order-error.html')
	else:
		return redirect('/login')
	
@app.route('/orders', methods=['GET'])
def orders():
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT o.order_id as id, o.order_no as uuid, o.order_total as grand_total, o.order_payment_mode as pay_mode, o.order_date as date, a.title as shipto FROM tbl_orders o INNER JOIN tbl_addresses a ON a.id = o.order_shipto WHERE o.order_user = %s ORDER BY o.order_date DESC"
		cursor.execute(query, (session['user']['id'], ))
		orders = cursor.fetchall()
		return render_template('/orders.html', orders = orders)
	else:
		return redirect('/login')
	

@app.route('/order-details/<int:order_id>', methods=['GET'])
def order_details(order_id):
	if session.get('user'):
		cursor = cnx.cursor(dictionary=True)
		query = "SELECT o.order_no as uuid, o.order_total as grand_total, o.order_payment_mode as pay_mode, o.order_date as date, a.*  FROM tbl_orders o INNER JOIN tbl_addresses a ON a.id = o.order_shipto WHERE o.order_user = %s AND o.order_id = %s"
		cursor.execute(query, (session['user']['id'], order_id))
		order = cursor.fetchone()
		if order != None:
			query = "SELECT p.id, p.name as title, p.thumbnail, s.size, s.price, d.product_quantity as quantity, d.product_color as color, d.product_total as total FROM tbl_products p INNER JOIN tbl_specifications s ON p.id = s.pid INNER JOIN tbl_order_details d ON s.id = d.product_id WHERE d.order_id = %s"
			cursor.execute(query, (order_id, ))
			order_details = cursor.fetchall()
			return render_template('order-details.html', order = order, details = order_details, user = session['user'])
		else:
			return redirect('/shop')
	else:
		return redirect('/login')

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("login"))

if (__name__  == '__main__'):
	app.run(debug=True)
