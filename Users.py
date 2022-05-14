from flask import Flask, jsonify
import jwt
from flaskext.mysql import MySQL
from flask import request
from flask import current_app
import math
import datetime
import re
import random


regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex_name_en_ar = '^[a-zA-Zء-ي]{4,}(?: [a-zA-Zء-ي]+)?(?: [a-zA-Zء-ي]+)?$'

def check_email(email):
    if (re.search(regex_email, email)):
        return "1"
    else:
        return "2"

def check_name_en_ar(name):
    if (re.search(regex_name_en_ar, name)):
        return "1"
    else:
        return "2"

def check_gender(gender):
    if gender == "male":
        return "1"
    if gender == "female":
        return "1"
    return "2"

def check_phone_number(s):
    try:
        int(s)
        if len(s) >= 14:
            return "please enter valid number format 9665XXXXXXXX or 5XXXXXXXX"
        number_5 = r"^(5)\d{8}\b$"
        number966 = r"^(966)\d{9}\b$"
        if len(s) == 9:
            Pattern = re.compile(number_5)
            if Pattern.match(s):
                return "1"
            else:
                return Pattern.match(s)
        if len(s) == 12:
            Pattern = re.compile(number966)
            if (Pattern.match(s)):
                return "1"
            else:
                return "2"
        return "please enter valid number format 9665XXXXXXXX or 5XXXXXXXX"
    except ValueError:
        return "please enter valid number not string "

def check_code6dig(s):
    if len(s) > 6:
        return "2"
    return "1"
app = Flask(__name__)
app.config.from_pyfile('config.py')
mysql = MySQL()
mysql.init_app(app)


def login1(email,password):#it should be email password
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s and password = %s;"
        cursor.execute(query,(email,password))
        rows = cursor.fetchall()
        return {"user_id":rows[0][0],"name":rows[0][1],"role":rows[0][3],"email":rows[0][4],"mobile":rows[0][5],"gender":rows[0][6]}
    except Exception as e:
        print(e)

def allusers():
    page = request.args.get('page')
    if page is None:
        page = 0

    try:
        page = int(page)
        to = int(page) * 20
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users ORDER BY ID ASC LIMIT {} ,20;""".format(to))
        rows = cursor.fetchall()
        cursor.execute("SELECT COUNT(ID) AS total FROM users;")
        dd = cursor.fetchall()
        s = dd[0][0]
        list1 = list(rows)
        users = []
        for xx in list1:
            users.append({"user_id": str(xx[0]), "name": str(xx[1]), "role": str(xx[3]), "email": str(xx[4]),
                          "mobile": str(xx[5]), "gender": str(xx[6])})
        next = str(int(page) + 1)
        allpage = str(math.ceil(s / 20))
        if int(next) > int(allpage):
            next = str(allpage)
        cursor.close()
        conn.close()
        return {
            "message": 1,
            "data": users,
            "nextpage:": next ,
            "allpage:": allpage
        }
    except ValueError as e:
        return jsonify(error="page must integer")
    except Exception as e:
        print(str(e))
        return jsonify(error="something wrong")

def by_id(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users WHERE id = "{}";""".format(id))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"user_id": rows[0][0], "name": rows[0][1], "role": rows[0][3], "email": rows[0][4], "mobile": rows[0][5],
            "gender": rows[0][6],"active":rows[0][7]}
    except Exception as e:
        return {"error":"somthing wrong"}

def mee():
    token = request.headers["Authorization"].split(" ")[0]
    data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    if request.method == "GET":
        try:
            id = data["user_id"]
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = %s;"
            cursor.execute(query,(id))
            rows = cursor.fetchall()
            user = {"user_id": rows[0][0], "name": rows[0][1], "role": rows[0][3], "email": rows[0][4],
                    "mobile": rows[0][5],
                    "gender": rows[0][6],}
            if rows[0][1] == "" and rows[0][4] == "" and rows[0][6] == None:
                return {
                    "message": 1,
                    "data": user,
                    "completedata": "false # required complete data name , email and gender"
                }
                cursor.close()
                conn.close()
            cursor.close()
            conn.close()
            return {
                    "message": 1,
                    "data": user,
                    "completedata": "True"
                }
        except Exception as e:
            return {"error": "somthing wrong"}
    elif request.method == "PUT":
        try:
            data1 = request.json
            if not data1:
                return {
                           "message": "Please provide user details",
                           "data": None,
                           "error": "Bad request"
                       }, 400
            email = data1["email"]
            if check_email(email) != "1":
                return {"message":"enter valid email"},500
            name = data1["name"]
            if check_name_en_ar(name)!="1":
                return {"message": "enter valid name"}, 500
            gender = data1["gender"]
            if check_name_en_ar(gender)!="1":
                return {"message": "enter valid gender"}, 500
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "UPDATE users SET name = %s, email = %s ,gender = %s WHERE id = %s;"
            cursor.execute(query,(name, email,gender, str(data["user_id"])))
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "Successfully update the data"}
        except Exception as e:
            return {"error": "somthing wrong","message":str(e)}, 401

