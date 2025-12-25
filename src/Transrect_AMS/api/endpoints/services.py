from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, flash
import requests

SERVICE_API = Namespace('special', description='service page')


@SERVICE_API.route('/services/<int:id>', methods=['GET', 'POST'])
class Service(Resource):
    def get(self, id):
        npoint_url = "https://api.npoint.io/2b0ecb1504cd1f27c242"
        response = requests.get(npoint_url)
        all_services = response.json()
        return make_response(render_template('./service-details.html', desc=all_services[id-1]))
