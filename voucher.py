from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'King In The North'

@app.route('/')
def home():
   return render_template('home.html')
   
@app.route('/list')
def list():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from voucher")
   
   rows = cur.fetchall();
   return render_template('list.html', rows = rows)

@app.route('/list2')
def list2():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from voucher")
   
   rows = cur.fetchall();
   return render_template('list2.html', rows = rows)
   
@app.route('/deletepesanan',methods = ['POST', 'GET'])
def deletepesanan():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   pesanId = request.form['postPesananId']

   cur = con.cursor()
   print(pesanId)
   cur.execute("delete from pesan where pesanId=?", (pesanId,))
   con.commit()

   return order()
   
@app.route('/deletevoucher',methods = ['POST', 'GET'])
def deletevoucher():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   voucherId = request.form['postvoucherId']

   cur = con.cursor()
   print(voucherId)
   cur.execute("delete from voucher where voucherId=?", (voucherId,))
   con.commit()

   return list2()
   
@app.route('/order')
def order():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   username = session['username']

   cur = con.cursor()
   cur.execute("select * from user where email=?", [username])
   rows = cur.fetchone();
   userId = rows['userId']
   
   cur.execute("select * from voucher")
   rows = cur.fetchall();
   print(rows)
   cur.execute("select * from pesan where userId=?", (userId,))
   rows2 = cur.fetchall();
   print(rows2)
   return render_template('order.html',rows=rows, rows2=rows2)

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/addvoucher')
def addvoucher():
   return render_template('addvoucher.html')

@app.route('/detailvoucher',methods = ['POST', 'GET'])
def detailvoucher():
   id = request.args.get('id')
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from voucher where voucherId=?", id)

   rows = cur.fetchone();
   
   return render_template('detailvoucher.html', row = rows)

@app.route('/pesanvoucher',methods = ['POST', 'GET'])
def pesanvoucher():
   if request.method == 'POST':
      try:
         username = session['username']
         voucherId = request.form['postvoucherId']
         print(voucherId)
         con = sql.connect("tos.db")
         con.row_factory = sql.Row 
   
         cur = con.cursor()
         cur.execute("select * from user where email=?", [username])
         rows = cur.fetchone();
         userId = rows['userId']
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            print(userId)
            print(voucherId)
            cur.execute("INSERT INTO pesan (voucherId, userId) VALUES (?,?)",(voucherId, userId))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return list()

@app.route('/tambahvoucher',methods = ['POST', 'GET'])
def tambahvoucher():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         star = request.form['postStar']
         price = request.form['postPrice']
         
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO voucher (name, description, imageUrl, star, price) VALUES (?,?,?,?,?)",(name, description, imageUrl, star, price) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         
   
@app.route('/editvoucher',methods = ['POST', 'GET'])
def editvoucher():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         star = request.form['postStar']
         price = request.form['postPrice']
         voucherId = request.form['postvoucherId']
         print name, description, imageUrl, star, price, voucherId
         
         con = sql.connect("tos.db")
         cur = con.cursor()

         cur.execute("UPDATE voucher SET name=?, description=?, imageUrl=?, star=?, price=? WHERE voucherId=?",(name, description, imageUrl, star, price, voucherId))
             
         con.commit()
      except Exception as e:
         print e
         con.rollback()
      finally:
         return listadmin()
         
@app.route('/formregister',methods = ['POST', 'GET'])
def formregister():
   if request.method == 'POST':
      try:
         email = request.form['postEmail']
         password = request.form['postPassword']
         
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO user (email, password) VALUES (?,?)",(email,password) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         

@app.route('/formlogin',methods = ['POST', 'GET'])
def formlogin():
   if request.method == 'POST':
      email = request.form['postEmail']
      password = request.form['postPassword']
      con = sql.connect("tos.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute('SELECT COUNT(*) FROM user WHERE email=? AND password=?', (email, password))
   
      rows = cur.fetchone()

      if rows[0] == 1:
         session['username'] = request.form['postEmail']

         return home()
      else:
         return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return home()
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
   app.debug = True
   app.run('0.0.0.0',5130)
