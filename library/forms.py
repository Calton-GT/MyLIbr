from django import forms
from .models import Book, Author, Genre


class BookForm(forms.ModelForm):
    """Форма для добавления/редактирования книги"""
    new_author = forms.CharField(
        max_length=200,
        required=False,
        label="Или введите нового автора:",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя нового автора'
        })
    )

    new_genre = forms.CharField(
        max_length=100,
        required=False,
        label="Или введите новый жанр:",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название нового жанра'
        })
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'year', 'annotation', 'review', 'cover']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'annotation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля автора и жанра необязательными
        self.fields['author'].required = False
        self.fields['genre'].required = False
        # Сортируем авторов и жанры по алфавиту
        self.fields['author'].queryset = Author.objects.all().order_by('name')
        self.fields['genre'].queryset = Genre.objects.all().order_by('name')
        # Добавляем пустую опцию
        self.fields['author'].empty_label = "Выберите автора или введите нового"
        self.fields['genre'].empty_label = "Выберите жанр или введите новый"

    def clean(self):
        """Проверяем, что выбран существующий автор ИЛИ введен новый"""
        cleaned_data = super().clean()
        author = cleaned_data.get('author')
        new_author = cleaned_data.get('new_author')
        genre = cleaned_data.get('genre')
        new_genre = cleaned_data.get('new_genre')

        # Проверка автора
        if not author and not new_author:
            self.add_error('author', 'Выберите автора из списка или введите нового')
            self.add_error('new_author', 'Выберите автора из списка или введите нового')

        # Проверка жанра (необязательное поле)
        if not genre and new_genre:
            # Создаем новый жанр
            genre, created = Genre.objects.get_or_create(name=new_genre.strip())
            cleaned_data['genre'] = genre

        return cleaned_data

    def save(self, commit=True):
        """Сохраняем форму, создавая нового автора/жанр при необходимости"""
        # Получаем данные
        new_author = self.cleaned_data.get('new_author')
        author = self.cleaned_data.get('author')
        new_genre = self.cleaned_data.get('new_genre')
        genre = self.cleaned_data.get('genre')

        # Создаем нового автора, если введен
        if new_author and not author:
            author, created = Author.objects.get_or_create(name=new_author.strip())
            self.instance.author = author

        # Создаем новый жанр, если введен
        if new_genre and not genre:
            genre, created = Genre.objects.get_or_create(name=new_genre.strip())
            self.instance.genre = genre

        # Сохраняем книгу
        return super().save(commit=commit)