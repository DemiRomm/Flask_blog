from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' %self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(author=author, title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/blog')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create.html')


@app.route('/blog/<int:id>/edit', methods=['POST', 'GET'])
def post_edit(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.author = request.form['author']
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']


        try:
            db.session.commit()
            return redirect('/blog')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        article =Article.query.get(id)
        return render_template('post_edit.html', article=article)

@app.route('/blog')
def blog():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('blog.html', articles=articles)


@app.route('/blog/<int:id>')
def post(id):
    article = Article.query.get(id)
    return render_template('post.html', article=article)

@app.route('/blog/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/blog')

    except:
        return 'При удалении статьи произошла ошибка'


if __name__ == '__main__':
    app.run(debug=True)
