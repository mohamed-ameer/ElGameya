import re
import frappe
from frappe import _ 


def validate_number(value, start_with=None, end_with=None, total_digits=None):
    value = str(value)

    if not value.isdigit():
        return False

    if total_digits is not None and len(value) != total_digits:
        return False

    if start_with is not None:
        prefixes = (
            start_with
            if isinstance(start_with, (list, tuple, set))
            else [start_with]
        )

        if not any(value.startswith(str(prefix)) for prefix in prefixes):
            return False

    if end_with is not None:
        suffixes = (
            end_with
            if isinstance(end_with, (list, tuple, set))
            else [end_with]
        )

        if not any(value.endswith(str(suffix)) for suffix in suffixes):
            return False

    return True

def validate_child_table_duplicates(
    doc,
    method=None,
    *,
    child_doctype: str,
    unique_fields: tuple,
    check_within_same_document: bool = True,
    check_other_parent_documents: bool = False,
    skip_empty_fields: bool = False
):
    """
    Generic validator to prevent duplicate rows in child tables.

    :param doc: Parent document
    :param child_doctype: Child table DocType name
    :param unique_fields: Tuple of fieldnames forming a unique key
    :param check_within_same_document: Prevent duplicates within same document
    :param check_other_parent_documents: Prevent duplicates across other parents

    Example:
    def validate(doc, method):
        validate_child_table_duplicates(
            doc,
            child_doctype="Child_Doctype_Name",
            unique_fields=("field1", "field2"),
        )
    """

    if not child_doctype or not unique_fields:
        return

    # Find all child table fields using this child doctype
    for field in doc.meta.fields:
        if field.fieldtype != "Table" or field.options != child_doctype:
            continue

        rows = doc.get(field.fieldname) or []
        seen_keys = {}

        for idx, row in enumerate(rows, start=1):
            values = {f: row.get(f) for f in unique_fields}

            # Skip incomplete rows
            if not all(values.values()):
                if not skip_empty_fields:
                    frappe.throw(_("All fields must be filled before saving."))

            # --------------------------------------
            # Cross-document duplicate check
            # --------------------------------------
            if check_other_parent_documents:
                existing_parent = frappe.db.get_value(
                    child_doctype,
                    {
                        **values,
                        "parent": ["!=", doc.name],
                    },
                    "parent",
                )

                if existing_parent:
                    frappe.throw(
                        _(
                            "Row {idx}: combination ({fields}) already exists "
                            "in document '{parent}'."
                        ).format(
                            idx=idx,
                            fields=", ".join(
                                f"{k}={v}" for k, v in values.items()),
                            parent=existing_parent,
                        ),
                        title=_("Duplicate Entry"),
                    )

            # --------------------------------------
            # Same-document duplicate check
            # --------------------------------------
            if check_within_same_document:
                key = tuple(values[f] for f in unique_fields)

                if key in seen_keys:
                    frappe.throw(
                        _(
                            "Duplicate rows found! Row {row1} and Row {row2} "
                            "have the same values for {fields}."
                        ).format(
                            row1=seen_keys[key],
                            row2=idx,
                            fields=", ".join(unique_fields),
                        ),
                        title=_("Duplicate Rows"),
                    )

                seen_keys[key] = idx
