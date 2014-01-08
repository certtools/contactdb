from django import forms

import json
               
class JSONListToNewlineWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            display_string = ''
            if value is not None and len(value) > 0:
                for v in value:
                    display_string += v + '\n'
                    
            value = display_string
        return super(JSONListToNewlineWidget, self).render(name, value, attrs)

class JSONWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = json.dumps(value, indent=2)
        return super(JSONWidget, self).render(name, value, attrs)
