#!/usr/bin/env python
import os
import sys

#config_mode = os.getenv('DJANGO_CONFIG_MODE', 'base')

#config_dict = {
#    'base': 'settings.base'
#    'local': 'settings.local'
#    'production': 'settings.production'
#}

if __name__ == "__main__":
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', config_dict[config_mode])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rss2.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
