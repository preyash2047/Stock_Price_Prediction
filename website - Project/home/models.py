from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.
class DataModel(Model):
    symbol = models.CharField(max_length = 50)
    qty = models.IntegerField(max_length=10, default=0)
    avgCost = models.FloatField(max_length=10, default=0)
    price = models.FloatField(max_length=10,default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.symbol

    class Meta:
        db_table = "datamodel_table"