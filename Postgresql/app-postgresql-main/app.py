from flask import Flask, flash, redirect, request, session, render_template, abort
import os
import psycopg2

app = Flask (__name__)

def get_db_connect():
    connect = None
    emp = None
    dept = None
    tabla = None

    try:
        connect = psycopg2.connect(host="192.168.125.13", dbname="scott", user="mario", password="hola")
    except Exception as excepcion:
        print("No puedo conectar a la base de datos:",excepcion)

    return connect


def emp_dept():
    connect = get_db_connect()

    emp = connect.cursor()
    emp.execute("select * from emp;")
    empno = emp.fetchall()

    tabla_cursor = connect.cursor()
    tabla_cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    tablas = tabla_cursor.fetchall()

    dept = connect.cursor()
    dept.execute("select * from dept;")
    deptno=dept.fetchall()

    return render_template("basedatos.html", tablas=tablas, empno=empno, deptno=deptno)


@app.route('/',methods=["GET"])
def inicio():
    if not session.get("logged_in"):
        return render_template("inicio.html")
    else:
        return emp_dept()

@app.route('/login', methods=["POST"])
def login():
    if request.form['username'] == 'mario' and request.form['password'] == 'hola':
        session['logged_in'] = True
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run('0.0.0.0' ,debug=False)
