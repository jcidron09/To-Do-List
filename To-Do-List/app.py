import datetime

from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta, date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Entries.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(1000))
    item = db.Column(db.String(1000))
    action = db.Column(db.String(1000))
    amount = db.Column(db.Integer)


@app.route("/")
def home():
    return render_template("index.html", content=create_table())


def create_table():
    table = """
    <table class="table">
        <thead>
            <tr>
              <th scope="col">Id</th>
              <th scope="col">Date</th>
              <th scope="col">Item</th>
              <th scope="col">Action</th>
              <th scope="col">Amount</th>
            </tr>
      </thead>
        """
    row = 1
    for entry in Entry.query.all():
        table += "<tr>\n" \
                 + "<th scope=""row"">" + str(row) + "</th>\n" \
                 + "<td>" + str(entry.id) + "</td>\n" \
                 + "<td>" + entry.date + "</td>\n" + "<td>" \
                 + entry.item + "</td>\n" + "<td>" + entry.action \
                 + "</td>\n" + "<td>" + str(entry.amount) \
                 + "</td>\n" + "</tr>"
        row += 1
    table += "</tbody>\n</table>\n"
    return table


if __name__ == "__main__":
    db.create_all()
    db.session.add(Entry(date=date.today(), item="Halo Top", action="Refill", amount=1))
    db.session.commit()
    app.run(debug=True)