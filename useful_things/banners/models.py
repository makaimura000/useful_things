from django.db import models


class Banner(models.Model):
    name = models.CharField('Название', max_length=30)
    description = models.TextField('Описание', blank=True, null=True)
    banner = models.ImageField(
        'Баннер',
        upload_to='banners/',
        blank=False
    )
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.name
