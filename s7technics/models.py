from django.db import models

# Create your models here.


class AirTypes(models.Model):
    model = models.CharField(max_length=16)
    length = models.FloatField()
    width = models.FloatField()

    def __str__(self):
        return 'Тип самолета {}'.format(self.model)


class AirPlane(models.Model):
    bort_number = models.CharField(max_length=64, unique=True)
    plane_type = models.ForeignKey(AirTypes, on_delete=models.PROTECT)
    on_service = models.BooleanField(default=False)
    x_in_hangar = models.PositiveIntegerField(null=True, blank=True)
    y_in_hangar = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return 'БН: {}, тип {}'.format(self.bort_number, self.plane_type)


class Hangar(models.Model):
    HANGARS = (
        ('DME', 'Домодедово'),
        ('SVO', 'Шереметьево'),
        ('VKO', 'Внуково')
    )

    name = models.CharField(max_length=3, choices=HANGARS, default='DME')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    is_filled = models.BooleanField(default=False)
    airplane = models.ForeignKey(AirPlane, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Ангар {}'.format(self.name)


class AviaCompany(models.Model):
    name = models.CharField(max_length=64)
    start_date_TS = models.DateField()
    end_date_TS = models.DateField()
    penalty_coef = models.FloatField()

    def __str__(self):
        return 'Авиакомпания {}'.format(self.name)


class TechnicalService(models.Model):
    class Meta:
        unique_together = [['type', 'airplane_type', 'hangar']]

    C_CHECK = 'C'
    D_CHECK = 'D'
    REDELIVERY = 'R'
    PAINTING = 'P'

    TYPES = (
        (C_CHECK, 'C-Check'),
        (D_CHECK, 'D-Check'),
        (REDELIVERY, 'Redelivery'),
        (PAINTING, 'Painting'),
    )
    type = models.CharField(max_length=1, choices=TYPES)
    airplane_type = models.ForeignKey(AirTypes, on_delete=models.PROTECT)
    hangar = models.ForeignKey(Hangar, on_delete=models.PROTECT)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Тип ТО {}, тип ВС {}, ангар {}, цена {}'.format(self.type, self.airplane_type, self.hangar, self.price)


class CompanyRequirement(models.Model):
    company = models.ForeignKey(AviaCompany, on_delete=models.PROTECT)
    service = models.ForeignKey(TechnicalService, on_delete=models.PROTECT)
    require_amount = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    contract_amount = models.PositiveSmallIntegerField(null=True, blank=True)

