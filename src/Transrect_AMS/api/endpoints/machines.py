from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash

import requests

MACHINE_API = Namespace('mech', description='machines portfolio page')


@MACHINE_API.route('/machine/<int:id>', methods=['GET', 'POST'])
class Machine(Resource):
    def get(self, id):
        npoint_url = "https://api.npoint.io/a95c45be7bea32ef1ff1"
        response = requests.get(npoint_url)
        mech_details = response.json()
        return make_response(render_template('./portfolio-details.html', desc=mech_details[id-1]))
