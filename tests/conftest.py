import resource


def pytest_generate_tests(metafunc):
    if "data" not in metafunc.fixturenames:
        return

    test_data = resource.get_data(f"{metafunc.function.__name__}_data")
    if test_data is None:
        raise Exception(f"Test data for {metafunc.function.__name__} not found")

    metafunc.parametrize("data", test_data, ids=(data["name"] for data in test_data))
