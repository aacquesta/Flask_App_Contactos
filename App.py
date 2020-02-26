from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)

#Mysqlconnection
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flaskcontacts'
mysql = MySQL(app)

#Vamos a gusadar la sesion dentro de la memoria de la aplicacion
#Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor() #Me conecto a la base de datos
    cur.execute('SELECT * FROM contacts') #Registro? la consulta a realizar
    data=cur.fetchall() #Ejecuto? la consulta
    return render_template('index.html', contacts = data) #le paso a index.html los datos resultantes

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method =='POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)', (fullname,phone,email))
        mysql.connection.commit()
        flash("Contact added succesfully")
        return redirect (url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id=%s', (id))#Declarar la consulta
    data = cur.fetchall()    
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method =='POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur=mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            phone = %s,
            email = %s
        WHERE id= %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash("Contact successfully updated")
        return redirect (url_for('Index'))  


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
#    cur.execute('DELETE FROM contacts WHERE id= %s',id)
    mysql.connection.commit()
    flash('Contact succesfully removed')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug= True) 
#esto es un comentario