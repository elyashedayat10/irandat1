from django.db import models


# Create your models here.
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class Setting(SingletonModel):
    title = models.CharField(max_length=125)
    icon = models.ImageField(upload_to="logo/")
    description = models.TextField()


class Guide(SingletonModel):
    text = models.TextField()


class Notification(models.Model):
    text = models.CharField(max_length=255)
    additional_data = models.JSONField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
