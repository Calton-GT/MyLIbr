from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Genre
from .forms import BookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def delete_book(request, book_id):
    """Удаление книги с подтверждением"""
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Удаляем книгу
        book.delete()
        # Перенаправляем на главную страницу с сообщением об успехе
        return redirect('home')

    # Если GET запрос, показываем страницу подтверждения
    return render(request, 'library/delete_book.html', {'book': book})

def home(request):
    """Главная страница со списком книг"""
    # Получаем все книги, отсортированные по дате добавления
    books_list = Book.objects.all().order_by('-created_at')

    # Создаем тестовые данные, если книг меньше 5
    if Book.objects.count() < 5:
        print("Книг мало, создаем тестовые данные...")
        create_sample_data()
        books_list = Book.objects.all().order_by('-created_at')

    # Настраиваем пагинацию - 6 книг на странице
    paginator = Paginator(books_list, 6)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, показываем первую страницу
        books = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона, показываем последнюю страницу
        books = paginator.page(paginator.num_pages)

    return render(request, 'library/home.html', {'books': books})


def book_detail(request, book_id):
    """Страница с детальной информацией о книге"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})


def statistics(request):
    """Страница со статистикой"""
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_genres = Genre.objects.count()

    return render(request, 'library/statistics.html', {
        'total_books': total_books,
        'total_authors': total_authors,
        'total_genres': total_genres,
    })


@login_required
def add_book(request):
    """Страница для добавления новой книги"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'library/add_book.html', {'form': form})


@login_required
def edit_book(request, book_id):
    """Редактирование существующей книги"""
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'library/edit_book.html', {'form': form, 'book': book})


