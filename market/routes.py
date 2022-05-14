from market import app, db
from market.dbmodels import Item, User
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=["POST", "GET"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()

    if request.method == "POST":
        # Purchase Item Logic
        purchase_item = request.form.get('purchased_item')
        p_itm_object = Item.query.filter_by(name=purchase_item).first()

        if p_itm_object:
            if current_user.can_purchase(p_itm_object):
                p_itm_object.buy(current_user)
                flash(f"You buy {p_itm_object.name} for {p_itm_object.price}$",
                      category='success')
            else:
                flash(f"lower budget than should", category='danger')

        # Sell Item Logic
        sell_item = request.form.get('sold_item')
        s_itm_object = Item.query.filter_by(name=sell_item).first()

        if s_itm_object:
            if current_user.owne_it(s_itm_object):
                s_itm_object.sell(current_user)
                flash(f"You sell {s_itm_object.name} for {s_itm_object.price}$",
                      category='success')
            else:
                flash(f"Something wrong while sell{s_itm_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template('market.html',
                               items=items,
                               owned_items=owned_items,
                               purchase_form=purchase_form,
                               sell_form=sell_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user2create = User(username=form.username.data,
                           email=form.email.data,
                           password=form.password1.data)

        db.session.add(user2create)
        db.session.commit()

        login_user(user2create)
        flash(f"Successful, user {user2create.username} created", category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}:
        for eer_msg in form.errors.values():
            flash(eer_msg, category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data)
        print(attempted_user)
        if attempted_user:
            attempted_user = attempted_user.first()

            if attempted_user and attempted_user.check_password(
                    form.password.data):

                login_user(attempted_user)
                flash(f"Successful, login with user {attempted_user.username}", category='success')
                return redirect(url_for('market_page'))
            else:
                flash('username and password aren\'t match! ', category='danger')

        else:
            flash('User name not exact !', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('you have been logout', category='info')
    return redirect(url_for('home_page'))
