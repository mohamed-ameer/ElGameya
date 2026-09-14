import frappe, base64
from frappe import _

def basic_auth(username, password):
    auth_string = f"{username}:{password}"
    return base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

def workflow_state_changed(doc, from_state=None, to_state=None):  # pragma: no cover
    """
    Check whether a document's workflow state changed.

    Args:
        doc (self object):
            It must be the `self` object of DocType instance methods,
            or it will always return False because `get_doc_before_save()` works with self only.
        from_state (str, optional):
            Only return True if the previous workflow state matches this value.
        to_state (str, optional):
            Only return True if the new workflow state matches this value.

    Returns:
        bool: True if the workflow state changed and the provided conditions match.
    """
    old = doc.get_doc_before_save()

    if doc.is_new() or not old:
        return False

    changed_from = (old.workflow_state == from_state) if from_state else True
    changed_to = (doc.workflow_state == to_state) if to_state else True
    has_changed = old.workflow_state != doc.workflow_state

    return changed_from and has_changed and changed_to

def create_integration_request(base_url ,method ,integration_request_service = "", request_id = '' , status_code = 200 ,request_headers="" , request_data = ""  , request_response = "" , ref_doctype = None , ref_name = None, commit=False) :
    """ create integration request for each request""" 
    integration_request = frappe.new_doc("Integration Request")
    integration_request.update(
        {
            "request_id": request_id,
            "integration_type": "Host",
            "integration_request_service": integration_request_service,
            "url" : base_url + method ,
            "requested_api": method,
            "requested_endpoint": method,
            "request_headers": str(request_headers),
            "data": str(request_data),
            "output": str(request_response),
            "reference_doctype" : ref_doctype ,
            "reference_docname" : ref_name ,
            "status" : "Completed" if 200 <= status_code < 300 else "Failed"
        }
    )
    integration_request.insert(ignore_permissions=True)
    if commit:
        frappe.db.commit()

    return integration_request.name

def to_dict(obj):
    if isinstance(obj, dict):
        return frappe._dict({k: to_dict(v) for k, v in obj.items()})

    if isinstance(obj, list):
        return [to_dict(i) for i in obj]

    return obj

@frappe.whitelist()
def get_allowed_roles_from_settings(settings_doctype, field_name):
    "get Allowed Roles from Doctype Settings"
    if not settings_doctype or not field_name:
        return []
    if isinstance(field_name, str):
        field_name = [field_name]
    elif not isinstance(field_name, (list, tuple)):
        frappe.throw("field_names must be a string or list of strings")
    settings = frappe.get_single(settings_doctype)
    allowed_roles = []
    for f_name in field_name:
        allowed_roles += [x.role for x in (settings.get(f_name) or []) if x.role]
    allowed_roles = set(allowed_roles)

    return list(allowed_roles)