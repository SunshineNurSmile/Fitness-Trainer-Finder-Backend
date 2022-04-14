from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from backend import settings


class Trainee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='trainee'
    )
    heightft = models.IntegerField(null=True, blank=True)
    heightin = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    training_style = models.CharField(max_length=50, default='PowerLifting')
    dob = models.DateField(default=date.today)
    gender = models.CharField(max_length=6, default="Male")
    _id = models.AutoField(primary_key=True, editable=False)
    description = models.TextField(null=True, blank=True)
    avatar = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Trainer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='trainer'
    )
    avatar = models.TextField(null=True, blank=True)
    image1 = models.TextField(null=True, blank=True)
    image2 = models.TextField(null=True, blank=True)
    image3 = models.TextField(null=True, blank=True)
    image4 = models.TextField(null=True, blank=True)
    image5 = models.TextField(null=True, blank=True)
    image6 = models.TextField(null=True, blank=True)
    training_style = models.CharField(max_length=50, default='PowerLifting')
    # TODO
    # create trainers course and category needs to search trainer
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    dob = models.DateField(default=date.today)
    gender = models.CharField(max_length=6, default="Male")
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    trainee = models.ForeignKey(Trainee, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(default=0, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    trainee = models.OneToOneField(
        'Trainee',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='order'
    )
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = False
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)


class Chat(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    trainee = models.ForeignKey(Trainee, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self._id)


class Note(models.Model):
    trainee = models.OneToOneField(
        'Trainee',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='note'
    )
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self._id)


class Payment(models.Model):
    trainer = models.OneToOneField(
        'Trainer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payment'
    )
    price1 = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    price2 = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    price3 = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    description1 = models.TextField(null=True, blank=True)
    description2 = models.TextField(null=True, blank=True)
    description3 = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.trainer.pk)


class File(models.Model):
    trainer = models.OneToOneField(
        'Trainer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='file'
    )
    existingPath = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()

    def __str__(self):
        return str(self.name)

