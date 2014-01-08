from django.db import models
from contactdb.forms.fields import JSONFormField

import json

# JSONWidget, JSONFormField and JSONField adapted from http://justcramer.com/2009/04/14/cleaning-up-with-json-and-sql/
# Added support for custom JSON encoders/decoders
class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase
    
    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=self.form_class, validator=self.validator, **kwargs)
    
    def __init__(self, *args, **kwargs):
        self.validator = kwargs.pop('validator', None)
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

