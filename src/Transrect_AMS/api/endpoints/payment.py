from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash, redirect, url_for, session, jsonify
from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.transaction_model import Transaction
from src.Transrect_AMS.database.inbox_model import Inbox
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Optional
from flask_wtf import FlaskForm

PAYMENT_API = Namespace('money', description='payment page')


class PaymentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = FloatField('Amount', validators=[
                        DataRequired()], render_kw={"readonly": True})
    upi_transaction_id = StringField(
        'UPI Transaction ID')
    location = StringField('Location', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[
        ('googlepay', 'Google Pay'),
        ('cod', 'Cash on Delivery')
    ], validators=[DataRequired()])

    machine_id = HiddenField('Machine ID')
    machine_name = HiddenField('Machine Name')
    machine_price = HiddenField('Machine Price')
    machine_quantities = HiddenField('Machine Quantities')
    machine_names = HiddenField('Machine Names')

    submit = SubmitField('Pay Now')

    def update_validators(self, payment_method):
        """ Dynamically update validators based on payment method """
        if payment_method == "googlepay":
            self.upi_transaction_id.validators = [DataRequired()]
        else:
            self.upi_transaction_id.validators = [Optional()]


@PAYMENT_API.route('/payment/', methods=['GET', 'POST'])
class Payment(Resource):
    def get(self):
        form = PaymentForm()

        machine_id = request.args.get('machine_id')
        machine_name = request.args.get('machine_name')
        machine_price = request.args.get('machine_price')
        machine_names = request.args.get('machine_names')
        machine_quantities = request.args.get('machine_quantities')

        if machine_id:
            form.machine_id.data = machine_id
        if machine_name:
            form.machine_name.data = machine_name
        if machine_price:
            form.machine_price.data = machine_price
            form.amount.data = machine_price

        if machine_names:
            form.machine_names.data = machine_names
        if machine_quantities:
            form.machine_quantities.data = machine_quantities

        machine_list = []
        if machine_names and machine_quantities:
            name_list = machine_names.split(",")
            quantity_list = machine_quantities.split(
                ",")
            if len(name_list) == len(quantity_list):
                machine_list = [{"name": name, "quantity": int(
                    quantity)} for name, quantity in zip(name_list, quantity_list)]

        print("m list", machine_list)
        return make_response(render_template('payment.html', form=form,
                                             machine_id=machine_id,
                                             machine_name=machine_name,
                                             machine_price=machine_price))

    def post(self):
        form = PaymentForm()
        form.update_validators(form.payment_method.data)
        m = form.payment_method.data
        tr_id = form.upi_transaction_id.data
        if (m == 'cod'):
            tr_id = 'COD- N/A'
        machine_id = request.form.get('machine_id')
        machine_name = request.form.get('machine_name')
        machine_price = request.form.get('machine_price')
        machine_names = request.form.get('machine_names')
        machine_quantities = request.form.get('machine_quantities')

        machine_list = []
        if machine_names and machine_quantities:
            name_list = machine_names.split(",")
            quantity_list = machine_quantities.split(
                ",")

            if len(name_list) == len(quantity_list):
                machine_list = [{"name": name, "quantity": int(
                    quantity)} for name, quantity in zip(name_list, quantity_list)]

        machine_details = ", ".join(
            [f"{item['name']} (Qty: {item['quantity']})" for item in machine_list])
        print("machine details: ", machine_details)

        if not machine_price:
            estimated_amount_value = None
        else:
            estimated_amount_value = float(
                machine_price)

        if form.validate_on_submit():
            print(machine_price)
            new_message = Inbox(
                sender_name=form.name.data,
                receiver_name="System",
                text="Payment received. Awaiting confirmation.",
                details=f"Transaction ID: {tr_id}, Amount: {form.amount.data}, Machine: {machine_details}",
                location=form.location.data,
                payment_confirmation=True,
                machine_name=machine_name,
                estimated_amount=estimated_amount_value
            )
            user_reg = form.name.data
            db.session.add(new_message)
            db.session.commit()
            flash("Payment request sent for approval.", "info")
            return redirect(url_for('log.communication_main', user_n=user_reg))

        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field.capitalize()}: {error}", "error")

        return make_response(render_template('payment.html', form=form,
                                             machine_id=machine_id,
                                             machine_name=machine_name,
                                             machine_price=machine_price))


@PAYMENT_API.route('/update_payment_validation/', methods=['POST'])
class UpdatePaymentValidation(Resource):
    """ API to dynamically update form validation based on payment method selection """

    def post(self):
        data = request.get_json()
        payment_method = data.get("payment_method")

        form = PaymentForm()
        form.update_validators(payment_method)

        return jsonify({"message": "Validation updated", "payment_method": payment_method})
