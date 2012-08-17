#!/usr/bin/env python
import traceback
from django.core.management import execute_manager
import imp

try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

try:
    from settings import active as settings
except ImportError, e:
    SETTINGS_ACTIVE_CONTENTS = 'from dev import *'
    print '\033[1;33m'
    print "Apparently you don't have the file settings/active.py yet."
    print "Create it containing '%s'\033[0m" % SETTINGS_ACTIVE_CONTENTS
    print
    print "=" * 20
    print "original traceback:"
    print "=" * 20
    print
    traceback.print_exc(e)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
