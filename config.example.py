# Description: Template configuration file for the app.

# Recipients of the daily menu
RECIPIENTS: list[str] = []

# Restaurant name and Facebook page
RESTAURANT: dict = {
    'name': '',
    'fb_page': ''
}


# OpenAI API key
OPEN_AI_KEY = ''

# RocketChat API access
ROCKET_CHAT: dict[str, str] = {
    'host': '',
    'user': '',
    'password': '',
}

# # SMTP server used for notification emails etc.
# SMTP: dict = {
#     'host': '',
#     'port': '',
#     'user': '',
#     'password': '',
# }