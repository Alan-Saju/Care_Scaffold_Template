def test_plugin_package_is_importable():
    """Keep a smoke test available without requiring a configured CARE database."""
    import care_connect

    assert care_connect.__name__ == "care_connect"
