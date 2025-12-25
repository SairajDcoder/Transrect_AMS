from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.machine_service import MachineService
from src.Transrect_AMS.database.machine_model import Machine

from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta

MAINTAIN_API = Namespace('maintenance', description="Machine Maintenance API")


@MAINTAIN_API.route('/machine/<int:id>')
class MachineDetails(Resource):
    def get(self, id):
        machine_obj = Machine.query.get(id)
        if not machine_obj:
            return {"message": "Machine not found"}, 404

        service_obj = MachineService.query.filter_by(machine_id=id).first()

        if not service_obj:
            last_service_date = machine_obj.purchase_date
            next_service_date = last_service_date + \
                relativedelta(months=machine_obj.lifespan)

            service_obj = MachineService(
                machine_id=id,
                last_service=last_service_date,
                next_service=next_service_date
            )
            db.session.add(service_obj)
            db.session.commit()

        last_service = service_obj.last_service.strftime('%Y-%m-%d')
        next_service = service_obj.next_service.strftime('%Y-%m-%d')

        all_machine_objs = Machine.query.order_by(Machine.id).all()
        machines = []
        for m in all_machine_objs:
            svc = MachineService.query.filter_by(machine_id=m.id).first()
            if not svc:
                last_svc_date = m.purchase_date
                next_svc_date = last_svc_date + \
                    relativedelta(months=m.lifespan)
                svc = MachineService(
                    machine_id=m.id,
                    last_service=last_svc_date,
                    next_service=next_svc_date
                )
                db.session.add(svc)
                db.session.commit()
            machines.append({
                "id": m.id,
                "name": m.name,
                "lastService": svc.last_service.strftime('%Y-%m-%d'),
                "nextService": svc.next_service.strftime('%Y-%m-%d')
            })

        index = next((i for i, m in enumerate(machines) if m["id"] == id), -1)

        return make_response(render_template(
            "admin/maintenance.html",
            machine={
                "id": machine_obj.id,
                "name": machine_obj.name,
                "lastService": last_service,
                "nextService": next_service
            },
            machines=machines,
            index=index
        ))
