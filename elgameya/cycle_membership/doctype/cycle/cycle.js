// Copyright (c) 2026, ElGameya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cycle", {
	refresh(frm) {
		frm.trigger("refresh_seat_number_options");
	},
	number_of_seats(frm) {
		frm.trigger("refresh_seat_number_options");
	},
	cycle_members_add(frm) {
		frm.trigger("refresh_seat_number_options");
	},
	cycle_members_remove(frm) {
		frm.trigger("refresh_seat_number_options");
	},
	refresh_seat_number_options(frm) {
		const grid = frm.fields_dict.cycle_members.grid;
		const total_seats = cint(frm.doc.number_of_seats);
		const taken_seats = (frm.doc.cycle_members || [])
			.map((row) => cint(row.seat_number))
			.filter(Boolean);
		const free_seats = Array.from({ length: total_seats }, (_, i) => i + 1).filter(
			(seat) => !taken_seats.includes(seat)
		);
		grid.update_docfield_property("seat_number", "options", [""].concat(free_seats));

		(grid.grid_rows || []).forEach((row) => {
			const own_seat = cint(row.doc.seat_number);
			if (!own_seat) {
				return;
			}
			const docfield = row.docfields.find((d) => d.fieldname === "seat_number");
			if (docfield) {
				docfield.options = [""].concat(free_seats, own_seat);
			}
		});
	},
});

frappe.ui.form.on("Cycle Member", {
	seat_number(frm) {
		frm.trigger("refresh_seat_number_options");
	},
});
