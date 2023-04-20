from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/random", methods = ["GET","POST"])
def random():
    if request.method == "GET":
        l = Cafe.query.count()
        c = randint(0,l-1)
        ca = Cafe.query.offset(c).first()
        dic = {"can_take_calls": ca.can_take_calls, "coffee_price":ca.coffee_price,"has_sockets":ca.has_sockets,"has_toilet":ca.has_toilet,"has_wifi": ca.has_wifi, "id":ca.id, "img_url": ca.img_url,"location":ca.location,"map_url": ca.map_url,"name": ca.name,"seats":ca.seats }
        return jsonify(cafe=dic)
@app.route("/all")
def all():
    lis = Cafe.query.all()
    dic = [{"can_take_calls": ca.can_take_calls, "coffee_price":ca.coffee_price,"has_sockets":ca.has_sockets,"has_toilet":ca.has_toilet,"has_wifi": ca.has_wifi, "id":ca.id, "img_url": ca.img_url,"location":ca.location,"map_url": ca.map_url,"name": ca.name,"seats":ca.seats } for ca in lis]
    return jsonify(cafe=dic)
@app.route("/search")
def search():
    query_location = request.args.get("location")
    lis = Cafe.query.filter_by(location=query_location).all()
    if lis:
        dic = [{"can_take_calls": ca.can_take_calls, "coffee_price": ca.coffee_price, "has_sockets": ca.has_sockets,
                "has_toilet": ca.has_toilet, "has_wifi": ca.has_wifi, "id": ca.id, "img_url": ca.img_url,
                "location": ca.location, "map_url": ca.map_url, "name": ca.name, "seats": ca.seats} for ca in lis]
        return jsonify(cafe=dic)
    else:
        return jsonify(error={"Not Found": "Sorry,we don't have a cafe at that location"})
@app.route("/add", methods = ["POST"])
def add():
    new_cafe = Cafe(
        id=request.form.get("id"),
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
@app.route("/update-price/<int:id>", methods = ["PATCH"])
def update(id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
@app.route("/report-closed/<int:id>", methods=["DELETE"])
def dele(id):
    c = Cafe.query.get(id)
    api_key = "hello"
    if c:
        if request.args.get("api_key") == api_key:
            db.session.delete(c)
            db.session.commit()
            return jsonify(success="Success")
        else:
            return jsonify(error="Sorry that's not allowed to make")
    else:
        return jsonify(error={"Not Found":"Sorry a cafe with that id doesn't exists"})

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
