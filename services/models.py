from django.db import models


class Treatment(models.Model):
    CATEGORY_CHOICES = [
        ("massage", "Massage"),
        ("body", "Body Treatment"),
        ("facial", "Facial"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )
    duration = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    included = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_active = models.BooleanField(default=True)

    @property
    def included_items(self):
        return [
            item.strip()
            for item in self.included.splitlines()
            if item.strip()
        ]

    def __str__(self):
        return self.name