from pydantic import BaseModel, create_model, Field
from typing import Any, Type, Dict, Optional


def create_dynamic_model(
    model_name: str = "BaseModel",
    field_types: Optional[Dict[str, type]] = None,
    conditions: Optional[Dict[str, Any]] = None
) -> Type[BaseModel]:
    """
    Создаёт динамическую Pydantic-модель на основе данных или заданных типов.

    Args:
        model_name: Имя создаваемой модели (по умолчанию "BaseModel").
        field_types: Словарь с типами данных.
        conditions: Словарь с ограничениями для полей в формате:
            {
                "field_name": {
                    "type": <тип>,  # обязательно
                    "min_length": 5,  # опционально
                    "max_length": 10,
                    "gt": 0,
                    "regex": r"^[a-z]+$",
                    ...
                }
            }

    Returns:
        Класс динамической Pydantic-модели.
    """
    fields = {}

    if conditions:
        for field_name, config in conditions.items():
            field_type = config.pop("type", Any) 
            field_info = Field(**config) if config else ...
            fields[field_name] = (field_type, field_info)

    else:
        for field_name, field_type in field_types.items():
            fields[field_name] = (field_type, Field())

    dynamic_model = create_model(model_name, **fields)

    return dynamic_model


conditions = {
    "username": {
        "type": str,
        "min_length": 3,
        "max_length": 20,
    },
    "age": {
        "type": int,
        "gt": 0,
        "lt": 120
    }
}
fi = {
    "username":  str,
    "age":  int,
}
data_h = {
    "username":  "hfgejfge",
    "age":  78,
}
daaaa = ({
    "username":  "hfgejfge",
    "age":  78,
    "height": 12
}, {
    "username":  123,
    "age":  7,
    "height": 34
})
try:
    UserModel = create_dynamic_model(conditions=conditions)
    user = UserModel(username="asfew", age="12") 
    print(type(user.age))
    Model = create_dynamic_model(field_types=fi)
    user = Model(**data_h) 
    print(user.age)
except Exception as e:
    print(f"Данные введены с ошибкой. Проверьте условия: {e}")


data_t = {
    "username":  "hfsehrtyr"
}
mmmm = []
result = []
columns = ["age", "height"]
UserModel = create_dynamic_model(conditions=conditions)
for row in daaaa:
    try: 
        UserModel(**row)
        mmmm.append(row)
    except Exception:
        continue
print(mmmm)
for row in mmmm:
    for col in columns:
        result.append({key: row[key] for key in columns if key in row})
print(result)