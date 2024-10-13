import os
import shutil
import pytest
from backend_generator import BackendGenerator

@pytest.fixture(scope="function")
def setup_output_dir():
    """
    Fixture to create and clean up the output directory for tests.
    This ensures that we start with a clean environment for each test.
    """
    output_dir = "test_output/backend"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Clean up before the test
    os.makedirs(output_dir)  # Create a fresh directory
    yield output_dir  # Provide the output_dir to the test
    shutil.rmtree(output_dir)  # Clean up after the test


def test_generate_backend_with_api_entities(setup_output_dir):
    """
    Test that BackendGenerator correctly generates backend files for given API entities.
    """
    output_dir = setup_output_dir
    generator = BackendGenerator(output_dir=output_dir)

    # Define the commands for generating backend API
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {
                'api': 'products, users, orders'
            }
        }
    ]

    generator.create_backend_structure(commands)

    # Check that essential files are created
    assert os.path.exists(os.path.join(output_dir, 'app.py')), "app.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'models.py')), "models.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'routes.py')), "routes.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'setup_db.py')), "setup_db.py was not created."

    # Verify contents of models.py
    with open(os.path.join(output_dir, 'models.py'), 'r') as f:
        content = f.read()
        assert 'class Product' in content, "Product model is missing in models.py"
        assert 'class User' in content, "User model is missing in models.py"
        assert 'class Order' in content, "Order model is missing in models.py"

    # Verify contents of routes.py
    with open(os.path.join(output_dir, 'routes.py'), 'r') as f:
        content = f.read()
        assert 'app.route(\'/products\'' in content, "Product route is missing in routes.py"
        assert 'app.route(\'/users\'' in content, "User route is missing in routes.py"
        assert 'app.route(\'/orders\'' in content, "Order route is missing in routes.py"


def test_generate_backend_with_no_entities(setup_output_dir):
    """
    Test that BackendGenerator handles an empty entities attribute correctly.
    """
    output_dir = setup_output_dir
    generator = BackendGenerator(output_dir=output_dir)

    # Define the commands for generating a backend with no API entities
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {
                'api': ''
            }
        }
    ]

    generator.create_backend_structure(commands)

    # Check that essential files are created
    assert os.path.exists(os.path.join(output_dir, 'app.py')), "app.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'models.py')), "models.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'routes.py')), "routes.py was not created."
    assert os.path.exists(os.path.join(output_dir, 'setup_db.py')), "setup_db.py was not created."

    # Verify that no API entities are included in models.py
    with open(os.path.join(output_dir, 'models.py'), 'r') as f:
        content = f.read()
        assert 'class ' not in content, "No models should be present in models.py if no entities are provided."


def test_generate_backend_invalid_command(setup_output_dir):
    """
    Test that BackendGenerator raises an error when an invalid command is provided.
    """
    output_dir = setup_output_dir
    generator = BackendGenerator(output_dir=output_dir)

    # Define an invalid command (missing API entities)
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {}
        }
    ]

    # Expecting an error due to missing 'api' attribute
    with pytest.raises(ValueError, match="API entities are required"):
        generator.create_backend_structure(commands)


def test_overwrite_existing_backend_files(setup_output_dir):
    """
    Test that BackendGenerator correctly overwrites existing files if they already exist.
    """
    output_dir = setup_output_dir
    generator = BackendGenerator(output_dir=output_dir)

    # Define the commands for generating backend API
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {
                'api': 'products, users'
            }
        }
    ]

    # First generation
    generator.create_backend_structure(commands)

    # Modify the command to add more entities
    commands[0]['attributes']['api'] = 'products, users, orders'

    # Second generation to overwrite the files
    generator.create_backend_structure(commands)

    # Verify that the updated entities are included in models.py
    with open(os.path.join(output_dir, 'models.py'), 'r') as f:
        content = f.read()
        assert 'class Product' in content, "Product model is missing in models.py"
        assert 'class User' in content, "User model is missing in models.py"
        assert 'class Order' in content, "Order model is missing in models.py"


def test_generate_setup_db_script(setup_output_dir):
    """
    Test that BackendGenerator correctly generates the setup_db.py script.
    """
    output_dir = setup_output_dir
    generator = BackendGenerator(output_dir=output_dir)

    # Define the commands for generating backend API
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {
                'api': 'products, users'
            }
        }
    ]

    generator.create_backend_structure(commands)

    # Verify that setup_db.py was created
    setup_db_file = os.path.join(output_dir, 'setup_db.py')
    assert os.path.exists(setup_db_file), "setup_db.py was not created."

    # Check the content of setup_db.py
    with open(setup_db_file, 'r') as f:
        content = f.read()
        assert 'db.create_all()' in content, "Database creation is missing in setup_db.py"
        assert 'app.app_context()' in content, "App context setup is missing in setup_db.py"


