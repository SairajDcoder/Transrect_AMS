from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_restx import Namespace, Resource
from wtforms.validators import DataRequired, NumberRange
from flask import request, render_template, make_response, flash, redirect, url_for, session

from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.inventory_model import Inventory

INVENTORY_API = Namespace('inventory', description='inbox page')


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField("Search")


class InventoryForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
                            DataRequired(), NumberRange(min=1)])
    amount = IntegerField('Amount', validators=[
                          DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Item')


@INVENTORY_API.route('/invent/', methods=['GET', 'POST'])
class Invent(Resource):
    def get(self):
        form = InventoryForm()
        items = Inventory.query.all()
        return make_response(render_template("admin/inventory.html", form=form, items=items))

    def post(self):
        form = InventoryForm()

        if form.validate_on_submit():
            new_item = Inventory(
                item_name=form.item_name.data,
                quantity=form.quantity.data,
                amount=form.amount.data
            )
            db.session.add(new_item)
            db.session.commit()
            flash("Item added successfully!", "success")

        return redirect(url_for('log.inventory_invent'))


@INVENTORY_API.route("/delete/<int:item_id>", methods=["POST"])
class DeleteItem(Resource):
    def post(self, item_id):
        item = Inventory.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            flash("Item deleted successfully!", "success")

        return redirect(url_for('log.inventory_invent'))
