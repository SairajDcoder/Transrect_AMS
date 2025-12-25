import math
from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.inbox_model import Inbox
from src.Transrect_AMS.database.transaction_model import Transaction
from src.Transrect_AMS.database.mech_info_model import MachineInfo, MachinePartsInfo
from src.Transrect_AMS.database.machine_model import Machine, Part
from src.Transrect_AMS.database.machine_service import MachineService
from datetime import datetime
import re

from dateutil.relativedelta import relativedelta

INBOX_API = Namespace('msg', description='Inbox page')


class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


@INBOX_API.route('/user_inbox', methods=['GET', 'POST'])
class Userinbox(Resource):
    def get(self):
        form = SearchForm()
        search_query = request.form.get('search_query', "").strip().lower()
        page = request.args.get('page', 1, type=int)
        messages_per_page = 5

        print(f"Search Query: {search_query}")

        query = Inbox.query
        username = session.get('username', '').lower()
        username_variations = {
            "sai3606t": ["sai3606t", "sairaj", "sairaj patil"]
        }

        valid_usernames = username_variations.get(username, [username])

        query = Inbox.query.filter(
            db.or_(
                *[Inbox.receiver_name.ilike(f"%{name}%") for name in valid_usernames])
        )

        print("Filtered Query for usernames:", valid_usernames)

        if search_query:
            query = query.filter(
                (Inbox.sender_name.ilike(f"%{search_query}%")) |
                (Inbox.text.ilike(f"%{search_query}%")) |
                (Inbox.details.ilike(f"%{search_query}%"))
            )

        paginated_messages = query.paginate(
            page=page, per_page=messages_per_page, error_out=False)

        return make_response(render_template(
            'user_inbox.html',
            form=form,
            messages=paginated_messages.items,
            page=paginated_messages.page,
            total_pages=paginated_messages.pages
        ))

    def post(self):
        form = SearchForm()
        search_query = request.form.get('search_query', "").strip().lower()
        page = request.args.get('page', 1, type=int)
        messages_per_page = 5

        print(f"Search Query: {search_query}")

        query = Inbox.query
        username = session.get('username', '').lower()
        username_variations = {
            "sai3606t": ["sai3606t", "sairaj", "sairaj patil"]
        }

        valid_usernames = username_variations.get(username, [username])

        query = Inbox.query.filter(
            db.or_(
                *[Inbox.receiver_name.ilike(f"%{name}%") for name in valid_usernames])
        )

        print("Filtered Query for usernames:", valid_usernames)

        if search_query:
            query = query.filter(
                (Inbox.sender_name.ilike(f"%{search_query}%")) |
                (Inbox.text.ilike(f"%{search_query}%")) |
                (Inbox.details.ilike(f"%{search_query}%"))
            )

        paginated_messages = query.paginate(
            page=page, per_page=messages_per_page, error_out=False)

        return make_response(render_template(
            'user_inbox.html',
            form=form,
            messages=paginated_messages.items,
            page=paginated_messages.page,
            total_pages=paginated_messages.pages
        ))


@INBOX_API.route('/inbox', methods=['GET', 'POST'])
class InboxAPI(Resource):
    def get(self):
        form = SearchForm()
        search_query = request.args.get('search_query', "").strip().lower()
        page = request.args.get('page', 1, type=int)
        messages_per_page = 5

        query = Inbox.query
        if search_query:
            query = query.filter(
                (Inbox.sender_name.ilike(f"%{search_query}%")) |
                (Inbox.text.ilike(f"%{search_query}%")) |
                (Inbox.details.ilike(f"%{search_query}%")) |
                (Inbox.receiver_name.ilike(f"%{search_query}%"))
            )

        paginated_messages = query.paginate(
            page=page, per_page=messages_per_page, error_out=False)

        return make_response(render_template(
            'admin/inbox.html',
            form=form,
            messages=paginated_messages.items,
            page=paginated_messages.page,
            total_pages=paginated_messages.pages
        ))

    def post(self):
        form = SearchForm()
        search_query = form.search_query.data.strip(
        ).lower() if form.validate_on_submit() else ""
        page = request.args.get('page', 1, type=int)
        messages_per_page = 5

        query = Inbox.query
        if search_query:
            query = query.filter(
                (Inbox.sender_name.ilike(f"%{search_query}%")) |
                (Inbox.text.ilike(f"%{search_query}%")) |
                (Inbox.details.ilike(f"%{search_query}%")) |
                (Inbox.receiver_name.ilike(f"%{search_query}%"))
            )

        paginated_messages = query.paginate(
            page=page, per_page=messages_per_page, error_out=False)

        return make_response(render_template(
            'admin/inbox.html',
            form=form,
            messages=paginated_messages.items,
            page=paginated_messages.page,
            total_pages=paginated_messages.pages
        ))


