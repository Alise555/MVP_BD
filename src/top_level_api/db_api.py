from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Dict, List, Optional

from abstract.database_api import AbstractDBAPI


class Status(StrEnum):
    OK = 'OK'
    ERROR = 'ERROR'


@dataclass
class ApiResult:
    status: Status
    message: str = ""


@dataclass
class ShowDataBases:
    status: Status
    databases: List[str]
    message: str = ""


class DBAPI(AbstractDBAPI):
    
    def __init__(self, data_root: str | Path = "./data"):
        self.data_root = Path(data_root).resolve()
        self.data_root.mkdir(parents=True, exist_ok=True)
        self.current_db: Optional[str] = None
    
    def valid_name(self, name:str) -> bool:
        return bool(
            name
            and (name[0].isalpha() or name[0] == "_")
            and all(char == "_" or char.isalnum() for char in name[1:])
        )

    def create_database(self, name:str) -> ApiResult:
        if not self.valid_name(name):
            return ApiResult(status=Status.OK, message=f"Нельзя создать такое имя для БД: {name}")
        
        path = self.data_root / name
        try:
            path.mkdir(exist_ok=False)
            (path / "tables").mkdir()
            return ApiResult(status=Status.OK, message=f"БД '{name}' создана")
        except FileExistsError:
            return ApiResult(status=Status.ERROR, message=f"БД '{name}' уже создана")
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка при создание БД: {e}")
    
    def update_database(self, old_name:str, new_name:str) -> ApiResult:
        if not (self.valid_name(old_name) and self.valid_name(new_name)):
            return ApiResult(status=Status.ERROR, message=f"Некорректное имя БД")
            
        old_path = self.data_root / old_name
        new_path = self.data_root / new_name
        if not old_path.exists() or not old_path.is_dir():
            return ApiResult(status=Status.ERROR, message=f"БД '{old_name}' с таким именем не найдена!")
        if new_path.exists():
            return ApiResult(status=Status.ERROR, message=f"БД '{new_name}' с таким именем уже существует")

        try:
            old_path.replace(new_path)
            if self.current_db == old_name:
                self.current_db = new_name
                return ApiResult(status=Status.OK, message=f"БД переименованно '{old_name}' -> '{new_name}'")
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в обновление БД: {e}")
        
    def delete_database(self, name:str) -> ApiResult:
        if not self.valid_name(name):
            return ApiResult(status=Status.OK, message=f"Некорректное имя: {name}")
        
        path = self.data_root / name
        if not path.exists() or not path.is_dir():
            return ApiResult(status=Status.ERROR, message=f"БД '{name}' не нейдена")
        
        try:
            items = sorted(path.rglob("*"), key= lambda n: len(n.parts), reverse=True)
            for item in items:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir:
                    item.rmdir()
            path.rmdir()
            if self.current_db == name:
                self.current_db = None
                return ApiResult(status=Status.OK, message=f"БД '{name}' удаленно")
        except Exception as e:
            return ApiResult(status=Status.ERROR, message=f"Ошибка в удаление: {e}")
    
    def show_databases(self) -> ShowDataBases:
        try:
            dbs = sorted([p.name for p in self.data_root.iterdir() if p.is_dir()])
            return ShowDataBases(status=Status.OK, databases=dbs)
        except Exception as e:
            return ShowDataBases(status=Status.ERROR, databases=[], message=f"Ошибка: {e}")
        
    def use_database(self, name:str) -> ApiResult:
        if not self.valid_name(name):
            return ApiResult(status=Status.OK, message=f"Некорректное имя: {name}")
        
        path = self.data_root / name
        if not path.exists() or not path.is_dir():
            return ApiResult(status=Status.ERROR, message=f"БД'{name}' не найдено")
        
        self.current_db = name
        return ApiResult(status=Status.OK, message=f"Используется БД '{name}'")
    

# if __name__ == "__main__":
#     api = DBAPI("./data")

#     print(api.create_database("test1"))
#     print(api.show_databases())
#     print(api.use_database("test1"))
#     print(api.update_database("test1", "test2"))
#     print(api.show_databases())
#     print(api.delete_database("test2"))
#     print(api.show_databases())

