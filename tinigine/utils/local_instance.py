import threading
context = threading.local()


def get_instance(name):
    return getattr(context, name, None)


def set_instance(name, obj):
    setattr(context, name, obj)