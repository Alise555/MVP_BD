import json
from .storage import Storage


storage = Storage()

def test_create_metadata(tmp_path):
    
    metadata = {"a": 1, "b": 2}
    metadata_file_path = tmp_path / "meta.json"

    storage.create_metadata(metadata, metadata_file_path)

    assert metadata_file_path.exists()

    with open(metadata_file_path, "r") as f:
        saved = json.load(f)
    
    assert saved == metadata
    
def test_update_metadata(tmp_path):
    
    metadata = {"a": 1, "b": 2}
    metadata_file_path = tmp_path / "meta.json"

    storage.create_metadata(metadata, metadata_file_path)

    assert metadata_file_path.exists()

    with open(metadata_file_path, "r") as f:
        saved = json.load(f)
    
    assert saved == metadata
    
def test_get_metadata(tmp_path):
    
    metadata = {"a": 1, "b": 2}
    metadata_file_path = tmp_path / "meta.json"
    
    with open(metadata_file_path, "w") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    assert storage.get_metadata(metadata_file_path) == metadata

    
def test_delete_metadata(tmp_path):
    
    metadata = {"a": 1, "b": 2}
    metadata_file_path = tmp_path / "meta.json"
    
    with open(metadata_file_path, "w") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    storage.delete_metadata(metadata_file_path)

    assert not metadata_file_path.exists()