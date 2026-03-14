import threading


_thread_locals = threading.local()


def set_current_organization(org):
    """
    Store organization for current request thread.
    """
    _thread_locals.organization = org


def get_current_organization():
    """
    Retrieve organization from current thread.
    """
    return getattr(_thread_locals, "organization", None)


def clear_current_organization():
    if hasattr(_thread_locals, "organization"):
        del _thread_locals.organization


def set_system_mode():
    _thread_locals.system_mode = True


def is_system_mode():
    return getattr(_thread_locals, "system_mode", False)


def clear_system_mode():
    if hasattr(_thread_locals, "system_mode"):
        del _thread_locals.system_mode