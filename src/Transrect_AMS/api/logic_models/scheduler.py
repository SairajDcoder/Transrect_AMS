from flask_apscheduler import APScheduler
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from src.Transrect_AMS.database import db
from src.Transrect_AMS.database.machine_model import Machine, Part
from src.Transrect_AMS.database.machine_service import MachineService
from src.Transrect_AMS.database.inbox_model import Inbox
from flask import current_app

g_app = None
scheduler = APScheduler()


def calculate_remaining_lifespan(purchase_date, lifespan_years):
    purchase_date = datetime.combine(purchase_date, datetime.min.time())
    now = datetime.now()
    elapsed_years = (now - purchase_date).days / 365.0
    remaining_years = max(lifespan_years - elapsed_years, 0)
    return round((remaining_years / lifespan_years) * 100)


def service_rollover_job():
    """
    Runs daily.  For every MachineService whose next_service <= today:
      1. set last_service = next_service
      2. set next_service = last_service + lifespan_months
      3. optionally, notify the user that maintenance was performed
    """
    with g_app.app_context():
        today = date.today()
        due_services = MachineService.query.filter(
            MachineService.next_service <= today
        ).all()

        for svc in due_services:
            # remember old due date
            old_next = svc.next_service

            # roll dates forward
            svc.last_service = old_next
            # fetch the machine to know its lifespan interval
            machine = Machine.query.get(svc.machine_id)
            # assume your service interval = machine.lifespan months
            svc.next_service = old_next + \
                relativedelta(months=machine.lifespan)

            db.session.add(svc)

            # send an inbox notification if you like
            user = svc.machine.name.split(
                '-')[-1].strip() if '-' in svc.machine.name else svc.machine.name
            note = Inbox(
                sender_name="System",
                receiver_name=user,
                text="Maintenance completed",
                details=(
                    f"Your machine '{machine.name}' was serviced on "
                    f"{old_next.strftime('%Y-%m-%d')}. Next service due on "
                    f"{svc.next_service.strftime('%Y-%m-%d')}."
                ),
                unread=True,
                location="Automated Maintenance Scheduler",
                payment_confirmation=False,
                machine_name=machine.name,
                estimated_amount=None
            )
            db.session.add(note)

        db.session.commit()


def health_check_job():
    """
    Your existing health-check logic, unchanged.
    """
    with g_app.app_context():
        machines = Machine.query.all()
        for machine in machines:
            health = calculate_remaining_lifespan(
                machine.purchase_date, machine.lifespan)
            user = machine.name.split(
                '-')[-1].strip() if '-' in machine.name else machine.name
            if health < 10:
                db.session.add(Inbox(
                    sender_name="System",
                    receiver_name=user,
                    text="Machine Health Alert",
                    details=f"Your machine '{machine.name}' health is critically low ({health}%).",
                    unread=True,
                    location="Machine Health Monitor",
                    payment_confirmation=False,
                    machine_name=machine.name,
                    estimated_amount=None
                ))
            for part in machine.parts:
                part_health = calculate_remaining_lifespan(
                    part.purchase_date, part.lifespan)
                if part_health < 10:
                    db.session.add(Inbox(
                        sender_name="System",
                        receiver_name=user,
                        text="Part Health Alert",
                        details=(
                            f"Your part '{part.name}' in machine '{machine.name}' "
                            f"is critically low ({part_health}%)."
                        ),
                        unread=True,
                        location="Machine Health Monitor",
                        payment_confirmation=False,
                        machine_name=machine.name,
                        estimated_amount=None
                    ))
        db.session.commit()


def init_scheduler(app):
    """
    Initialize both jobs:
      - service_rollover_job: runs every day at midnight
      - health_check_job:     runs every 3 days
    """
    global g_app
    g_app = app
    scheduler.init_app(app)

    scheduler.add_job(
        id='service_rollover',
        func=service_rollover_job,
        trigger='cron',     # daily at 00:00
        hour=0, minute=0
    )
    scheduler.add_job(
        id='machine_health_check',
        func=health_check_job,
        trigger='interval',
        days=3
    )
    scheduler.start()
