from scripts.check_android_config import validate_android_config


def test_android_offline_and_build_first_guardrails() -> None:
    assert validate_android_config() == []
