import os
from flask import request, Flask, render_template, redirect, url_for, jsonify, make_response
from flask_migrate import Migrate
from src.Transrect_AMS.api.endpoints import AUTH_BLUEPRINT
from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.login_model import Login
from src.Transrect_AMS.api.endpoints.contact import ContactForm
from src.Transrect_AMS.api.endpoints.transaction import TransactionForm, SearchForm, MarkReadForm
from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.transaction_model import Transaction
from src.Transrect_AMS.database.inbox_model import Inbox
from src.Transrect_AMS.database.inventory_model import Inventory
from src.Transrect_AMS.database.user_model import User
from src.Transrect_AMS.database.admin_model import Admin
from src.Transrect_AMS.api.logic_models.scheduler import init_scheduler

import requests


def create_app():
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")
    app.secret_key = "Syntax_Work"

    @app.route('/')
    def index():
        return redirect(url_for('log.account_login'))

    @app.route('/home')
    def home():
        return redirect(url_for('log.communication_main'))

    @app.route('/admin')
    def admin():
        return render_template('admin/admin.html')

    @app.route('/portfolio')
    def portfolio():
        return render_template('portfolio-details.html')

    transactions = [
        {"id": "1234", "amount": 250, "account": "John Doe", "read": False},
        {"id": "5678", "amount": 100, "account": "Jane Smith", "read": False},
        {"id": "9101", "amount": 50, "account": "Alice Brown", "read": True},
        {"id": "1121", "amount": 500, "account": "Bob Johnson", "read": False}
    ]

    @app.route('/trans', methods=["GET", "POST"])
    def trans():

        search_query = request.args.get("search", "").strip().lower()
        page = request.args.get("page", 1, type=int)
        per_page = 5

        query = Transaction.query
        if search_query:
            query = query.filter(
                Transaction.account.ilike(f"%{search_query}%"))

        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False)
        transactions = pagination.items

        return render_template(
            "admin/transaction.html",
            transactions=transactions,
            pagination=pagination,
            search_query=search_query
        )

    @app.route("/mark_read", methods=["POST"])
    def mark_read():

        transaction_id = request.form.get("transaction_id")
        transaction = Transaction.query.filter_by(
            transaction_id=transaction_id).first()

        if transaction:
            transaction.read = True
            db.session.commit()
            return jsonify({"success": True})

        return jsonify({"success": False, "error": "Transaction not found"}), 404

    psd = "sai3606"

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sai3606@localhost/TransrectDB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sairaj:lOWaQhbXVzD8KPOGQppcWlUQjXuQDaN0@dpg-d56em46uk2gs73cf70u0-a/transrectdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db, directory=os.path.join(
        "src", "Transrect_AMS", "alembic"))

    init_scheduler(app)

    app.register_blueprint(AUTH_BLUEPRINT)

    return app
