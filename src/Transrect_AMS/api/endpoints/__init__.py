from flask import Blueprint
from flask_restx import Api

from src.Transrect_AMS.api.endpoints.login import LOGIN_API
from src.Transrect_AMS.api.endpoints.services import SERVICE_API
from src.Transrect_AMS.api.endpoints.admin import ADMIN_API
from src.Transrect_AMS.api.endpoints.contact import CONTACT_API
from src.Transrect_AMS.api.endpoints.transaction import TRANSACTION_API
from src.Transrect_AMS.api.endpoints.payment import PAYMENT_API
from src.Transrect_AMS.api.endpoints.machines import MACHINE_API
from src.Transrect_AMS.api.endpoints.inventory import INVENTORY_API
from src.Transrect_AMS.api.endpoints.inbox import INBOX_API
from src.Transrect_AMS.api.endpoints.status import STATUS_API
from src.Transrect_AMS.api.endpoints.maintainance import MAINTAIN_API


AUTH_BLUEPRINT = Blueprint('log', __name__)


API = Api(AUTH_BLUEPRINT)

API.add_namespace(LOGIN_API)
API.add_namespace(SERVICE_API)
API.add_namespace(ADMIN_API)
API.add_namespace(CONTACT_API)
API.add_namespace(TRANSACTION_API)
API.add_namespace(PAYMENT_API)
API.add_namespace(MACHINE_API)
API.add_namespace(INVENTORY_API)
API.add_namespace(INBOX_API)
API.add_namespace(STATUS_API)
API.add_namespace(MAINTAIN_API)
