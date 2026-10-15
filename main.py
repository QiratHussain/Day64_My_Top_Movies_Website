from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired , URL
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
class AddForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    review = StringField('review', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    year = StringField('year', validators=[DataRequired()])
    rating = StringField('rating', validators=[DataRequired()])
    img_url = StringField('img_url', validators=[DataRequired(),URL()])
    submit = SubmitField('Submit')

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[float] = mapped_column(Integer, nullable= False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movies).order_by(Movies.rating))
        all_movies = result.scalars()
        return render_template("index.html",movies_list= all_movies)

@app.route("/add",methods=['POST','GET'])
def add():
    add_form=AddForm()
    if request.method=='POST':
        with app.app_context():
            new_book = Movies(title=request.form['title'],year=request.form['year'],description=request.form['description'],rating=request.form['rating'],review=request.form['review'],img_url=request.form['img_url'])
            db.session.add(new_book)
            db.session.commit()
    return render_template("add.html", form= add_form)

@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method=='POST':
        movie_id = request.args.get('id')
        with app.app_context():
            movie_to_update = db.get_or_404(Movies, movie_id)  
            movie_to_update.rating = request.form['Rating']
            movie_to_update.review = request.form['Review']
            db.session.commit()
            return redirect(url_for('home'))
    edit_form=EditForm()
    return render_template("edit.html", form= edit_form)

@app.route("/delete")
def delete():
    pass

if __name__ == '__main__':
    app.run(debug=True)


#https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg