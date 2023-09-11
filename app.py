from flask import Flask,render_template,request,redirect
import psycopg2
import psycopg2.extras

def Database(q,send=False):
    conn=None
    cur=None
    try:
        conn=psycopg2.connect(
            database="flask_db",
            user='postgres',
            password="Naresh@123",
            host="localhost",
            port=5432
        )
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # fetch data----------------
        cur.execute(q)
        if send:
            conn.commit()
            return True
        else: 
            data=cur.fetchall()
            return data

    except Exception as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

app = Flask(__name__)





@app.route('/',methods=["POST","GET"])
def hello_world():
    if request.method=="POST":
        print(request.form["title"])
        print(request.form["des"])
        Database(f"INSERT INTO todo VALUES ('{request.form['title']}','{request.form['des']}')",send=True)
    allTodo=Database("SELECT * FROM todo")
    return render_template("index.html",allTodo=allTodo)

@app.route("/show") # Convert these function into api.
def show():
    return  "hello"

@app.route("/delete/<int:uid>")
def deleted(uid):
    res=Database(f"DELETE FROM todo WHERE id={uid};",send=True)
    return redirect("/")




@app.route("/update/<int:uid>")
def update(uid):
    todo=Database(f"SELECT * FROM todo WHERE id = {uid}")
    return render_template("add.html",todo=todo)


@app.route("/update/upr",methods=["GET","POST"])
def upr():
    if(request.method=="POST"):
        Database(f"UPDATE todo SET title = '{request.form['title']}',des='{request.form['des']}' WHERE id={request.form['uid']}",send=True)
    return redirect('/')

def dataTwoDict(data):
    if(not data):
        return {}
    dataInDict={}
    dataInDict.update({"title":data[0][0],"des":data[0][1]})
    return dataInDict
@app.route('/data/<int:uid>')
def datatest(uid):
    data=Database(f"SELECT * FROM todo WHERE id={uid}")
    return dataTwoDict(data)

    


if __name__=="__main__":
    app.run(debug=True,port=8000)