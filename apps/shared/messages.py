# Django
from django.utils.translation import ugettext_lazy as _

INVALID_REQUIRED = _('This field is required.')
INVALID_PASSWORD_LENGTH = _('This password is too short. '
                            'It must contain at least 8 characters.')
INVALID_PASSWORD_ENTIRELY_NUMERIC = _('This password is entirely numeric.')
INVALID_BLANK = _('This field may not be blank.')
INVALID_STRING = _('Not a valid string.')
INVALID_BOOLEAN = _('"%s" is not a valid boolean.')
INVALID_DATETIME = _(
    'Datetime has wrong format. '
    'Use one of these formats instead: '
    'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
)
INVALID_NULL = _('This field may not be null.')
INVALID_PK = _('Incorrect type. Expected pk value, received str.')
INVALID_CHOICE = _('"%s" is not a valid choice.')
INVALID_DOES_NOT_EXICT = _('Invalid pk "%s" - object does not exist.')
CREATED = _('Created')
UPDATED = _('Updated')
NOT_OWNER_PERMISSION = _('You not owner of this company')