def create_sample_data():
    """Функция для создания 20 тестовых книг"""

    # Проверяем, есть ли уже данные
    if Book.objects.count() > 5:  # Если уже есть хотя бы 5 книг, не создаем
        print("В базе уже есть книги, пропускаем создание тестовых данных")
        return

    print("Создаем 20 тестовых книг...")

    try:
        # Создаем авторов (15 авторов)
        authors_data = [
            "Фёдор Достоевский", "Лев Толстой", "Антон Чехов", "Александр Пушкин",
            "Михаил Лермонтов", "Николай Гоголь", "Иван Тургенев", "Александр Солженицын",
            "Михаил Булгаков", "Владимир Набоков", "Иван Бунин", "Максим Горький",
            "Александр Островский", "Александр Грибоедов", "Александр Радищев"
        ]

        authors = {}
        for author_name in authors_data:
            author, created = Author.objects.get_or_create(name=author_name)
            authors[author_name] = author
            if created:
                print(f"Создан автор: {author_name}")

        print(f"Всего авторов: {Author.objects.count()}")

        # Создаем жанры (10 жанров)
        genres_data = [
            "Роман", "Классика", "Драма", "Поэзия", "Фантастика",
            "Детектив", "Исторический", "Приключения", "Научная литература", "Биография"
        ]

        genres = {}
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres[genre_name] = genre
            if created:
                print(f"Создан жанр: {genre_name}")

        print(f"Всего жанров: {Genre.objects.count()}")

        # Создаем 20 книг
        books_data = [
            # Достоевский
            {
                "title": "Преступление и наказание",
                "author": authors["Фёдор Достоевский"],
                "genre": genres["Роман"],
                "year": 1866,
                "annotation": "Роман о студенте Родионе Раскольникове, который совершает преступление.",
                "review": "Глубокий психологический роман, исследующий тему морали и раскаяния."
            },
            {
                "title": "Братья Карамазовы",
                "author": authors["Фёдор Достоевский"],
                "genre": genres["Роман"],
                "year": 1880,
                "annotation": "Последний роман Достоевского, затрагивающий вопросы веры и морали.",
                "review": "Философский роман, исследующий природу человека."
            },
            {
                "title": "Идиот",
                "author": authors["Фёдор Достоевский"],
                "genre": genres["Роман"],
                "year": 1869,
                "annotation": "Роман о князе Мышкине, добром и наивном человеке.",
                "review": "Трогательная история о чистоте души в жестоком мире."
            },

            # Толстой
            {
                "title": "Война и мир",
                "author": authors["Лев Толстой"],
                "genre": genres["Исторический"],
                "year": 1869,
                "annotation": "Эпопея о жизни русского общества во время войны с Наполеоном.",
                "review": "Монументальное произведение, охватывающее судьбы множества персонажей."
            },
            {
                "title": "Анна Каренина",
                "author": authors["Лев Толстой"],
                "genre": genres["Роман"],
                "year": 1877,
                "annotation": "Роман о трагической любви замужней женщины Анны Карениной.",
                "review": "Классика мировой литературы о любви, предательстве и обществе."
            },
            {
                "title": "Воскресение",
                "author": authors["Лев Толстой"],
                "genre": genres["Роман"],
                "year": 1899,
                "annotation": "Последний роман Толстого о нравственном возрождении.",
                "review": "Сильное произведение о раскаянии и искуплении."
            },

            # Чехов
            {
                "title": "Вишневый сад",
                "author": authors["Антон Чехов"],
                "genre": genres["Драма"],
                "year": 1904,
                "annotation": "Пьеса о дворянской семье, вынужденной продать свой вишневый сад.",
                "review": "Тонкая драма о смене эпох и уходящем дворянском быте."
            },
            {
                "title": "Три сестры",
                "author": authors["Антон Чехов"],
                "genre": genres["Драма"],
                "year": 1901,
                "annotation": "Пьеса о трёх сёстрах, мечтающих о Москве.",
                "review": "Глубокое произведение о несбывшихся мечтах и надеждах."
            },

            # Пушкин
            {
                "title": "Евгений Онегин",
                "author": authors["Александр Пушкин"],
                "genre": genres["Поэзия"],
                "year": 1833,
                "annotation": "Роман в стихах, считающийся классикой русской литературы.",
                "review": "Блестящее произведение о любви и судьбе."
            },
            {
                "title": "Капитанская дочка",
                "author": authors["Александр Пушкин"],
                "genre": genres["Исторический"],
                "year": 1836,
                "annotation": "Исторический роман о Пугачёвском восстании.",
                "review": "Увлекательная история о любви и долге на фоне исторических событий."
            },

            # Лермонтов
            {
                "title": "Герой нашего времени",
                "author": authors["Михаил Лермонтов"],
                "genre": genres["Роман"],
                "year": 1840,
                "annotation": "Психологический роман о молодом офицере Печорине.",
                "review": "Один из первых психологических романов в русской литературе."
            },

            # Гоголь
            {
                "title": "Мертвые души",
                "author": authors["Николай Гоголь"],
                "genre": genres["Роман"],
                "year": 1842,
                "annotation": "Поэма о похождениях Чичикова, скупающего 'мертвые души'.",
                "review": "Сатира на русское общество первой половины XIX века."
            },
            {
                "title": "Ревизор",
                "author": authors["Николай Гоголь"],
                "genre": genres["Драма"],
                "year": 1836,
                "annotation": "Комедия о чиновниках, принявших проезжего за ревизора.",
                "review": "Острая сатира на бюрократию и человеческие пороки."
            },

            # Тургенев
            {
                "title": "Отцы и дети",
                "author": authors["Иван Тургенев"],
                "genre": genres["Роман"],
                "year": 1862,
                "annotation": "Роман о конфликте поколений в России XIX века.",
                "review": "Знаковое произведение о нигилизме и семейных ценностях."
            },

            # Булгаков
            {
                "title": "Мастер и Маргарита",
                "author": authors["Михаил Булгаков"],
                "genre": genres["Фантастика"],
                "year": 1967,
                "annotation": "Роман о визите дьявола в Москву 1930-х годов.",
                "review": "Философский и мистический роман, ставший культовым."
            },

            # Набоков
            {
                "title": "Лолита",
                "author": authors["Владимир Набоков"],
                "genre": genres["Роман"],
                "year": 1955,
                "annotation": "Роман о трагической страсти мужчины к девочке-подростку.",
                "review": "Скандальный и мастерски написанный роман о запретной любви."
            },

            # Солженицын
            {
                "title": "Архипелаг ГУЛАГ",
                "author": authors["Александр Солженицын"],
                "genre": genres["Исторический"],
                "year": 1973,
                "annotation": "Художественно-историческое исследование советской репрессивной системы.",
                "review": "Монументальный труд о сталинских репрессиях."
            },

            # Горький
            {
                "title": "На дне",
                "author": authors["Максим Горький"],
                "genre": genres["Драма"],
                "year": 1902,
                "annotation": "Пьеса о жизни обитателей ночлежки.",
                "review": "Социальная драма о людях, опустившихся на самое дно жизни."
            },

            # Фантастика
            {
                "title": "451° по Фаренгейту",
                "author": Author.objects.get_or_create(name="Рэй Брэдбери")[0],
                "genre": genres["Фантастика"],
                "year": 1953,
                "annotation": "Антиутопия о мире, где книги запрещены и сжигаются.",
                "review": "Пророческий роман о важности знаний и свободы мысли."
            },

            # Детектив
            {
                "title": "Убийство в Восточном экспрессе",
                "author": Author.objects.get_or_create(name="Агата Кристи")[0],
                "genre": genres["Детектив"],
                "year": 1934,
                "annotation": "Детектив о расследовании убийства в поезде.",
                "review": "Блестящий детектив с неожиданной развязкой."
            }
        ]

        # Создаем книги
        created_count = 0
        for book_info in books_data:
            book, created = Book.objects.get_or_create(
                title=book_info["title"],
                defaults={
                    'author': book_info["author"],
                    'genre': book_info["genre"],
                    'year': book_info["year"],
                    'annotation': book_info["annotation"],
                    'review': book_info["review"],
                }
            )
            if created:
                created_count += 1

        print(f"Создано книг: {created_count} из {len(books_data)} (остальные уже существовали)")
        print(f"Всего книг в базе: {Book.objects.count()}")
        print("Тестовые данные успешно созданы!")

    except Exception as e:
        print(f"Ошибка при создании тестовых данных: {str(e)}")
        import traceback
        traceback.print_exc()