from main import BooksCollector
import pytest
# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.mark.parametrize(
        'name, expected',
        [
            ('', False),
            ('a' * 41, False),
            ('a' * 40, True),
            ('Книга', True),
        ]
    )
    def test_add_new_book_length_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) is expected

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book('Книга')
        collector.add_new_book('Книга')
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_valid(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_book_genre('Книга') == 'Фантастика'

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    def test_get_book_genre_without_genre(self, collector):
        collector.add_new_book('Книга')
        assert collector.get_book_genre('Книга') == ''


    @pytest.mark.parametrize(
        'genre, expected_books',
        [
            ('Фантастика', ['Книга 1']),
            ('Ужасы', ['Книга 2']),
            ('Комедии', []),
        ]
    )
    def test_get_books_with_specific_genre(self, genre, expected_books, collector):
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 2', 'Ужасы')
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_with_specific_genre_invalid_genre(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_books_with_specific_genre('Несуществующий') == []

    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_books_genre() == {'Книга': 'Фантастика'}

    def test_get_books_for_children_excludes_age_rating(self, collector):
        collector.add_new_book('Сказка')
        collector.set_book_genre('Сказка', 'Мультфильмы')
        collector.add_new_book('Ужастик')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.add_new_book('Детектив')
        collector.set_book_genre('Детектив', 'Детективы')
        collector.add_new_book('Комедия')
        collector.set_book_genre('Комедия', 'Комедии')
        assert collector.get_books_for_children() == ['Сказка', 'Комедия']

    def test_add_book_in_favorites_valid(self, collector):
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        assert collector.get_list_of_favorites_books() == ['Книга']

    def test_delete_book_from_favorites_valid(self, collector):
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_empty_initially(self, collector):
        assert collector.get_list_of_favorites_books() == []
