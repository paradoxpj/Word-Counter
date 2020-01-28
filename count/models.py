from django.db import models


class UrlText(models.Model):
    urltext = models.CharField(max_length=200)


class FinalData(models.Model):
    query = models.ForeignKey(UrlText, null=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=20)
    value = models.IntegerField()
