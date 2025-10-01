from pydantic import BaseModel, create_model, Field
from typing import Any, Type, Dict


def create_dynamic_model(
    conditions: Dict[str, Any],
    model_name: str = "BaseModel"
) -> Type[BaseModel]:
    """
    Создаёт динамическую Pydantic-модель на основе данных или заданных типов.

    Args:
        model_name: Имя создаваемой модели (по умолчанию "BaseModel").
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

    for field_name, config in conditions.items():
        if isinstance(config, dict):
            field_type = config.pop("type", Any)
            field_info = Field(**config) if config else ...
            fields[field_name] = (field_type, field_info)
        else:
            fields[field_name] = (config, Field())

    dynamic_model = create_model(model_name, **fields)

    return dynamic_model


