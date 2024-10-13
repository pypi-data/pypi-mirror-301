import pytest
import os
import shutil
from executor import Executor
from web_generator import WebGenerator
from mobile_generator import MobileGenerator
from backend_generator import BackendGenerator

@pytest.fixture(scope="function")
def setup_output_dirs():
    """
    Fixture to create and clean up the output directories for tests.
    This ensures that we start with a clean environment for each test.
    """
    web_output_dir = "test_output/web"
    mobile_output_dir = "test_output/mobile"
    backend_output_dir = "test_output/backend"

    # Clean up and create directories
    for output_dir in [web_output_dir, mobile_output_dir, backend_output_dir]:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)  # Clean up before the test
        os.makedirs(output_dir)  # Create a fresh directory

    yield web_output_dir, mobile_output_dir, backend_output_dir

    # Clean up after the test
    for output_dir in [web_output_dir, mobile_output_dir, backend_output_dir]:
        shutil.rmtree(output_dir)


def test_executor_web_generation(setup_output_dirs):
    """
    Test that the Executor correctly calls the WebGenerator for web commands.
    """
    web_output_dir, _, _ = setup_output_dirs
    executor = Executor()

    # Mock WebGenerator instance to ensure it creates web content
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Test Web Page',
                'description': 'This is a test description for a web page',
                'products': 'Product 1, Product 2'
            }
        }
    ]

    # Execute the commands
    executor.execute(commands)

    # Check if web files are generated
    index_file = os.path.join(web_output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created for the web command."

    # Verify content
    with open(index_file, 'r') as f:
        content = f.read()
        assert 'Test Web Page' in content, "Title is missing in index.html"
        assert 'This is a test description for a web page' in content, "Description is missing in index.html"
        assert 'Product 1' in content, "Product 1 is missing in index.html"
        assert 'Product 2' in content, "Product 2 is missing in index.html"


def test_executor_mobile_generation(setup_output_dirs):
    """
    Test that the Executor correctly calls the MobileGenerator for mobile commands.
    """
    _, mobile_output_dir, _ = setup_output_dirs
    executor = Executor()

    # Mock MobileGenerator instance to ensure it creates mobile content
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'title': 'Test Mobile Screen',
                'description': 'This is a test mobile screen description',
                'products': 'Mobile Product 1, Mobile Product 2'
            }
        }
    ]

    # Execute the commands
    executor.execute(commands)

    # Check if mobile files are generated
    screen_file = os.path.join(mobile_output_dir, 'HomeScreen.js')
    assert os.path.exists(screen_file), "HomeScreen.js was not created for the mobile command."

    # Verify content
    with open(screen_file, 'r') as f:
        content = f.read()
        assert 'Test Mobile Screen' in content, "Title is missing in HomeScreen.js"
        assert 'This is a test mobile screen description' in content, "Description is missing in HomeScreen.js"
        assert 'Mobile Product 1' in content, "Mobile Product 1 is missing in HomeScreen.js"
        assert 'Mobile Product 2' in content, "Mobile Product 2 is missing in HomeScreen.js"


def test_executor_backend_generation(setup_output_dirs):
    """
    Test that the Executor correctly calls the BackendGenerator for backend commands.
    """
    _, _, backend_output_dir = setup_output_dirs
    executor = Executor()

    # Mock BackendGenerator instance to ensure it creates backend content
    commands = [
        {
            'command': 'generate',
            'object': 'backend',
            'attributes': {
                'api': 'products, users, orders'
            }
        }
    ]

    # Execute the commands
    executor.execute(commands)

    # Check if backend files are generated
    assert os.path.exists(os.path.join(backend_output_dir, 'app.py')), "app.py was not created for the backend command."
    assert os.path.exists(os.path.join(backend_output_dir, 'models.py')), "models.py was not created for the backend command."
    assert os.path.exists(os.path.join(backend_output_dir, 'routes.py')), "routes.py was not created for the backend command."
    assert os.path.exists(os.path.join(backend_output_dir, 'setup_db.py')), "setup_db.py was not created for the backend command."

    # Verify content in models.py
    with open(os.path.join(backend_output_dir, 'models.py'), 'r') as f:
        content = f.read()
        assert 'class Product' in content, "Product model is missing in models.py"
        assert 'class User' in content, "User model is missing in models.py"
        assert 'class Order' in content, "Order model is missing in models.py"


def test_executor_invalid_command(setup_output_dirs):
    """
    Test that the Executor raises an error when an invalid command is provided.
    """
    _, _, _ = setup_output_dirs
    executor = Executor()

    # Define an invalid command (unsupported object)
    commands = [
        {
            'command': 'create',
            'object': 'invalid_object',
            'attributes': {
                'title': 'Invalid Object Test'
            }
        }
    ]

    # Expecting an error due to invalid object type
    with pytest.raises(ValueError, match="Unknown object type: invalid_object"):
        executor.execute(commands)


def test_executor_overwrite_files(setup_output_dirs):
    """
    Test that the Executor correctly overwrites existing files if a command is re-executed.
    """
    web_output_dir, _, _ = setup_output_dirs
    executor = Executor()

    # Initial command to create a web page
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Original Web Page',
                'description': 'Original description',
                'products': 'Original Product'
            }
        }
    ]

    # Execute the first command
    executor.execute(commands)

    # Modify the command to change the content
    commands[0]['attributes']['title'] = 'Updated Web Page'
    commands[0]['attributes']['description'] = 'Updated description'
    commands[0]['attributes']['products'] = 'Updated Product'

    # Re-execute the command to overwrite the file
    executor.execute(commands)

    # Verify that the file was overwritten with new content
    index_file = os.path.join(web_output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created."

    with open(index_file, 'r') as f:
        content = f.read()
        assert 'Updated Web Page' in content, "Title was not updated in index.html"
        assert 'Updated description' in content, "Description was not updated in index.html"
        assert 'Updated Product' in content, "Products were not updated in index.html"
