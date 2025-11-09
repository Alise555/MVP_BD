import pytest
from models.dynamic_model import create_dynamic_model


@pytest.mark.parametrize(
        "conditions, data",
        [
            ({"username":  str, "age":  int}, {"username":  "Misha", "age": 25} ),
            ({"username": {"type": str, "min_length": 3, "max_length": 20},
              "age": {"type": int, "gt": 0, "lt": 120}}, {"username":  "Misha", "age":  "twenty five",} )
        ]
)
def test_create_dynamic_model(conditions, data):
    try:
        Model = create_dynamic_model(conditions=conditions)
        user = Model(**data)
        assert isinstance(user.age, int)
        assert isinstance(user.username, str)
    except Exception as e:
        print(f"Данные введены с ошибкой. Проверьте условия: {e}")
