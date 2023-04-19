from flask import Flask, render_template, redirect, request, url_for,flash
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import json

import ocr

app = Flask(__name__)

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense2.db"
db.init_app(app)


class Expense1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    ampount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String)
    payee = db.Column(db.String)
    mode= db.Column(db.String)

    def __repr__(self):
        return '%s On %r you paid ₹%s to %r for %r through %s' %(self.id, self.date, self.ampount, self.payee, self.category, self.mode)

with app.app_context():
    db.create_all()

@app.route("/expenses")
def user_list():
    ex_val = Expense1.query.order_by(Expense1.date)
    ex_amt= Expense1.query.with_entities(Expense1.ampount, Expense1.date).group_by(Expense1.id).order_by(Expense1.id).all()
    
    ex_amt2=[]
    ex_date=[]
    for total,_ in ex_amt:
        ex_amt2.append(total)
        ex_date.append(_)
    return render_template('list.html', headings=headings, data= data, ex_val=ex_val, 
                           ex_amts=json.dumps(ex_amt2),ex_dates=json.dumps(ex_date) )  

@app.route("/expenses/addexp", methods=["GET", "POST"])
def user_create():
    
    if request.method == "POST":
        expenses = Expense1(
            id=request.form["id"], 
            date=request.form["date"],
            ampount=request.form["ampount"],
            category = request.form["category"],
            payee = request.form["payee"],
            mode= request.form["mode"],
        )
        if(expenses.id != None):
            ex_id =  db.session.query(Expense1.id).filter(expenses.id >= expenses.id ).first()
            ex_id1 = db.session.query(Expense1).filter(Expense1.id >= expenses.id).first()
            
        if ex_id1 == None:
            db.session.add(expenses)
            flash("Expense added sucessfully", "success")
            db.session.commit()
            return redirect(request.url)
        else:
            flash("Id already present", "warning")
            return redirect(request.url)
    
        # return redirect(url_for("expense_detail", id=expenses.id))
    return render_template("create.html")

@app.route("/expenses/<int:id>")
def expense_detail(id):
    expenses = db.get_or_404(Expense1, id)
    ex_val = Expense1.query.order_by(Expense1.date)
    return render_template("detail.html", expenses=expenses, ex_val=ex_val)


global ampount1 

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ampount1 = None;
    if request.method == 'POST':
        file= None
        try: 
            file = request.files['file']        
            filename = 'image.jpg'  # change this to the desired name for the image
            file.save(filename)
            image='image.jpg'
            ampount1= int(ocr.ocro(image))
            print(ampount1)
            return render_template("create.html", ampount1=ampount1)
        except:        
            return user_create()
        # print(ocr.ocro(image))
        # return f"Image uploaded and saved as {filename}!"
        
        # return redirect('/expenses/addexp',ampount1=ampount1)

    return render_template("upload.html")





#Query data

# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username))
#     return render_template("list.html", users=users)

# @app.route("/users/create", methods=["GET", "POST"])
# def user_create():
#     if request.method == "POST":
#         user = User(
#             username=request.form["username"],
#             email=request.form["email"],
#         )
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for("index", id=user.id))
#     return render_template("create.html")

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("detail.html", user=user)

# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
#     user = db.get_or_404(User, id)

#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))

#     return render_template("delete.html", user=user)

@app.route("/articles")
def user_detail():
    return render_template("articles.html")


headings=("Amt(₹)", "Category", "Payee","Mode of Payment", "Date")

    

data=( 
      (),
      )



@app.route("/", methods=["GET", "POST"])
def hello_world():
    ex_val = Expense1.query.order_by(Expense1.date)
    ex_amt= Expense1.query.with_entities(Expense1.ampount, Expense1.date).group_by(Expense1.id).order_by(Expense1.id).all()
    
    ex_amt2=[]
    ex_date=[]
    for total,_ in ex_amt:
        ex_amt2.append(total)
        ex_date.append(_)
    
    return render_template('index.html', headings=headings, data= data, ex_val=ex_val, 
                           ex_amts=json.dumps(ex_amt2),ex_dates=json.dumps(ex_date) )  


@app.route("/services")
def services(name=None):
    return render_template('services.html', name=name)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
    
    