def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        user = login1(data["email"],data["password"])
        if user:
            try:
                # token should expire after 20 minuets
                user["token"] = jwt.encode(
                    {"user_id": user["user_id"], "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "1",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500


def sendsms():
    data = request.json
    if not data:
        return {
                   "message": "Please provide user details",
                   "data": None,
                   "error": "Bad request"
               }, 400
    try:
        phone_number =data["phone_number"]
        dig6 = random.randint(000000, 999999)
        if check_phone_number(phone_number) != "1":
            return {"error":check_phone_number(phone_number)}
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM codes_sms WHERE expire < NOW()""")
        cursor.execute("SELECT * FROM codes_sms WHERE mobile = %s",(phone_number,)) #query execute direct
        msg = cursor.fetchone()
        if msg:
            return {"error":'the code still valid if not receive it try after 2 mints '}
        query = "INSERT INTO codes_sms (mobile, code, expire) VALUES (%s,%s, NOW() + INTERVAL 2 MINUTE);"# then send the code via sms gateway and handle it
        cursor.execute(query, (phone_number,dig6))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Successfully send the code to {} also code is {}".format(phone_number,dig6)}# for debug i send code in res
    except Exception as e:
        return {"error":"oops something went wrong","message":str(e)}



def loginviasms():
    data = request.json
    if not data:
        return {
                   "message": "Please provide user details",
                   "data": None,
                   "error": "Bad request"
               }, 400
    try:
        phone_number = data["phone_number"]
        code = data["code"]
        if check_phone_number(phone_number) != "1":
            return {"error": check_phone_number(phone_number)}
        if check_code6dig(code) != "1":
            return {"error":"the code must equal 6 or less"}
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM codes_sms WHERE expire < NOW()""")
        cursor.execute("SELECT * FROM codes_sms WHERE mobile = %s",(phone_number,))
        msg = cursor.fetchone()
        if not msg:
            cursor.close()
            conn.close()
            return {"error":'no codes send to the number'}
        query = "SELECT * FROM codes_sms WHERE mobile = %s and code = %s;"
        cursor.execute(query,(phone_number,code))
        msg = cursor.fetchone()
        if not msg:
            cursor.close()
            conn.close()
            return {"error":'error code'}
        cursor.execute("SELECT * FROM users WHERE mobile = %s",(phone_number,))
        msg = cursor.fetchall()
        if not msg:
            query = "INSERT INTO users(mobile) VALUES (%s);"
            cursor.execute(query,(phone_number))
            conn.commit()
            query = "SELECT * FROM users WHERE mobile = %s;"
            cursor.execute(query, (phone_number))
            rows = cursor.fetchall()
            user = {"user_id": rows[0][0], "name": rows[0][1], "role": rows[0][3], "email": rows[0][4], "mobile": rows[0][5],
            "gender": rows[0][6],"token":""}
            user["token"] = jwt.encode(
                    {"user_id": user["user_id"], "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
            cursor.execute("""DELETE FROM codes_sms WHERE mobile = {}""".format(phone_number))
            conn.commit()
            cursor.close()
            conn.close()
            return {
            "message": "Successfully add user",
            "data": user,
            "new": "True [TRUE] # now let the user go to PUT /users/me via auth to add his info its required name , email and gender only"
                    }
        cursor.execute("""DELETE FROM codes_sms WHERE mobile = {}""".format(phone_number))
        conn.commit()
        query = "SELECT * FROM users WHERE mobile = %s;"
        cursor.execute(query, (phone_number))
        rows = cursor.fetchall()
        user = {"user_id": rows[0][0], "name": rows[0][1], "role": rows[0][3], "email": rows[0][4], "mobile": rows[0][5],
                "gender": rows[0][6],"token":""}
        if rows[0][1] == "" and rows[0][4] == "" and rows[0][6] == None:
            user["token"] = jwt.encode(
                {"user_id": user["user_id"], "iat": datetime.datetime.utcnow(),
                 "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            cursor.close()
            conn.close()
            return {
                "message": "Successfully add user",
                "data": user,
                "new": "True [TRUE] # now let the user go to /users/me via auth to add his info its required name , email and gender only\n because he is not complete /users/me then he is login again this why the data not complete  "
            }

        user["token"] = jwt.encode(
            {"user_id": user["user_id"], "iat": datetime.datetime.utcnow(),
             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        cursor.close()
        conn.close()
        return {
            "message": "Successfully add user",
            "data": user,
            "new": "False [False] # the data its complete "
        }
    except Exception as e:
        return {"error": "oops something went wrong", "message": str(e)}