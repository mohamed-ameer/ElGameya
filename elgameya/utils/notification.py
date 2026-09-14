import frappe
from frappe.desk.doctype.notification_log.notification_log import make_notification_logs
from frappe.core.doctype.communication.email import _make as make_communication  

def send_notification(
    *,
    doc,
    users,
    notification_subject=None,
    notification_message=None,
    email_template=None,
    email_subject=None,
    email_message=None,
    send_notification=True,
    send_email=True,
    add_communication_record=False,
    from_user="Administrator",
):
    """
    Generic utility for sending notifications and/or emails.

    Args:
        doc: Frappe document used for template rendering.
        users (list): Recipients.
        notification_subject (str): Notification subject/template.
        notification_message (str): Notification message/template.
        email_template (str|Document): Email Template name or document.
        email_subject (str): Email subject/template.
        email_message (str): Email message/template.
    """
    is_notification_sent = False
    is_email_sent = False
    if isinstance(users, str):
        users = [users]
    users = list({u for u in users if u})
    context = {"doc": doc}

    def render(value):
        return frappe.render_template(value, context) if value else None

    # Notification
    if send_notification and (notification_subject or notification_message):
        try:
            notification_doc = frappe._dict(
                {
                    "document_type": doc.doctype,
                    "document_name": doc.name,
                    "type": "Alert",
                    "subject": render(notification_subject),
                    "email_content": render(notification_message),
                    "from_user": from_user,
                }
            )

            make_notification_logs(notification_doc, users)
            is_notification_sent = True
        except Exception:
            frappe.log_error(
                title=f"Notification Failed | {doc.doctype} | {doc.name}",
                message=frappe.get_traceback()
            )

    # Email from Email Template
    if send_email and email_template:
        try:
            template = (
                frappe.get_doc("Email Template", email_template)
                if isinstance(email_template, str)
                else email_template
            )
            subject = render(template.subject) 
            message = render(template.response)
            communication = None  
            if add_communication_record:  
                # Create Communication record first  
                communication = make_communication(  
                    doctype=get_reference_doctype(doc),  
                    name=get_reference_name(doc),  
                    content=message,  
                    subject=subject,  
                    recipients=users,  
                    communication_medium="Email",  
                    send_email=False,  
                    communication_type="Automated Message",  
                ).get("name") 
            
            frappe.sendmail(
                recipients=users,
                subject=subject,
                message=message,
                reference_doctype=get_reference_doctype(doc) if add_communication_record else None,
                reference_name=get_reference_name(doc) if add_communication_record else None,
                communication=communication
            )
            is_email_sent = True
        except frappe.OutgoingEmailError:
            pass
        except Exception as e:
            frappe.log_error(
                title=f"Email Notification Failed | {doc.doctype} | {doc.name}",
                message=frappe.get_traceback()
            )

    # Direct Email
    elif send_email and (email_subject or email_message):
        try:
            subject = render(email_subject)  
            message = render(email_message)  
              
            communication = None  
            if add_communication_record:  
                # Create Communication record first  
                communication = make_communication(  
                    doctype=get_reference_doctype(doc),  
                    name=get_reference_name(doc),  
                    content=message,  
                    subject=subject,  
                    recipients=users,  
                    communication_medium="Email",  
                    send_email=False,  
                    communication_type="Automated Message",  
                ).get("name")

            frappe.sendmail(
                recipients=users,
                subject=subject,
                message=message,
                reference_doctype=get_reference_doctype(doc) if add_communication_record else None,
                reference_name=get_reference_name(doc) if add_communication_record else None,
                communication=communication
            )
            is_email_sent = True
        except frappe.OutgoingEmailError:
            pass
        except Exception as e:
            frappe.log_error(
                title=f"Email Notification Failed | {doc.doctype} | {doc.name}",
                message=frappe.get_traceback()
            )
    
    return is_notification_sent, is_email_sent

def get_reference_doctype(doc):
    return doc.parenttype if doc.meta.istable else doc.doctype

def get_reference_name(doc):
    return doc.parent if doc.meta.istable else doc.name