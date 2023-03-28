import os


SENDGRID_API_KEY= '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'
FROM_EMAIL='kumawatmohitmk@gmail.com'
DEFAULT_FROM_EMAIL='kumawatmohitmk@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
EMAIL_PORT = 587

# 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