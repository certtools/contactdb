from django import forms
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ValidationError

import json

from contactdb.forms.widgets import JSONListToNewlineWidget, JSONWidget


class JSONListToNewlineField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.validator = kwargs.pop('validator', None)
        
        messages = getattr(self, 'error_messages', {})
        custom_error_messages = kwargs.pop('error_messages', {})
        
        for (key, value) in custom_error_messages:
            messages[key] = value
            
        self.error_messages = messages
        
        kwargs['widget'] = JSONListToNewlineWidget
        super(JSONListToNewlineField, self).__init__(*args, **kwargs)
        
        print 'Got here'
        
        if self.validator:
            if self.validators:
                self.validators.append(self.validate_elements)
            else:
                self.validators = [self.validate_elements]
            
        print 'Got here too: %r' % self.validators
        
    def validate_elements(self, value):
        errors = []
        values = [v.strip() for v in value.split('\n')]
        i = 0
        
        if not self.validator:
            return values
        
        print 'Validate elements'
        
        for v in values:
            i += 1
            try:
                self.validator(v)
            except ValidationError as e:
                message = 'Error in element %s: %s' % (i, str(e))
                errors.append(message)
        if errors:
            raise ValidationError(errors)
        else:
            return values
        
    def clean(self, value):
        print 'Cleaning elements'
        if not value:
            return
        try:
            return self.validate_elements(value)
        except Exception, exc:
            raise exc
            
#class JSONListToNewlineField(forms.CharField):
#    def __init__(self, *args, **kwargs):
#        kwargs['widget'] = JSONListToNewlineWidget
#        super(JSONListToNewlineField, self).__init__(*args, **kwargs)
#        
#    def clean(self, value):
#        if not value:
#            return
#        try:
#            return [v.strip() for v in value.split('\n')]
#        except Exception, exc:
#            raise forms.ValidationError(u'Split error: %s' % unicode(exc))

class JSONFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONWidget
        super(JSONFormField, self).__init__(*args, **kwargs)
        
    def clean(self, value):
        if not value:
            return
        try:
            if self.decoder:
                return json.loads(value, cls=self.decoder)
            else:
                return json.loads(value)
        except Exception, exc:
            raise forms.ValidationError(u'JSON decode error: %s' % unicode(exc))
