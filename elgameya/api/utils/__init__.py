import frappe

def api_error(message, type=None):
    if type == 'Auth':
        frappe.local.response["http_status_code"] = 401
        frappe.local.response['message'] = message
        raise frappe.AuthenticationError(message)
    elif type == 'Perm':
        frappe.local.response["http_status_code"] = 403
        frappe.local.response['message'] = message
        raise frappe.AuthenticationError(message)
    elif type == 'Exist':
        frappe.local.response["http_status_code"] = 404
        frappe.local.response['message'] = message
        raise frappe.DoesNotExistError(message)
    elif type == 'Validation':
        frappe.local.response["http_status_code"] = 417
        frappe.local.response['message'] = message
        raise frappe.ValidationError(message)
    else:
        frappe.local.response["http_status_code"] = 404
        frappe.local.response["message"] = message
        frappe.throw(message)