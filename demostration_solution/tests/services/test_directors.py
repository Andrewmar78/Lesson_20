from unittest.mock import MagicMock
import pytest
from demostration_solution.dao.director import DirectorDAO
from demostration_solution.dao.model.director import Director
from demostration_solution.service.director import DirectorService

# Первый вариант всех тестов
# @pytest.fixture
# def directors_dao_var1():
#     dao = DirectorDAO(None)
#     first_dir = Director(id=1, name="test_name")
#     second_dir = Director(id=2, name="test_name2")
#     directors_dao_var1.get_one = MagicMock(return_value=first_dir)
#     directors_dao_var1.get_all = MagicMock(return_value=[first_dir, second_dir])
#     directors_dao_var1.create = MagicMock(return_value=Director(id=2))
#     directors_dao_var1.update = MagicMock()
#     directors_dao_var1.delete = MagicMock()
#     return directors_dao_var1


# Тесты все
# class TestDirectorService:
#     @pytest.fixture(autouse=True)
#     def directors_service(self, directors_dao_var1):
#         self.directors_service = DirectorService(dao=directors_dao_var1)
#
#     def test_get_one(self):
#         director = self.directors_service.get_one(1)
#         assert director is not None
#         assert director.id is not None
#
#     def test_get_all(self):
#         director = self.directors_service.get_all()
#         assert len(director) > 0
#
#     def test_create(self):
#         director_d = {"name": "test_name"}
#         director = self.directors_service.create(director_d)
#         assert director.id is not None
#
#     def test_update(self):
#         director_d = {"name": "test_name2"}
#         self.directors_service.update(director_d)
#
#     def test_delete(self):
#         self.directors_service.delete(1)


# Второй вариант
@pytest.fixture
def directors_dao():
    dao = DirectorDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.create = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def directors_service(self, directors_dao):
        self.directors_service = DirectorService(dao=directors_dao)

# Тест получения одного (вар.2)
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

    @pytest.mark.parametrize('bid, director', parameters)
    def test_get_one(self, bid, director):
        # print(bid, director)

        # self.directors_service.dao.get_one.return_value = {
        #     'id': 1,
        #     'title': 'test_name'
        # }
        self.directors_service.dao.get_one.return_value = director

        # assert self.directors_service.get_one(1) == {
        #     'id': 1,
        #     'title': 'test_name'
        # }, "BAD"
        assert self.directors_service.get_one(bid) == director, "BAD"

# Тест получения всех
    parameters = (
        (
            [
                {
                    'id': 1,
                    'name': 'test_name',
                },
                {
                    'id': 3,
                    'name': 'test_name3',
                },
                {
                    'id': 2,
                    'name': 'test_name2',
                }
            ]
        ),
    )

    @pytest.mark.parametrize('directors', parameters)
    def test_get_all(self, directors):
        # print(directors, len(directors))
        self.directors_service.dao.get_all.return_value = directors
        assert self.directors_service.get_all() == directors, "BAD"
        assert len(directors) > 0

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

    @pytest.mark.parametrize('director', parameters)
    def test_create(self, director):
        # print(director)
        self.directors_service.dao.create.return_value = director
        assert self.directors_service.create(director) == director, "BAD"

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

    @pytest.mark.parametrize('director_initial, director_new', parameters)
    def test_update(self, director_initial, director_new):
        # print(director_initial, director_new)
        self.directors_service.dao.update.return_value = director_new
        assert self.directors_service.update(director_new) == director_new, 'BAD'
        self.directors_service.dao.update.assert_called_once_with(director_new)

# Тест удаления
    def test_delete(self):
        self.directors_service.delete(2)
        self.directors_service.dao.delete.assert_called_once_with(2)
