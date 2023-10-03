#!/usr/bin/python3
import configparser
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

conf = configparser.ConfigParser()
conf.read('cfg.ini')

subject = conf.get('MAIL', 'subject')
mailfrom = conf.get('MAIL', 'from')
smtp = conf.get('MAIL', 'smtp')
mail_usr = conf.get('MAIL', 'user')
mail_pwd = conf.get('MAIL', 'pwd')
mail_to = conf.get('MAIL', 'to')

print('CFG erfolgreich geladen')
