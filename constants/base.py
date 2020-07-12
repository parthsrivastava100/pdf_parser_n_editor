# PII constant types
PII_CC_NUMBER = 'cc_number'
PII_EIN = 'ein'
PII_EMAIL = 'email'
PII_GENDER = 'gender'
PII_USA_PHONE = 'usa_phone'
PII_SSN = 'ssn'
PII_CITY = 'city'
PII_COUNTRY = 'country'
PII_STATE = 'state'
PII_NAME = 'name'
PII_FNAME = 'first_name'
PII_LNAME = 'last_name'
PII_ROUTING = 'routing'
PII_IP = 'ip_address'
PII_COMPANY = 'company'

PII_DESCRIPTIONS = {
    'cc_number': 'Credit Card Number',
    'ein': 'Employee Identification Number',
    'email': 'E-Mail Address',
    'gender': 'Gender',
    'usa_phone': 'Phone Number (USA)',
    'ssn': 'Social Security Number',
    'city': 'City',
    'country': 'Country',
    'state': 'State',
    'name': 'Name',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'ip_address': 'IP Address',
    'routing': 'Routing Number',
    'company':'Company Name',
}

PII_CATEGORIES = {
    'cc_number': 'Financial',
    'ein': 'Identity',
    'email': 'Identity',
    'gender': 'Identity',
    'usa_phone': 'Identity',
    'ssn': 'Identity',
    'city': 'Location',
    'country': 'Location',
    'state': 'Location',
    'name': 'Identity',
    'first_name': 'Identity',
    'last_name': 'Identity',
    'ip_address': 'Identity',
    'routing': 'Financial',
    'company':'Financial'
}
