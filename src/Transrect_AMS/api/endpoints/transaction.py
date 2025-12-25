from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from flask_restx import Namespace
from wtforms.validators import DataRequired

TRANSACTION_API = Namespace('payhistory', description='transaction page')


class SearchForm(FlaskForm):
    search = StringField("Search transactions...")
    submit = SubmitField("Search")


class TransactionForm(FlaskForm):
    trans_id = HiddenField("Transaction ID")
    amount = HiddenField("Amount")
    account = HiddenField("Account Name")
    mark_read = SubmitField("Mark as Read")


class MarkReadForm(FlaskForm):
    transaction_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Mark as Read")
