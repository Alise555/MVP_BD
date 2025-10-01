import pytest
from unittest.mock import Mock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from enum_status import Status
from database_manager.DBManager import DBManager


@pytest.fixture
def mock_storage():
    storage = Mock()
    storage.create_folder.return_value = Status.OK
    storage.delete_folder.return_value = Status.OK
    storage.rename_folder.return_value = Status.OK
    storage.update_metadata.return_value = Status.OK
    storage.create_metadata.return_value = Status.OK
    storage.get_metadata.return_value = Status.OK
    return storage


@pytest.fixture
def db_manager(mock_storage):
    return DBManager(storage=mock_storage)


def test_create_db_success(db_manager, mock_storage):
    result = db_manager.create_db("test_db")
    assert result == Status.OK
    assert "test_db" in db_manager._databases
    mock_storage.create_folder.assert_called_once_with("test_db")


def test_create_db_already_exists(db_manager, mock_storage):
    db_manager._databases.add("test_db")
    result = db_manager.create_db("test_db")
    assert result == Status.ERROR
    mock_storage.create_folder.assert_not_called()


def test_delete_db_success(db_manager, mock_storage):
    db_manager._databases.add("test_db")
    result = db_manager.delete_db("test_db")
    assert result == Status.OK
    assert "test_db" not in db_manager._databases
    mock_storage.delete_folder.assert_called_once_with("test_db")


def test_delete_db_not_found(db_manager, mock_storage):
    result = db_manager.delete_db("nonexistent_db")
    assert result == Status.ERROR
    mock_storage.delete_folder.assert_not_called()


def test_update_db_success(db_manager, mock_storage):
    db_manager._databases.add("old_db")
    result = db_manager.update_db("old_db", "new_db")
    assert result == Status.OK
    assert "old_db" not in db_manager._databases
    assert "new_db" in db_manager._databases
    mock_storage.rename_folder.assert_called_once_with("old_db", "new_db")


def test_update_db_not_found(db_manager, mock_storage):
    result = db_manager.update_db("old_db", "new_db")
    assert result == Status.ERROR
    mock_storage.rename_folder.assert_not_called()


def test_use_database_success(db_manager, mock_storage):
    db_manager._databases.add("test_db")
    db_manager.use_database("test_db")
    assert db_manager.current_database() == "test_db"


def test_use_database_not_found(db_manager, mock_storage):
    result = db_manager.use_database("nonexistent_db")
    assert result == Status.ERROR


def test_show_database(db_manager, mock_storage):
    db_manager._databases.update(["db1", "db2"])
    result = db_manager.show_database()
    assert "db1" in result
    assert "db2" in result
    assert len(result) == 2


def test_current_database_default(db_manager):
    assert db_manager.current_database() == ""