@INBOX_API.route('/mark_read/<int:message_id>', methods=['POST'])
class MarkRead(Resource):
    def post(self, message_id):
        message = Inbox.query.get_or_404(message_id)
        message.unread = False
        db.session.commit()

        page = request.args.get('page', 1, type=int)

        if (session.get('email') == 'transrectsalesandservices@gmail.com'):
            return redirect(url_for('log.msg_inbox_api', page=page))
        else:
            return redirect(url_for('log.msg_userinbox', page=page))


@INBOX_API.route('/delete/<int:message_id>', methods=['POST'])
class DeleteMessage(Resource):
    def post(self, message_id):
        message = Inbox.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()

        page = request.args.get('page', 1, type=int)

        if (session.get('email') == 'transrectsalesandservices@gmail.com'):
            flash("Message deleted successfully.", "success")
            return redirect(url_for('log.msg_inbox_api', page=page))
        else:
            flash("Message deleted successfully.", "success")
            return redirect(url_for('log.msg_userinbox', page=page))


@INBOX_API.route('/confirm_payment/<int:message_id>', methods=['POST'])
class ConfirmPayment(Resource):
    def post(self, message_id):
        message = Inbox.query.get_or_404(message_id)
        c_user = message.sender_name

        details = message.details.split(", ")
        transaction_id = details[0].split(": ")[1]
        print("hello transaction id: " + transaction_id)
        amount = float(details[1].split(": ")[1])

        if ": " in details[2]:
            machine_details = details[2].split(
                ": ", 1)[1]
        else:
            machine_details = details[2]

        print("details: ", details)
        machine_list = [item.replace("Machine: ", "")
                        for item in details if "Qty:" in item]

        print("machinee list: ", machine_list)
        parsed_machines = []
        for machine_info in machine_list:
            try:
                match = re.match(r"^(.*) \(Qty: (\d+)\)$",
                                 machine_info.strip())
                if match:
                    name, qty = match.groups()
                    qty = int(qty)
                else:
                    name, qty = machine_info.strip(), 1

                parsed_machines.append({"name": name, "quantity": qty})

            except ValueError:
                flash(
                    f"Invalid machine quantity format: {machine_info}", "danger")
                return redirect(url_for('log.msg_inbox_api'))

        print(f"Parsed machines: {parsed_machines}")
        print("nice one: " + transaction_id)
        for machine in parsed_machines:
            machine_info = MachineInfo.query.filter_by(
                name=machine["name"]).first()
            if not machine_info:
                flash(
                    f"Machine information not found for {machine['name']}!", "danger")
                return redirect(url_for('log.msg_inbox_api'))

            for _ in range(machine["quantity"]):
                last_machine = Machine.query.order_by(
                    Machine.id.desc()).first()
                next_id = (last_machine.id + 1) if last_machine else 1
                new_machine = Machine(
                    name=f"{machine_info.name} - {next_id} - {message.sender_name}",
                    purchase_date=datetime.utcnow().date(),
                    lifespan=machine_info.lifespan,
                    image=machine_info.image
                )
                db.session.add(new_machine)
                db.session.flush()

                parts_info = MachinePartsInfo.query.filter_by(
                    machine_info_id=machine_info.id).all()
                for part in parts_info:
                    new_part = Part(
                        machine_id=new_machine.id,
                        name=part.name,
                        purchase_date=new_machine.purchase_date,
                        lifespan=part.lifespan
                    )
                    db.session.add(new_part)

                next_svc = new_machine.purchase_date + \
                    relativedelta(months=new_machine.lifespan)
                db.session.add(MachineService(
                    machine_id=new_machine.id,
                    last_service=new_machine.purchase_date,
                    next_service=next_svc
                ))

        db.session.delete(message)
        db.session.commit()

        # last_transaction = Transaction.query.order_by(
        #     Transaction.id.desc()).first()
        # print("\nniceone:" + transaction_id)
        # # transaction_id = f"{last_transaction.id + 1}-N/A (COD)" if last_transaction else ""

        # new_transaction = Transaction(
        #     transaction_id=transaction_id,
        #     amount=amount,
        #     account=message.sender_name,
        #     location=message.location,
        #     machine_name=", ".join([m["name"] for m in parsed_machines]),
        #     estimated_amount=message.estimated_amount or 0
        # )
        # db.session.add(new_transaction)
        # db.session.commit()

        # if transaction_id == "":
        #     new_transaction.transaction_id = f"{new_transaction.id}-N/A (COD)"
        #     db.session.commit()

        # First, create transaction without transaction_id so we get the primary key
        print("bada acha bacha haih tuuuuuuuuuuuuuuuuuuuu")
        new_transaction = Transaction(
            transaction_id=None,   # leave empty until we get id
            amount=amount,
            account=message.sender_name,
            location=message.location,
            machine_name=", ".join([m["name"] for m in parsed_machines]),
            estimated_amount=message.estimated_amount or 0
        )

        db.session.add(new_transaction)
        db.session.flush()  # get new_transaction.id without committing yet

        # If COD, generate unique transaction_id using the new primary key
        print("transaction id: " + transaction_id)
        print(type(transaction_id))
        # if transaction_id.isdigit():
        #     new_transaction.transaction_id = transaction_id
        # if new_transaction.transaction_id is None or new_transaction.transaction_id == "":
        #     new_transaction.transaction_id = f"{new_transaction.id}-N/A (COD)"
        #     print("teri maa ki chuuuuuu..............." +
        #           new_transaction.transaction_id)
        # Case 1: COD → no real transaction_id, generate custom one
        if "COD" in transaction_id.upper():
            # COD payment, generate COD-style transaction_id
            new_transaction.transaction_id = f"{new_transaction.id}-N/A (COD)"
        else:
            # real transaction_id from GPAY or other method
            new_transaction.transaction_id = transaction_id

        db.session.commit()

        #
        #

        acceptance_message = Inbox(
            sender_name="System",
            receiver_name=c_user,
            text="Payment Accepted",
            details=f"Transaction ID: {new_transaction.transaction_id} has been accepted.",
            location=message.location,
            payment_confirmation=False,
            machine_name=", ".join([m["name"] for m in parsed_machines]),
            estimated_amount=message.estimated_amount
        )
        db.session.add(acceptance_message)

        db.session.commit()

        page = request.args.get('page', 1, type=int)

        flash("Payment confirmed and transaction recorded.", "success")
        return redirect(url_for('log.msg_inbox_api', page=page))

