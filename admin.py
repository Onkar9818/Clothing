from flask import Flask, Response, make_response, redirect,render_template, request, session,url_for,flash
from mysql.connector import MySQLConnection
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF
import datetime

app = Flask(__name__)

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

'''_____________________________________________________________________________________________________'''

@app.route('/')
def login():
    return render_template('signin.html')

@app.route('/error')
def error():
    flash("Wrong password! try again.")
    return redirect(url_for('login')) 

@app.route('/display', methods=['POST'])
def display():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        cursor = cnx.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM clothing_store.admlogin where admlogin.username=%s and admlogin.password=%s"
        val = (username, password)
        cursor.execute(query, val)
        data = cursor.fetchall()
        cursor.close()
        print(data)
        if data:
            if password == data[0]['password']:
                resp = make_response(render_template("pcategory.html"))
                return resp
            else:
                flash("Wrong password! Please try again.")
                return redirect(url_for('login'))
        else:
            flash("Username not found")
            return redirect(url_for('login'))


'''__________________________________________________________________________________________________'''
@app.route('/home')
def index():
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT * FROM clothing_store.tbl_categories")
    data=cursor.fetchall()
    return render_template('pcategory.html', cat=data)
    
@app.route('/add_product', methods =['POST'])
def add_product():
    if request.method=='POST':
        title = request.form['title']
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute('INSERT INTO clothing_store.tbl_categories (title,date) VALUES (%s, now())',(title,))
        cnx.commit()
        flash('Category added successufully')
        return redirect(url_for('index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_product(id):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM clothing_store.tbl_categories WHERE id = %s',(id,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('pcategoryedit.html', product = data[0])
 
@app.route('/update/<nid>', methods=['POST'])
def update_product(nid):
    if request.method == 'POST':
        title = request.form['title']
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute('UPDATE clothing_store.tbl_categories SET title=%s, date=now() where id=%s',(title,nid))
        flash('Category Updated Successfully')
        cnx.commit()
        return redirect(url_for('index'))

@app.route('/delete/<nid>', methods = ['POST','GET'])
def delete_category(nid):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('DELETE FROM clothing_store.tbl_categories WHERE id = {0}'.format(nid))
    cnx.commit()
    flash('Category Removed Successfully')
    return redirect(url_for('index'))

'''__________________________________________________________________________________________________'''

@app.route('/products')
def index1():
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT * FROM clothing_store.tbl_products")
    data=cursor.fetchall()
    cursor.execute("select id from clothing_store.tbl_categories")
    data1=cursor.fetchall()
    cursor.execute("select id,title from clothing_store.tbl_categories")
    data11=cursor.fetchall()
    l1=len(data11)
    return render_template('products.html', product=data, product1=data1, data11=data11, l1=l1)

@app.route('/products1', methods=['POST'])
def products1():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        thumbnail = request.files['thumbnail']
        category = request.form['id']
        
        if thumbnail:
            filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join('C:\\vck\\Project\\Clothing\\static\\images', filename))

            cursor = cnx.cursor(buffered=True, dictionary=True)
            query = "INSERT INTO clothing_store.tbl_products (name, description, thumbnail, category) VALUES (%s, %s, %s, %s)"
            val = (name, description,'images/'+filename, category)
            cursor.execute(query, val)
            cnx.commit()
            
            flash('Product added successfully')
            return redirect(url_for('index1'))
    
@app.route('/productedit/<aid>', methods = ['POST', 'GET'])
def products_edit(aid):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM clothing_store.tbl_products WHERE id = %s',(aid,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('productsedit.html', product = data[0])
 
@app.route('/productupdate/<did>', methods=['POST'])
def update_products(did):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        thumbnail = request.files['thumbnail']

        if thumbnail:
            filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join('C:\\vck\\Project\\Clothing\\static\\images', filename))

            cursor = cnx.cursor(buffered=True, dictionary=True)
            query='UPDATE clothing_store.tbl_products SET name=%s, description=%s, thumbnail=%s where id=%s'
            cursor.execute(query,(name,description,'images/'+filename,did))
            cnx.commit()

            flash('Product Updated Successfully')
            return redirect(url_for('index1'))

@app.route('/productdelete/<did>', methods = ['POST','GET'])
def delete_products(did):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('DELETE FROM clothing_store.tbl_products WHERE id = {0}'.format(did))
    cnx.commit()
    flash('Product Removed Successfully')
    return redirect(url_for('index1'))

'''____________________________________________________________________________________________________'''
   
@app.route('/pspecific')
def index2():
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("SELECT * FROM clothing_store.tbl_specifications")
    data=cursor.fetchall()
    cursor.execute("select id from clothing_store.tbl_products")
    data1=cursor.fetchall()
    cursor.execute("select id,name from clothing_store.tbl_products")
    data11=cursor.fetchall()
    l1=len(data11)
    return render_template('pspecification.html', product=data, product1=data1, data11=data11, l1=l1)

@app.route('/pspecific1', methods =['POST'])
def pspecific1():
    if request.method=='POST':
        size = request.form['size']
        quantity = request.form['quantity']
        price = request.form['price']
        pid = request.form['pid']
        cursor = cnx.cursor(buffered=True, dictionary=True)
        query='INSERT INTO clothing_store.tbl_specifications (size,quantity,price,pid,date) VALUES (%s, %s, %s, %s, now())'
        val=(size,quantity,price,pid)
        cursor.execute(query,val)
        cnx.commit()
        flash('Specification added successufully')
        return redirect(url_for('index2'))

@app.route('/edit2/<eid>', methods = ['POST', 'GET'])
def pspecific_edit(eid):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM clothing_store.tbl_specifications WHERE id = %s',(eid,))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('pspecificationedit.html', product = data[0])
 
@app.route('/update2/<fid>', methods=['POST'])
def update_pspecific(fid):
    if request.method == 'POST':
        size = request.form['size']
        quantity = request.form['quantity']
        price = request.form['price']
        cursor = cnx.cursor(buffered=True, dictionary=True)
        query='UPDATE clothing_store.tbl_specifications SET size=%s, quantity=%s, price=%s, date=now() where id=%s'
        cursor.execute(query,(size,quantity,price,fid))
        flash('Specification Updated Successfully')
        cnx.commit()
        return redirect(url_for('index2'))

@app.route('/delete2/<gid>', methods = ['POST','GET'])
def delete_pspecific(gid):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute('DELETE FROM clothing_store.tbl_specifications WHERE id = {0}'.format(gid))
    cnx.commit()
    flash('Specification Removed Successfully')
    return redirect(url_for('index2'))

'''______________________________________________________________________________________________________'''

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route('/download/userreport/pdf',methods=['POST'])
def download_userreport():
    if request.method=="POST":
        now=datetime.date.today()
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute("SELECT * from clothing_store.tbl_users")
        result=cursor.fetchall()
        print(result)
    
        pdf=FPDF()
        pdf.add_page()
        page_width=pdf.w-2*pdf.l_margin
        
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width,0.0,"Street Illusion",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Tarabai park kolhapur",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Users Report",align='C')
        pdf.ln(7)
        pdf.ln(10)
        
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Date:- "+now.strftime("%d/%m/%y"),align='L')
        pdf.ln(4)
    
        pdf.line(x1=0,y1=35,x2=300,y2=35)

        pdf.set_font('Courier','',10)
        col_width=page_width/4
        pdf.ln(1)

        th=pdf.font_size
        i=1
        pdf.cell(20,th,"User Id",border=1)
        pdf.cell(col_width,th,"First Name",border=1)
        pdf.cell(col_width,th,"Last Name",border=1)
        pdf.cell(col_width,th,"Email",border=1)
          
        pdf.ln(th)
        for col in result:
            pdf.cell(20,th,str(col[0]),border=1)
            pdf.cell(col_width,th,(col[1]),border=1)
            pdf.cell(col_width,th,(col[2]),border=1)
            pdf.cell(col_width,th,(col[3]),border=1)
            i=i+1
            pdf.ln(th)
        pdf.ln(10)

        cursor.close()
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=users_report.pdf'})

