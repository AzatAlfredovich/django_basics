from django.db import models


class Blog(models.Model):
    heading = models.CharField(
        max_length=50,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи",
    )
    content = models.TextField(
        max_length=1000,
        verbose_name="Содержимое",
        help_text="Введите содержимое статьи",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью статьи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания статьи",
        help_text="Введите дату создания",
        blank=True,
        null=True,
    )
    publication_sign = models.BooleanField(
        default=False,
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
        editable=False
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["heading"]

    def __str__(self):
        return f"Статья - {self.heading}"