# @INBOX_API.route('/confirm_payment/<int:message_id>', methods=['POST'])
# class ConfirmPayment(Resource):
#     def post(self, message_id):
#         message = Inbox.query.get_or_404(message_id)
#         c_user = message.sender_name

#         # Parse details from message
#         details = message.details.split(", ")
#         transaction_id = details[0].split(": ")[1].strip()
#         amount = float(details[1].split(": ")[1])

#         machine_list = [item.replace("Machine: ", "")
#                         for item in details if "Qty:" in item]
#         parsed_machines = []

#         for machine_info in machine_list:
#             match = re.match(r"^(.*) \(Qty: (\d+)\)$", machine_info.strip())
#             if match:
#                 name, qty = match.groups()
#                 qty = int(qty)
#             else:
#                 name, qty = machine_info.strip(), 1
#             parsed_machines.append({"name": name, "quantity": qty})

#         # Insert machines and their parts/services
#         for machine in parsed_machines:
#             machine_info = MachineInfo.query.filter_by(
#                 name=machine["name"]).first()
#             if not machine_info:
#                 flash(
#                     f"Machine information not found for {machine['name']}!", "danger")
#                 return redirect(url_for('log.msg_inbox_api'))

#             for _ in range(machine["quantity"]):
#                 new_machine = Machine(
#                     name=f"{machine_info.name} - 0 - {message.sender_name}",
#                     purchase_date=datetime.utcnow().date(),
#                     lifespan=machine_info.lifespan,
#                     image=machine_info.image
#                 )
#                 db.session.add(new_machine)
#                 db.session.flush()  # assign ID

