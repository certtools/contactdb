from django.db import models
from django import forms

import json

class JSONListToNewlineField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONListToNewlineWidget
        super(JSONListToNewlineField, self).__init__(*args, **kwargs)
        
    def clean(self, value):
        if not value:
            return
        try:
            return [v.strip() for v in value.split('\n')]
        except Exception, exc:
            raise forms.ValidationError(u'Decode error: %s' % unicode(exc))
                
class JSONListToNewlineWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            display_string = ''
            if value is not None and len(value) > 0:
                for v in value:
                    display_string += v + '\n'
                    
            value = display_string
        return super(JSONListToNewlineWidget, self).render(name, value, attrs)

# JSONWidget, JSONFormField and JSONField adapted from http://justcramer.com/2009/04/14/cleaning-up-with-json-and-sql/
# Added support for custom JSON encoders/decoders
class JSONWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = json.dumps(value, indent=2)
        return super(JSONWidget, self).render(name, value, attrs)
        
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

class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase
    
    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=self.form_class, **kwargs)
    
    def __init__(self, *args, **kwargs):
        self.encoder = kwargs.pop('encoder', None)
        self.decoder = kwargs.pop('decoder', None)
        self.form_class = kwargs.pop('form_class', JSONFormField)
        super(JSONField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        if not value:
            return
        elif isinstance(value, basestring):
            if self.decoder:
                return json.loads(value, cls=self.decoder)
            else:
                return json.loads(value)
        else:
            return value
            
    def get_db_prep_value(self, value, *args, **kwargs):
        if not value:
            return
        elif self.encoder:
            return json.dumps(value, cls=self.encoder)
        else:
            return json.dumps(value)
            
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
