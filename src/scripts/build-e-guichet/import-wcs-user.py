from quixote import get_publisher

user = get_publisher().user_class()
user.form_data = {}
user.email = 'TEST'
user.form_data['_first_name'] = 'TEST'
user.form_data['_last_name'] = 'TEST'
user.name_identifiers = []
user.store()

