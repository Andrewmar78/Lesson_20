from unittest.mock import MagicMock
import pytest
from demostration_solution.dao.genre import GenreDAO
from demostration_solution.service.genre import GenreService


@pytest.fixture
def genres_dao():
    dao = GenreDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.create = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genres_service(self, genres_dao):
        self.genres_service = GenreService(dao=genres_dao)

# Тест получения одного
    parameters = (
        (
            1,
            {
                'id': 1,
                'name': 'test_name',
            }
        ),
        (
            2,
            {
                'id': 2,
                'name': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('bid, genre', parameters)
    def test_get_one(self, bid, genre):
        # print(bid, genre)
        self.genres_service.dao.get_one.return_value = genre
        assert self.genres_service.get_one(bid) == genre, "BAD"

# Тест получения всех
    parameters = (
        (
            [
                {
                    'id': 1,
                    'name': 'test_name',
                },
                {
                    'id': 2,
                    'name': 'test_name2',
                },
                {
                    'id': 3,
                    'name': 'test_name3',
                }
            ]
        ),
    )

    @pytest.mark.parametrize('genres', parameters)
    def test_get_all(self, genres):
        # print(genres, len(genres))
        self.genres_service.dao.get_all.return_value = genres
        assert self.genres_service.get_all() == genres, "BAD"
        assert len(genres) > 0

# Тест создания
    parameters = (
        (
            {
                'id': 1,
                'name': 'test_name',
            }
        ),
        (
            {
                'id': 2,
                'name': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('genre', parameters)
    def test_create(self, genre):
        # print(genre)
        self.genres_service.dao.create.return_value = genre
        assert self.genres_service.create(genre) == genre, "BAD"

# Тест изменения
    parameters = (
        (
            {
                'id': 1,
                'name': 'test_name',
            },
            {
                'id': 1,
                'name': 'test_name2',
            }
        ),
    )

    @pytest.mark.parametrize('genre_initial, genre_new', parameters)
    def test_update(self, genre_initial, genre_new):
        # print(director_initial, director_new)
        self.genres_service.dao.update.return_value = genre_new
        assert self.genres_service.update(genre_new) == genre_new, 'BAD'
        self.genres_service.dao.update.assert_called_once_with(genre_new)

# Тест удаления
    def test_delete(self):
        self.genres_service.delete(2)
        self.genres_service.dao.delete.assert_called_once_with(2)
