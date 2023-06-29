from django.db.models.fields import CharField
import random

class RandomField(CharField):
    def __init__(self, available_chars=None, length=None, *args, **kwargs):
        self.available_chars = available_chars
        self.length = length
        super().__init__(*args, **kwargs)
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value:
            value = self.generate_random_value()
            setattr(model_instance, self.attname, value)
        return value
    
    def generate_random_value(self):
        phrase = ''.join(random.choice(self.available_chars) for _ in range(self.length))
        model_class = self.model
        while model_class._default_manager.filter(**{self.name:phrase}).exists():
            phrase = ''.join(random.choice(self.available_chars) for _ in range(self.length))
        return phrase

