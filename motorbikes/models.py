from django.db import models

class Brands(models.Model):
    """
        Big storage where daily prices will go
    """
    class Meta:
        app_label = 'motorbikes'

    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, db_index=True)

class Motorbikes(models.Model):
    """
        Big storage where daily prices will go
    """
    class Meta:
        app_label = 'motorbikes'

    bike_id = models.CharField(primary_key=True, max_length=64, db_index=True)
    name = models.CharField(max_length=64)
    brand = models.ForeignKey(Brands, null=True, db_index=True, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, db_index=True)
    km = models.IntegerField(null=True, db_index=True)
    type = models.CharField(max_length=64, db_index=True)
    licence = models.CharField(max_length=64, db_index=True)
    old_price = models.IntegerField(null=True, db_index=True)
    price = models.IntegerField(null=True, db_index=True)
    cc = models.IntegerField(null=True, db_index=True)
    url = models.CharField(max_length=128)
    image = models.CharField(max_length=128)

    