import sqlite3

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


def test_sqlite_store_versions_schema_and_initialization_is_idempotent(tmp_path):
    store = KineticsSQLite(tmp_path / "kinetics.sqlite3")
    store.initialize()
    store.execute_many(
        "INSERT INTO datasets(dataset_id, name) VALUES (?, ?)",
        [("preserved", "Preserve me")],
    )

    # Reinitialization must not destroy data or change the schema version.
    store.initialize()
    with store.session() as connection:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 1
    assert store.fetch_all(
        "SELECT dataset_id, name FROM datasets WHERE dataset_id = ?", ("preserved",)
    ) == [{"dataset_id": "preserved", "name": "Preserve me"}]


def test_sqlite_store_refuses_newer_schema_version(tmp_path):
    import sqlite3
    import pytest

    database = tmp_path / "future.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA user_version = 999")

    store = KineticsSQLite(database)
    with pytest.raises(RuntimeError, match="newer than this Kinetics version supports"):
        store.initialize()


def test_sqlite_store_backup_creates_parent_and_preserves_data(tmp_path):
    store = KineticsSQLite(tmp_path / "source" / "kinetics.sqlite3")
    store.initialize()
    store.execute_many(
        "INSERT INTO datasets(dataset_id, name) VALUES (?, ?)",
        [("backup-test", "Backup test")],
    )

    backup_path = tmp_path / "backups" / "nested" / "backup.sqlite3"
    store.backup(backup_path)

    with sqlite3.connect(backup_path) as connection:
        row = connection.execute(
            "SELECT name FROM datasets WHERE dataset_id = ?", ("backup-test",)
        ).fetchone()
    assert row == ("Backup test",)


def test_sqlite_store_rejects_backup_over_source(tmp_path):
    import pytest

    store = KineticsSQLite(tmp_path / "kinetics.sqlite3")
    store.initialize()
    with pytest.raises(ValueError, match="must differ from the source"):
        store.backup(store.path)


def test_sqlite_store_upgrades_pre_versioned_database_without_losing_data(tmp_path):
    database = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE datasets (
                dataset_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                source TEXT,
                version TEXT,
                license TEXT,
                citation TEXT,
                checksum_sha256 TEXT,
                local_path TEXT,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            "INSERT INTO datasets(dataset_id, name, source) VALUES (?, ?, ?)",
            ("legacy-dataset", "Existing dataset", "legacy-import"),
        )
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 0

    store = KineticsSQLite(database)
    store.initialize()

    assert store.fetch_all(
        "SELECT dataset_id, name, source FROM datasets WHERE dataset_id = ?",
        ("legacy-dataset",),
    ) == [{
        "dataset_id": "legacy-dataset",
        "name": "Existing dataset",
        "source": "legacy-import",
    }]
    with store.session() as connection:
        assert connection.execute("PRAGMA user_version").fetchone()[0] == 1
