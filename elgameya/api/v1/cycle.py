import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import cint, today
from elgameya.api.utils import api_error


@frappe.whitelist(methods=["POST"])
@rate_limit(key="cycle", limit=10, seconds=60)
def join_cycle(cycle, seat_number, client=None):
	client = get_requesting_client(client)
	seat_number = validate_seat_number(seat_number)
	cycle_doc = get_joinable_cycle(cycle)

	validate_seat_available(cycle_doc, seat_number)
	validate_not_already_requested(cycle_doc, client)

	cycle_doc.append(
		"cycle_members",
		{
			"client": client,
			"join_date": today(),
			"seat_number": seat_number,
			"status": "Pending",
		},
	)
	cycle_doc.save(ignore_permissions=True)
	member_row = get_cycle_member_row(cycle_doc, client) or {}
	return {
		"cycle": cycle_doc.name,
		"client": client,
		"seat_number": member_row.get("seat_number"),
		"status": member_row.get("status"),
		"row_name": member_row.get("name"),
	}


def get_requesting_client(client):
	if client:
		if "System Manager" not in frappe.get_roles():
			api_error(
				_("You are not allowed to apply a join request on behalf of another client."),
				"Perm",
			)
		if not frappe.db.exists("Client", client):
			api_error(_("Client {0} does not exist.").format(client))
		return client

	own_client = frappe.db.get_value("Client", {"user": frappe.session.user})
	if not own_client:
		api_error(_("No Client record is linked to your account. Please complete your profile first."))

	return own_client


def validate_seat_number(seat_number):
	seat_number = cint(seat_number)
	if seat_number < 1:
		api_error(_("Seat Number must be a positive number."))

	return seat_number


def get_joinable_cycle(cycle):
	if not frappe.db.exists("Cycle", cycle):
		api_error(_("Cycle {0} does not exist.").format(cycle))

	cycle_doc = frappe.get_doc("Cycle", cycle)

	if cycle_doc.docstatus != 0:
		api_error(_("Cycle {0} is not open for new join requests.").format(cycle))

	return cycle_doc

def get_cycle_member_row(cycle_doc, client):
	for row in cycle_doc.cycle_members:
		if row.client == client:
			return row
	return None

def validate_seat_available(cycle_doc, seat_number):
	if seat_number > cint(cycle_doc.number_of_seats):
		api_error(
			_("Seat {0} does not exist in a cycle of {1} seats.").format(
				seat_number, cycle_doc.number_of_seats
			)
		)

	if seat_number in cycle_doc.get_taken_seat_numbers():
		api_error(_("Seat {0} has already been taken. Please choose another seat.").format(seat_number))


def validate_not_already_requested(cycle_doc, client):
	if any(row.client == client for row in cycle_doc.cycle_members):
		api_error(_("You already have a join request for Cycle {0}.").format(cycle_doc.name))
