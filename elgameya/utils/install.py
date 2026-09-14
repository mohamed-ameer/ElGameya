import frappe

def after_install():
    """Runs after app installation"""
    print("Running ElGameya After Install Hook")
    set_app_logo()
    set_system_settings()
    set_navbar_settings()
    set_website_settings()
    set_workspace_settings()
    add_switch_language_to_navbar_settings()

def before_migrate():
    """Runs before database migration"""
    print("Running ElGameya Before Migrate Hook")

def after_migrate():
    """Runs after database migration"""
    print("Running ElGameya After Migrate Hook")
    set_app_logo()
    set_system_settings()
    set_navbar_settings()
    set_website_settings()
    set_workspace_settings()
    add_switch_language_to_navbar_settings()

def set_app_logo():
    """Sets app logo in navbar"""
    print("Setting App Logo")
    app_logo = frappe.get_hooks("app_logo_url")[-1]
    frappe.db.set_single_value("Navbar Settings", "app_logo", app_logo)

def set_system_settings():
    """Sets default system settings"""
    print("Setting Default System Settings")
    frappe.db.set_value("Currency", "EGP", {"enabled": 1}, update_modified=False)
    settings = frappe.get_doc("System Settings")
    settings.app_name = "ElGameya"
    settings.language = "ar"
    settings.country = "Egypt"
    settings.currency = "EGP"
    settings.time_zone = "Africa/Cairo"
    settings.session_expiry = "12:00"
    settings.login_with_email_link = False
    settings.store_attached_pdf_document = False
    settings.allow_guests_to_upload_files = True
    settings.link_field_results_limit = 10
    settings.allow_error_traceback = frappe.get_site_config().get("developer_mode", 0)
    settings.disable_system_update_notification = False
    settings.disable_user_pass_login = True if int(frappe.db.get_value("LDAP Settings", "LDAP Settings", "enabled")) else False
    settings.allowed_file_extensions = "JPG\nJPEG\nPNG\nPDF\nDOC\nDOCX\nMP4\nWEBM"
    settings.save()

def set_navbar_settings():
    """Sets default navbar settings"""
    print("Setting Default Navbar Settings")
    settings = frappe.get_doc("Navbar Settings")
    settings.logo_width = "35"
    for help_item in settings.help_dropdown:
        if not help_item.item_label == "Keyboard Shortcuts":
            help_item.hidden = True
    settings.save()

def set_website_settings():
    """Sets default website settings"""
    print("Setting Default Website Settings")
    settings = frappe.get_doc("Website Settings")
    settings.app_name = "ElGameya"
    settings.home_page = "login"
    settings.hide_footer_signup = True
    settings.save()

def set_workspace_settings():
    """Sets default workspace settings"""
    print("Setting Default Workspace Settings")
    HIDDEN_WORKSPACE = ["Build", "Integrations", "Users", "Tools", "Website", "Welcome Workspace"]
    for workspace in HIDDEN_WORKSPACE:
        if frappe.db.exists("Workspace", workspace):
            ws = frappe.get_doc("Workspace", workspace)
            ws.is_hidden = 1
            ws.public = 0
            ws.save()

def add_switch_language_to_navbar_settings():
    """ Add switch language to navbar settings """
    print("Adding Switch Language to Navbar Settings")
    navbar_settings = frappe.get_single("Navbar Settings")
    if frappe.db.exists("Navbar Item", {"item_label": "Toggle Language"}):
        return
    for navbar_item in navbar_settings.settings_dropdown[8:]:
        navbar_item.idx = navbar_item.idx + 1
    navbar_settings.append(
        "settings_dropdown",
        {
            "item_label": "Toggle Language",
            "item_type": "Action",
            "action": "new elgameya.ui.LanguageSwitcher().toggle()",
            "is_standard": 0,
            "idx": 9,
        },
    )
    navbar_settings.save()