from tortoise import fields, Model

class Personas(Model):
    id_persona = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    telefono = fields.CharField(max_length=100, unique=True)

    class Meta:
        db = "default" 
