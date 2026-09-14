# Copyright (c) 2026, ElGameya and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"fieldname": "cycle", "label": _("Cycle"), "fieldtype": "Link", "options": "Cycle", "width": 150},
		{"fieldname": "cycle_status", "label": _("Cycle Status"), "fieldtype": "Data", "width": 150},
		{"fieldname": "start_date", "label": _("Start Date"), "fieldtype": "Date", "width": 150},
		{"fieldname": "end_date", "label": _("End Date"), "fieldtype": "Date", "width": 100},
		{"fieldname": "number_of_seats", "label": _("Seats"), "fieldtype": "Int", "width": 70},
		{"fieldname": "joined_seats", "label": _("Joined"), "fieldtype": "Int", "width": 70},
		{"fieldname": "available_seats", "label": _("Available"), "fieldtype": "Int", "width": 150},
		{"fieldname": "seat_number", "label": _("Seat #"), "fieldtype": "Data", "width": 70},
		{"fieldname": "client", "label": _("Client"), "fieldtype": "Link", "options": "Client", "width": 140},
		{"fieldname": "client_name", "label": _("Client Name"), "fieldtype": "Data", "width": 160},
		{"fieldname": "join_date", "label": _("Join Date"), "fieldtype": "Date", "width": 150},
		{"fieldname": "member_status", "label": _("Member Status"), "fieldtype": "Data", "width": 150},
	]


def get_data(filters):
	filters = frappe._dict(filters or {})

	Cycle = frappe.qb.DocType("Cycle")
	CycleMember = frappe.qb.DocType("Cycle Member")
	Client = frappe.qb.DocType("Client")

	query = (
		frappe.qb.from_(Cycle)
		.left_join(CycleMember)
		.on((CycleMember.parent == Cycle.name) & (CycleMember.parenttype == "Cycle"))
		.left_join(Client)
		.on(Client.name == CycleMember.client)
		.select(
			Cycle.name.as_("cycle"),
			Cycle.status.as_("cycle_status"),
			Cycle.start_date,
			Cycle.end_date,
			Cycle.number_of_seats,
			Cycle.joined_seats,
			Cycle.available_seats,
			CycleMember.seat_number,
			CycleMember.client,
			Client.full_name.as_("client_name"),
			CycleMember.join_date,
			CycleMember.status.as_("member_status"),
		)
		.where(Cycle.docstatus < 2)
		.orderby(Cycle.start_date, order=frappe.qb.desc)
		.orderby(CycleMember.idx)
	)

	if filters.cycle:
		query = query.where(Cycle.name == filters.cycle)

	if filters.cycle_status:
		query = query.where(Cycle.status == filters.cycle_status)

	if filters.member_status:
		query = query.where(CycleMember.status == filters.member_status)

	return query.run(as_dict=True)
