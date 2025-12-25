from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, session
from datetime import datetime
from src.Transrect_AMS.database.machine_model import Machine, Part

STATUS_API = Namespace('stat', description='Machines status page')


def calculate_remaining_lifespan(purchase_date, lifespan_years):
    """Calculates remaining lifespan percentage."""
    purchase_date = datetime.strptime(
        purchase_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
    current_date = datetime.now()
    elapsed_years = (current_date - purchase_date).days / 365.0
    remaining_years = max(lifespan_years - elapsed_years, 0)
    return round((remaining_years / lifespan_years) * 100)


def show_machine_details(machine):
    """Generates HTML to display machine details."""
    image_url = f"/static/{machine.image}"

    html = f"<h3>{machine.name}</h3>"
    html += f'<img src="{image_url}" alt="{machine.name}" width="200px">\n'
    html += f'<p>Purchased on: {machine.purchase_date}</p>\n'
    html += f'<p>Lifespan: {machine.lifespan} years</p>\n'

    lifespan_percentage = calculate_remaining_lifespan(
        machine.purchase_date, machine.lifespan)
    html += f'<div class="progress-container">\n'
    html += f'    <div class="progress-bar" style="width:{lifespan_percentage}%">{round(lifespan_percentage)}%</div>\n'
    html += f'</div>\n'

    html += "<h4>Parts:</h4>\n<ul class='ul_this'>\n"
    for part in machine.parts:
        part_lifespan_percentage = calculate_remaining_lifespan(
            part.purchase_date, part.lifespan)
        html += f'    <li class="li_this">{part.name} - Purchased: {part.purchase_date}, Lifespan: {part.lifespan} years\n'
        html += f'        <div class="progress-container">\n'
        html += f'            <div class="progress-bar" style="width:{part_lifespan_percentage}%">{round(part_lifespan_percentage)}%</div>\n'
        html += f'        </div>\n'
        html += f'    </li>\n'
    html += "</ul>\n"

    return html


@STATUS_API.route('/status/<int:index>', methods=['GET'])
class Status(Resource):
    def get(self, index):
        machines = Machine.query.all()
        if 0 <= index < len(machines):
            machine = machines[index]
            machine_details_html = show_machine_details(machine)
            return make_response(render_template(
                'admin/machine.html',
                machines=enumerate(machines),
                calculate_remaining_lifespan=calculate_remaining_lifespan,
                machine_details_html=machine_details_html
            ))
        return "Machine not found", 404


@STATUS_API.route('/stat', methods=['GET'])
class Stat(Resource):
    def get(self):
        return make_response(render_template(
            'admin/machine.html',
            machines=enumerate(Machine.query.all()),
            calculate_remaining_lifespan=calculate_remaining_lifespan,
            machine_details_html=None
        ))


@STATUS_API.route('/user_status/<int:index>', methods=['GET'])
class UserStatus(Resource):
    def get(self, index):
        username = session.get("username")
        if not username:
            return "Unauthorized", 401

        username = username.lower()

        username_variations = {
            "sai3606t": ["sai3606t", "sairaj", "sairaj patil"]
        }

        valid_usernames = username_variations.get(username, [username])

        def is_substring_match(str1, str2):
            if not str1 or not str2:
                return False
            return str1 in str2 or str2 in str1

        def extract_username(machine_name):
            """Extracts username from machine name after the last '-'"""
            if not machine_name:
                return ""

            parts = machine_name.rsplit('-', 1)
            extracted = parts[-1].strip() if len(parts) > 1 else ""
            return extracted.lower()

        user_machines = [
            machine for machine in Machine.query.all()
            if any(is_substring_match(extract_username(machine.name), valid) for valid in valid_usernames)
        ]

        if 0 <= index < len(user_machines):
            machine = user_machines[index]
            machine_details_html = show_machine_details(machine)
            return make_response(render_template(
                'user_machine.html',
                machines=enumerate(user_machines),
                calculate_remaining_lifespan=calculate_remaining_lifespan,
                machine_details_html=machine_details_html
            ))
        return "Machine not found", 404


@STATUS_API.route('/user_stat', methods=['GET'])
class UserStat(Resource):
    def get(self):

        username = session.get("username")
        if not username:
            return "Unauthorized", 401

        username = username.lower()

        username_variations = {
            "sai3606t": ["sai3606t", "sairaj", "sairaj patil"]
        }

        valid_usernames = username_variations.get(username, [username])

        def is_substring_match(str1, str2):
            if not str1 or not str2:
                return False
            return str1 in str2 or str2 in str1

        def extract_username(machine_name):
            """Extracts username from machine name after the last '-'"""
            if not machine_name:
                return ""
            parts = machine_name.rsplit('-', 1)
            extracted = parts[-1].strip() if len(parts) > 1 else ""
            return extracted.lower()

        user_machines = [
            machine for machine in Machine.query.all()
            if any(is_substring_match(extract_username(machine.name), valid) for valid in valid_usernames)
        ]
        return make_response(render_template(
            'user_machine.html',
            machines=enumerate(user_machines),
            calculate_remaining_lifespan=calculate_remaining_lifespan,
            machine_details_html=None
        ))
