from flask import Flask, jsonify
from functools import wraps
import jwt
from flaskext.mysql import MySQL
from flask import request, abort
from flask import current_app
import Users
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address






app = Flask(__name__)
app.config.from_pyfile('config.py')
mysql = MySQL()
mysql.init_app(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per minute", "3 per second"],
)



@app.errorhandler(429)
def resource_not_found(e):
    return jsonify(error={"error_message":"sorry but you attack me"}), 429

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[0]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user= Users.by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated


def token_required_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[0]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data= jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user= Users.by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if current_user["role"] != "admin":
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated


@app.route("/users")
@token_required_admin
@limiter.limit("5/second", override_defaults=False,error_message="sorry but you attack me")
def i():
    return Users.allusers()

@app.route("/users/<int:id>",methods=["GET","PUT"])
@token_required_admin
def by_id_route(id):
    return Users.by_id(id)

@app.route("/users/me",methods=["GET","PUT"])
@token_required
def idd():
    return Users.mee()

@app.route("/users/login", methods=["POST"])
@limiter.limit("2/second;2/minute")
def login():
    return Users.login()

@app.route("/users/loginSMScode", methods=["POST"])
@limiter.limit("2/second;2/minute")
def loginphonenumber():
    return Users.loginviasms()

@app.route("/users/sendsms", methods=["POST"])
@limiter.limit("2/second;5/minute")
def sendsms():
    return Users.sendsms()


if __name__ == '__main__':
    app.run(debug=True)