from flask import Flask, render_template, request, redirect,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


#Mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flaskpython"
mysql = MySQL(app)

#Session
app.secret_key = "mysecretkey"


@app.route("/")
def contact():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    return render_template("index.html", contacts = data)

@app.route("/add_contact", methods=["POST"])
def addContact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash("Contact Added successfully")
        return redirect(url_for("contact"))

@app.route("/edit/<string:id>")
def editContact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = (%s)", (id))
    data = cur.fetchall()
    return render_template("edit.html", contact = data[0])
    

@app.route("/update/<string:id>", methods=["POST"])
def updateContact(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]    
        cur = mysql.connection.cursor()
        cur.execute("UPDATE contacts SET fullname=(%s),phone=(%s), email=(%s) WHERE id = (%s)", (fullname, phone, email, id))
        mysql.connection.commit()
        flash("Contact updated successfully")
        return redirect(url_for("contact"))


@app.route("/delete/<string:id>")
def deleteContact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id = (%s)", (id))
    mysql.connection.commit()
    flash("Contact deleted successfully")
    return redirect(url_for("contact"))




app.run(port=3000, debug=True)