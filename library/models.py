from django.db import models



class Author(models.Model):
    """Модель автора книги"""
    name = models.CharField(max_length=200, verbose_name="Имя автора")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']


class Genre(models.Model):
    """Модель жанра книги"""
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']


class Book(models.Model):
    """Основная модель книги"""
    title = models.CharField(max_length=300, verbose_name="Название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name="Автор", related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name="Жанр")
    year = models.IntegerField(verbose_name="Год издания")
    annotation = models.TextField(verbose_name="Аннотация", blank=True)
    review = models.TextField(verbose_name="Рецензия", blank=True)
    cover = models.ImageField(upload_to='book_covers/',
                              verbose_name="Обложка", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author.name}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']