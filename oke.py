import sqlite3
from flask import Flask, render_template, url_for, flash, redirect
import sqlite3 as sql
app = Flask(__name__)


#conn = sqlite3.connect('sites.db')
#print ("Opened database successfully")

#conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
#print ("Table created successfully")
#conn.close()

@app.route('/')
def home():
   con = sql.connect("site.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from v1 where University of Divinity<100")

   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)



@app.route('/list')
def list():
   con = sql.connect("site.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from v1 where University of Divinity<100")

   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)












if __name__ == '__main__':
   app.run(debug = True)
   