from unittest.mock import MagicMock
import pytest
from demostration_solution.dao.movie import MovieDAO
from demostration_solution.service.movie import MovieService


@pytest.fixture
def movies_dao():
    dao = MovieDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.create = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movies_service(self, movies_dao):
        self.movies_service = MovieService(dao=movies_dao)

# Тест получения одного
    parameters = (
        (
            1,
            {
                'id': 1,
                'title': 'test_name',
            }
        ),
        (
            2,
            {
                'id': 2,
                'title': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('bid, movie', parameters)
    def test_get_one(self, bid, movie):
        # print(bid, movie)

        # self.movies_service.dao.get_one.return_value = {
        #     'id': 1,
        #     'title': 'test_name'
        # }
        self.movies_service.dao.get_one.return_value = movie

        # assert self.movies_service.get_one(1) == {
        #     'id': 1,
        #     'title': 'test_name'
        # }, "BAD"
        assert self.movies_service.get_one(bid) == movie, "BAD"

# Тест получения всех
    parameters = (
        (
            [
                {
                    'id': 1,
                    'title': 'test_name',
                },
                {
                    'id': 2,
                    'title': 'test_name2',
                }
            ]
        ),
    )

    @pytest.mark.parametrize('movies', parameters)
    def test_get_all(self, movies):
        # print(movies, len(movies))
        self.movies_service.dao.get_all.return_value = movies
        assert self.movies_service.get_all() == movies, "BAD"
        assert len(movies) > 0

# Тест создания
    parameters = (
        (
            {
                'id': 1,
                'title': 'test_name',
            }
        ),
        (
            {
                'id': 2,
                'title': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('movie', parameters)
    def test_create(self, movie):
        print(movie)
        self.movies_service.dao.create.return_value = movie
        assert self.movies_service.create(movie) == movie, "BAD"

# Тест изменения
    parameters = (
        (
            {
                'id': 1,
                'title': 'test_name',
            },
            {
                'id': 1,
                'title': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('movie_initial, movie_new', parameters)
    def test_update(self, movie_initial, movie_new):
        print(movie_initial, movie_new)
        self.movies_service.dao.update.return_value = movie_new
        assert self.movies_service.update(movie_new) == movie_new, 'BAD'
        # Проверка срабатывания вызова один раз
        self.movies_service.dao.update.assert_called_once_with(movie_new)

# Тест удаления
    def test_delete(self):
        self.movies_service.delete(2)
        # Проверка срабатывания вызова один раз
        self.movies_service.dao.delete.assert_called_once_with(2)