def split_line(line, chunk_size=40):
    chunks = [line[i:i+chunk_size] for i in range(0, len(line), chunk_size)]
    return chunks

@app.route('/download/productreport/pdf',methods=['POST'])
def download_productreport():
    if request.method=="POST":
        now=datetime.date.today()
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute("select tbl_categories.id,tbl_categories.title,tbl_products.id,tbl_products.category,tbl_products.name,tbl_products.description from clothing_store.tbl_categories,clothing_store.tbl_products where clothing_store.tbl_categories.id=clothing_store.tbl_products.category")
        result=cursor.fetchall()
        print(result)
    
        pdf=FPDF('L')
        pdf.add_page()
        page_width=pdf.w-2*pdf.l_margin
        
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width,0.0,"Street Illusion",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Kolhapur",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Product Report",align='C')
        pdf.ln(7)
        pdf.ln(10)
        
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Date:- "+now.strftime("%d/%m/%y"),align='L')
        pdf.ln(4)
    
        pdf.line(x1=0,y1=35,x2=300,y2=35)

        pdf.set_font('Courier','',10)
        col_width=page_width/6
        pdf.ln(1)

        th=pdf.font_size
        i=1
        pdf.cell(15,th,"Cat Id",align='C')
        pdf.cell(23,th,"Title",align='C')
        pdf.cell(15,th,"Pro Id",align='C')
        pdf.cell(20,th,"Category",align='C')
        pdf.cell(80,th,"Name",align='C')
        pdf.cell(120,th,"Description",align='C')
          
        pdf.ln(th+2)
        for col in result:
            pdf.cell(15,th,str(col[0]),align='C')
            pdf.cell(23,th,(col[1]),align='C')
            pdf.cell(15,th,str(col[2]),align='C')
            pdf.cell(20,th,str(col[3]),align='C')
            pdf.cell(80,th,(col[4]),align='C')
            print(len(col[5]))
            c=1
            if len(col[5])>50:
                chunks = split_line(col[5])
                print(chunks,len)
                for chunk in chunks:
                    print(chunk,c)
                    if c==1:
                        pdf.cell(150, th, chunk )
                    else:
                        pdf.cell(150,th,"")
                        pdf.cell(150, th, chunk )
                    c=c+1
                    pdf.ln(th)
            else:
                pdf.cell(200, th, col[5] )
            i=i+1
            pdf.ln(th+2)
        pdf.ln(10)

        cursor.close()
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=products_report.pdf'})


