from market import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=True)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def owne_it(self, item_obj):
        return item_obj.owner == self.id

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, new_passward):
        self.password_hash = bcrypt.generate_password_hash(new_passward).decode('utf-8')

    def check_password(self, aword):
        return bcrypt.check_password_hash(self.password_hash, aword)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{str(self.budget)}$"


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1222), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
