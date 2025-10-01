from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)


class Quiz(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    question_id = db.relationship('Question', backref='quiz', lazy='dynamic')

    def __repr__(self):
        return 'Quiz %r' % self.id 


class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(100))
    a = db.Column(db.String(100))
    b = db.Column(db.String(100))
    c = db.Column(db.String(100))
    correct = db.Column(db.String(100))
    id_quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    def __repr__(self):
        return 'Question %r' % self.id 


@app.route('/', methods=['GET', 'POST'])
def index():
    quiz = Quiz.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        quiz = Quiz(title=title)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html",quiz=quiz)


@app.route('/education', methods=['GET', 'POST'])
def education():
    return render_template("education.html")


@app.route('/delete-quiz/<int:id>', methods=['GET', 'POST'])
def delete_quiz(id):
    quiz = Quiz.query.get(id)
    if not quiz:
        abort(404) 
    db.session.delete(quiz)
    db.session.commit()
    return redirect('/')


@app.route('/delete-question/<int:id>/<int:id_quiz>', methods=['GET', 'POST'])
def delete_question(id,id_quiz):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("quiz", id=id_quiz))


@app.route('/quiz/<int:id>', methods=['GET', 'POST'])
def quiz(id):
    quiz = Quiz.query.get(id)
    question = Question.query.filter_by(id_quiz=id).all()
    if request.method == 'POST':
        question = request.form.get('question')
        a = request.form.get('A')
        b = request.form.get('B')
        c = request.form.get('C')
        correct = request.form.get('correct')
        question = Question(question=question,a=a,b=b,c=c,correct=correct,id_quiz=id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("quiz", id=id))
    return render_template("quiz.html",quiz=quiz,question=question)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)