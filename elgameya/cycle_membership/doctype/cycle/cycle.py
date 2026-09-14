# Copyright (c) 2026, ElGameya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, add_months, cint, getdate

from elgameya.utils.validations import validate_child_table_duplicates


class Cycle(Document):
	def validate(self):
		self.validate_seats()
		self.set_end_date()
		self.set_seat_counts()

	def before_submit(self):
		self.validate_fully_subscribed()
		self.validate_no_pending_requests()
		self.status = "Active"

	def on_cancel(self):
		self.status = "Cancelled"

	def validate_seats(self):
		"""Enforce seat rules: seat exists in the cycle, one client per seat, no duplicate requests."""
		for row in self.cycle_members:
			if not row.seat_number:
				continue

			seat_number = cint(row.seat_number)
			if seat_number < 1 or seat_number > cint(self.number_of_seats):
				frappe.throw(
					_("Row {idx}: Seat {seat} does not exist in a cycle of {total} seats.").format(
						idx=row.idx, seat=row.seat_number, total=self.number_of_seats
					),
					title=_("Invalid Seat"),
				)

		validate_child_table_duplicates(self, child_doctype="Cycle Member", unique_fields=("seat_number",))
		validate_child_table_duplicates(self, child_doctype="Cycle Member", unique_fields=("client",))

	def validate_fully_subscribed(self):
		"""A cycle can only start once every seat is filled - the monthly payout depends on it."""
		
		if self.available_seats:
			frappe.throw(
				_(
					"Cannot submit {0}: {1} seat(s) are still available. "
					"Fill all seats before starting the cycle."
				).format(frappe.bold(self.name), self.available_seats),
				title=_("Cycle Not Fully Subscribed"),
			)

	def validate_no_pending_requests(self):
		"""Every join request must be resolved before the member list is locked in by submission."""
		pending_rows = [row.idx for row in self.cycle_members if row.status == "Pending"]
		if pending_rows:
			frappe.throw(
				_("Cannot submit {0}: Row(s) {1} are still Pending. Approve or reject them first.").format(
					frappe.bold(self.name), ", ".join(str(idx) for idx in pending_rows)
				),
				title=_("Pending Join Requests"),
			)
			
	def set_end_date(self):
		"""Derive `end_date` as `duration` full calendar months from `start_date`."""
		if self.start_date and self.duration:
			self.end_date = add_days(add_months(getdate(self.start_date), cint(self.duration)), -1)

	def set_seat_counts(self):
		"""Recalculate `joined_seats` and `available_seats` from seats already taken."""
		self.joined_seats = len(self.get_taken_seat_numbers())
		self.available_seats = cint(self.number_of_seats) - self.joined_seats

	def get_taken_seat_numbers(self):
		"""Return the seat numbers already assigned in `cycle_members`."""
		return {cint(row.seat_number) for row in self.cycle_members if row.seat_number}

	@frappe.whitelist()
	def get_available_seat_numbers(self):
		"""Return the seat numbers not yet taken in `cycle_members`, for seat selection."""
		taken_seats = self.get_taken_seat_numbers()
		return [seat for seat in range(1, cint(self.number_of_seats) + 1) if seat not in taken_seats]