#                 # Set machine name with ID
#                 new_machine.name = f"{machine_info.name} - {new_machine.id} - {message.sender_name}"

#                 # Add parts
#                 parts_info = MachinePartsInfo.query.filter_by(
#                     machine_info_id=machine_info.id).all()
#                 for part in parts_info:
#                     db.session.add(Part(
#                         machine_id=new_machine.id,
#                         name=part.name,
#                         purchase_date=new_machine.purchase_date,
#                         lifespan=part.lifespan
#                     ))

#                 # Add machine service
#                 next_svc = new_machine.purchase_date + \
#                     relativedelta(months=new_machine.lifespan)
#                 db.session.add(MachineService(
#                     machine_id=new_machine.id,
#                     last_service=new_machine.purchase_date,
#                     next_service=next_svc
#                 ))

#         # Remove the processed message
#         db.session.delete(message)

#         # Generate unique transaction_id for COD if empty
#         if not transaction_id:
#             last_transaction = Transaction.query.order_by(
#                 Transaction.id.desc()).first()
#             next_id = last_transaction.id + 1 if last_transaction else 1
#             transaction_id = f"{next_id}-N/A (COD)"

#         # Insert transaction
#         new_transaction = Transaction(
#             transaction_id=transaction_id,
#             amount=amount,
#             account=message.sender_name,
#             location=message.location,
#             machine_name=", ".join([m["name"] for m in parsed_machines]),
#             estimated_amount=message.estimated_amount or 0
#         )
#         db.session.add(new_transaction)
#         db.session.commit()

#         # Send acceptance message
#         acceptance_message = Inbox(
#             sender_name="System",
#             receiver_name=c_user,
#             text="Payment Accepted",
#             details=f"Transaction ID: {new_transaction.transaction_id} has been accepted.",
#             location=message.location,
#             payment_confirmation=False,
#             machine_name=", ".join([m["name"] for m in parsed_machines]),
#             estimated_amount=message.estimated_amount
#         )
#         db.session.add(acceptance_message)
#         db.session.commit()

#         flash("Payment confirmed and transaction recorded.", "success")
#         page = request.args.get('page', 1, type=int)
#         return redirect(url_for('log.msg_inbox_api', page=page))


@INBOX_API.route('/reject_payment/<int:message_id>', methods=['POST'])
class RejectPayment(Resource):
    def post(self, message_id):
        message = Inbox.query.get_or_404(message_id)
        c_user = message.sender_name

        details = message.details.split(", ")
        transaction_id = details[0].split(": ")[1]

        rejection_message = Inbox(
            sender_name="System",
            receiver_name=c_user,
            text="Payment Rejected",
            details=f"Transaction ID: {transaction_id} has been canceled.",
            location=message.location,
            payment_confirmation=False,
            machine_name=message.machine_name,
            estimated_amount=message.estimated_amount or 0
        )
        db.session.add(rejection_message)

        db.session.delete(message)
        db.session.commit()
        page = request.args.get('page', 1, type=int)

        flash("Payment rejected. Notification sent.", "reject")
        return redirect(url_for('log.msg_inbox_api', page=page))
