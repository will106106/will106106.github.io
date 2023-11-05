from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tips.db'  # Ensure this points to your desired database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tip(db.Model):
    __tablename__ = 'tips'  # Optional: specify a custom table name
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(80), nullable=False)
    tip_amount = db.Column(db.Float, nullable=False)  # Use Float for monetary values
    tip_out_to = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Tip {self.id}>"

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server_name = request.form['serverName']
        tip_amount = float(request.form['tipAmount'])  # Convert string to float
        tip_out_to = request.form['tipOutTo']

        new_tip = Tip(server_name=server_name, tip_amount=tip_amount, tip_out_to=tip_out_to)
        db.session.add(new_tip)
        db.session.commit()

        return redirect(url_for('index'))
    
    tips = Tip.query.all()
    return render_template('index.html', tips=tips)

if __name__ == '__main__':
    app.run(debug=True)