from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash, redirect, url_for, make_response, session
from src.Transrect_AMS.api.endpoints.transaction import TransactionForm, SearchForm


ADMIN_API = Namespace('exclusive', description='admin page')


@ADMIN_API.route('/machine', methods=['GET', 'POST'])
class machine(Resource):
    def get(self):
        return make_response(render_template('./admin/machine.html'))


@ADMIN_API.route('/admin', methods=['GET', 'POST'])
class admin(Resource):
    def get(self):
        user_n = request.args.get('user_n')
        print(user_n)
        print(user_n)
        print(user_n)
        print(user_n)
        return make_response(render_template('./admin/admin.html', user_n=user_n))


@ADMIN_API.route('/delivery', methods=['GET', 'POST'])
class delivery(Resource):
    def get(self):
        return make_response(render_template('./admin/delivery.html'))


@ADMIN_API.route('/inbox', methods=['GET', 'POST'])
class inbox(Resource):
    def get(self):
        return redirect(url_for("log.msg_inbox_api"))


@ADMIN_API.route('/inventory', methods=['GET', 'POST'])
class inventory(Resource):
    def get(self):
        return make_response(render_template('./admin/inventory.html'))


@ADMIN_API.route('/maintenance/<int:id>', methods=['GET', 'POST'])
class maintenance(Resource):
    def get(self, id):
        return redirect(url_for("log.maintenance_machine_details", id=id))


@ADMIN_API.route('/transaction', methods=['GET', 'POST'])
class transaction(Resource):

    def get(self):
        return redirect(url_for("trans"))


@ADMIN_API.route('/logout', methods=['GET', 'POST'])
class logout(Resource):
    def get(self):
        from src.Transrect_AMS.api.endpoints.login import MyForm

        form = MyForm()
        session.pop('email', None)
        session.pop('keep_signed_in', None)
        session.pop('last_email', None)
        session.pop('username', None)
        return make_response(render_template('./loginhtml.html', form=form))
