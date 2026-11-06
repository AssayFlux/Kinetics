from kinetics_core.storage import KineticsSQLite


def test_sqlite_store_initializes_and_round_trips(tmp_path):
    store = KineticsSQLite(tmp_path / "kinetics.sqlite3")
    store.initialize()

    changed = store.execute_many(
        "INSERT INTO datasets(dataset_id, name, source) VALUES (?, ?, ?)",
        [("test-dataset", "Test dataset", "unit-test")],
    )
    assert changed == 1
    rows = store.fetch_all(
        "SELECT dataset_id, name, source FROM datasets WHERE dataset_id = ?",
        ("test-dataset",),
    )
    assert rows == [{
        "dataset_id": "test-dataset",
        "name": "Test dataset",
        "source": "unit-test",
    }]


def test_sqlite_store_rolls_back_failed_transaction(tmp_path):
    store = KineticsSQLite(tmp_path / "kinetics.sqlite3")
    store.initialize()

    try:
        with store.transaction() as connection:
            connection.execute(
                "INSERT INTO datasets(dataset_id, name) VALUES (?, ?)",
                ("rolled-back", "Should not persist"),
            )
            raise RuntimeError("force rollback")
    except RuntimeError:
        pass

    assert store.fetch_all(
        "SELECT dataset_id FROM datasets WHERE dataset_id = ?",
        ("rolled-back",),
    ) == []