@app.route('/download/cartreport/pdf',methods=['POST'])
def download_cartreport():
    if request.method=="POST":
        now=datetime.date.today()
        cursor = cnx.cursor(buffered=True, dictionary=True)
        cursor.execute("select tbl_cart.user_id,tbl_users.email,tbl_cart.product_info,tbl_cart.date from clothing_store.tbl_cart,clothing_store.tbl_users where tbl_cart.user_id=tbl_users.id")
        result=cursor.fetchall()
        print(result)
    
        pdf=FPDF('L')
        pdf.add_page()
        page_width=pdf.w-2*pdf.l_margin
        
        pdf.set_font('Times','B',14.0)
        pdf.cell(page_width,0.0,"Street Illusion",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Kolhapur",align='C')
        pdf.ln(7)
        pdf.cell(page_width,0.0,"Cart Report",align='C')
        pdf.ln(7)
        pdf.ln(10)
        
        pdf.set_font('Times','B',12.0)
        pdf.cell(page_width,0.0,"Date:- "+now.strftime("%d/%m/%y"),align='L')
        pdf.ln(4)
    
        pdf.line(x1=0,y1=35,x2=300,y2=35)

        pdf.set_font('Courier','',10)
        col_width=page_width/6
        pdf.ln(1)

        th=pdf.font_size
        i=1
        pdf.cell(17,th,"User Id",border=1)
        pdf.cell(50,th,"Email",border=1)
        pdf.cell(110,th,"Product Info",border=1)
        pdf.cell(50,th,"Date",border=1)
          
        pdf.ln(th)
        for col in result:
            pdf.cell(17,th,str(col[0]),border=1)
            pdf.cell(50,th,(col[1]),border=1)
            pdf.cell(110,th,(col[2]),border=1)
            pdf.cell(50,th,str(col[3]),border=1)
            i=i+1
            pdf.ln(th)
        pdf.ln(10)

        cursor.close()
        return Response(pdf.output(dest='S').encode('latin-1'),mimetype='application/pdf',headers={'Content-Disposition':'attachment;filename=cart_report.pdf'})


'''______________________________________________________________________________________________________'''
# running application 
if __name__ == '__main__': 
    app.run(debug=True) 