# Copyright (c) 2026, ElGameya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from elgameya.utils.national_id import validate_egyptian_national_id, parse_egyptian_national_id
from elgameya.utils.phone_numbers import validate_egyptian_phone, normalize_egyptian_phone

class Client(Document):
	def validate(self):
		validate_egyptian_phone(self.phone, throw=True)
		validate_egyptian_national_id(self.national_id, throw=True)
	
	def before_save(self):
		self.set_client_info_from_national_id()
		self.set_client_full_name()
		self.set_client_phone_code()

	def set_client_info_from_national_id(self):
		nid_info = parse_egyptian_national_id(self.national_id)
		if not nid_info.get('is_valid'):
			return
		self.age = int(nid_info.get("age"))
		self.gender = nid_info.get("gender")
	
	def set_client_full_name(self):
		if not self.first_name or not self.last_name:
			return
		self.full_name = f"{self.first_name} {self.middle_name or ''} {self.last_name}"
	
	def set_client_phone_code(self):
		phone = normalize_egyptian_phone(self.phone)
		if not phone:
			return
		self.phone = f"+2{phone}"
		
			
		
		
