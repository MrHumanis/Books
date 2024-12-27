# Create your models here.
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name="Имя")
    def __str__(self):
        return self.name

class BaseBlog(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )

    class Meta:
        abstract = True


class Shelf(BaseBlog):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True,
                            verbose_name="Идентификатор",
                            help_text="Идентификатор страницы для URL; "
                                      "разрешены символы латиницы, "
                                      "цифры, дефис и подчёркивание."
                            )
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'полка'
        verbose_name_plural = 'Полки'


class Book(BaseBlog):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст", )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(verbose_name="Остаток")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name="Автор книги",
        related_name="posts"
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.SET_NULL,
        verbose_name="Полка",
        null=True
    )
    image = models.ImageField(
        upload_to="media/",
        null=True,
        verbose_name="Обложка",
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'Книги'
