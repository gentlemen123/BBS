#! /usr/bin/env python3
# coding:utf-8

import re
re_email1 = re.compile(r'[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?com')
re_email2 = re.compile(r'<[a-zA-Z]+\s[a-zA-Z]+>\s[0-9a-zA-Z.]+@[0-9a-zA-Z.]+?org')
email_address = input('Please enter your email address:')
if re_email1.match(email_address):
    print ('Yes, your email_address is valid')
    print (email_address)
elif re_email2.match(email_address):
    print ('Yes, your email_address is valid')
    print (email_address)
else:
    print ('sorry, your email address is invalid')
