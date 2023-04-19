from multiprocessing import connection
from unittest import TestCase

from bank.models import Account


def log_sql(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print("Raw SQL was:", connection.queries, "Number of SQL queries: ", len(connection.queries))
    return wrapper

class Learn_Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        author_obj = [
            Account(midle_name='Jack', surname='London'),
            Account(name='Lev', surname='Tolsoy'),
            Account(name='Victor', surname='Hugo'),
        ]

        Author.objects.bulk_create(author_obj)
        Book.objects.bulk_create(book_obj)
        Address.objects.bulk_create(address_obj)
        Language.objects.bulk_create(lang_obj)
        books = Book.objects.all()
        languages = Language.objects.all()
        for lang in languages:
            lang.books.add(*books)
        connection.force_debug_cursor = True

@log_sql
def test_generator_at_query(self):
    for entry in Book.objects.iterator(chunk_size=1):
        return entry.title