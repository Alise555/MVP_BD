from src.models.dynamic_model import create_dynamic_model


def test_create_dynamic_model_with_field_types():
    field_types = {
        "username":  str,
        "age":  int,
    }
    data = {
        "username":  "Misha",
        "age":  25,
    } 
    Model = create_dynamic_model(field_types=field_types)
    user = Model(**data)
    assert isinstance(user.age, int)
    assert isinstance(user.username, str)


def test_create_dynamic_model_with_conditions():
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
    Model = create_dynamic_model(conditions=conditions)
    user = Model(username="Misha", age=25)
    assert isinstance(user.age, int)
    try:
        user2 = Model(username="Misha", age="trtr")
        assert isinstance(user2.age, int)
    except Exception as e:
        print(f"Данные введены с ошибкой. Проверьте условия: {e}")

