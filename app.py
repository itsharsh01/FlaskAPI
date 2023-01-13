import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask,request,jsonify
from datetime import datetime



load_dotenv()
app= Flask(__name__)
url=os.getenv("DATABASE_URL")
connection=psycopg2.connect(url)

@app.post('/api/postMessage')
def postMessage():
    try:
        data = request.get_json()
        msg = data["msg"]
        userId=data["user"]
        mydate=datetime.now()
        mytime=datetime.now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO messages(msg,mydate,mytime,uid) values(%s,%s,%s,%s) RETURNING id;",(msg,mydate,mytime,userId,))
                id=cursor.fetchone()[0]
                # cursor.execute(INSERT_LIKE,(id,0,))

        return jsonify({"id":id,"messgae":f"Your Message-> {msg}."})
    except:
        return jsonify({"Response":"No Response From Your Side"})    


@app.get('/api/getMessage')
def getMessage():
    try:
        all_messages=[]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT a.id,a.msg,a.mydate,a.mytime,a.uid,b.num_like From messages as a left join likes_table as b on a.id=b.mid ORDER BY a.mytime DESC;""")
                rounds=cursor.fetchall()
                for row in rounds:
                    all_messages.append({
                        "Message":row[1],
                        "Date":str(row[2]),
                        "Time":str(row[3]),
                        "User Id":row[4],
                        "Likes":row[5]
                    })
        return  jsonify({
        "Status":"OK",
        "List":all_messages
        })   
    except:
        return jsonify({"Response":"No Response From Your Side"})    

@app.delete('/api/deleteMessage')
def deleteMessage():
    try:
        data = request.get_json()
        mid=data["mid"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT msg FROM messages WHERE id=%s""",(mid,))
                message=cursor.fetchone()[0]
                cursor.execute("DELETE FROM messages WHERE id=%s",(mid,))    
        return jsonify({"DeletedMessage":f"{message}."})
    except:
        return jsonify({"Response":"No Response From Your Side"})    


@app.put('/api/likeMessage')
def likeMessage():
    try:
        data = request.get_json()
        like = (data["like"])
        mid=data["mid"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT num_like from likes_table where mid=%s;""",(mid,))
                num_like=cursor.fetchone()[0]
                if(like) :
                    num_like+=1
                else :
                    num_like-=1    
                cursor.execute("UPDATE likes_table set num_like=%s where mid=%s;",(num_like,mid,))    
        return jsonify({"Number Of Like":f"Total Like On Your Message-> {num_like}."})
    except:
        return jsonify({"Response":"No Response From Your Side"})


    
