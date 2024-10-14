import os
import shutil
import pytest
from mobile_generator import MobileGenerator

@pytest.fixture(scope="function")
def setup_output_dir():
    """
    Fixture to create and clean up the output directory for tests.
    This ensures that we start with a clean environment for each test.
    """
    output_dir = "test_output/mobile"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Clean up before the test
    os.makedirs(output_dir)  # Create a fresh directory
    yield output_dir  # Provide the output_dir to the test
    shutil.rmtree(output_dir)  # Clean up after the test


def test_create_mobile_screen_with_title(setup_output_dir):
    """
    Test that MobileGenerator correctly creates a mobile screen with a given title and products.
    """
    output_dir = setup_output_dir
    generator = MobileGenerator(output_dir=output_dir)

    # Define the commands for creating a mobile screen
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'title': 'ShopEasy Mobile',
                'description': 'Browse the latest products',
                'products': 'Smartphone X, Laptop Pro'
            }
        }
    ]

    generator.create_mobile_structure(commands)

    # Check that HomeScreen.js was created
    screen_file = os.path.join(output_dir, 'HomeScreen.js')
    assert os.path.exists(screen_file), "HomeScreen.js was not created."

    # Check the content of the generated HomeScreen.js
    with open(screen_file, 'r') as f:
        content = f.read()
        assert 'ShopEasy Mobile' in content, "Title is missing in HomeScreen.js"
        assert 'Browse the latest products' in content, "Description is missing in HomeScreen.js"
        assert 'Smartphone X' in content, "Product Smartphone X is missing in HomeScreen.js"
        assert 'Laptop Pro' in content, "Product Laptop Pro is missing in HomeScreen.js"


def test_create_mobile_screen_with_empty_products(setup_output_dir):
    """
    Test that MobileGenerator handles empty products attribute correctly.
    """
    output_dir = setup_output_dir
    generator = MobileGenerator(output_dir=output_dir)

    # Define the commands for creating a mobile screen without products
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'title': 'Empty Products Screen',
                'description': 'This screen has no products',
                'products': ''
            }
        }
    ]

    generator.create_mobile_structure(commands)

    # Check that HomeScreen.js was created
    screen_file = os.path.join(output_dir, 'HomeScreen.js')
    assert os.path.exists(screen_file), "HomeScreen.js was not created."

    # Check the content of the generated HomeScreen.js
    with open(screen_file, 'r') as f:
        content = f.read()
        assert 'Empty Products Screen' in content, "Title is missing in HomeScreen.js"
        assert 'This screen has no products' in content, "Description is missing in HomeScreen.js"
        assert 'products' not in content, "Product section should not exist in HomeScreen.js"


def test_create_mobile_screen_with_no_description(setup_output_dir):
    """
    Test that MobileGenerator correctly handles commands without a description.
    """
    output_dir = setup_output_dir
    generator = MobileGenerator(output_dir=output_dir)

    # Define the commands for creating a mobile screen without a description
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'title': 'Screen Without Description',
                'products': 'Product A, Product B'
            }
        }
    ]

    generator.create_mobile_structure(commands)

    # Check that HomeScreen.js was created
    screen_file = os.path.join(output_dir, 'HomeScreen.js')
    assert os.path.exists(screen_file), "HomeScreen.js was not created."

    # Check the content of the generated HomeScreen.js
    with open(screen_file, 'r') as f:
        content = f.read()
        assert 'Screen Without Description' in content, "Title is missing in HomeScreen.js"
        assert 'Product A' in content, "Product A is missing in HomeScreen.js"
        assert 'Product B' in content, "Product B is missing in HomeScreen.js"
        assert 'description' not in content, "Description section should not exist in HomeScreen.js"


def test_create_mobile_screen_invalid_command(setup_output_dir):
    """
    Test that MobileGenerator raises an error when an invalid command is provided.
    """
    output_dir = setup_output_dir
    generator = MobileGenerator(output_dir=output_dir)

    # Define an invalid command (missing title)
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'description': 'A mobile screen without a title'
            }
        }
    ]

    # Expecting an error due to missing title
    with pytest.raises(ValueError, match="Title is required"):
        generator.create_mobile_structure(commands)


def test_overwrite_existing_mobile_screen(setup_output_dir):
    """
    Test that MobileGenerator correctly overwrites existing files if they already exist.
    """
    output_dir = setup_output_dir
    generator = MobileGenerator(output_dir=output_dir)

    # Define the commands for creating a mobile screen
    commands = [
        {
            'command': 'create',
            'object': 'mobile',
            'attributes': {
                'title': 'Overwrite Test',
                'description': 'This file should be overwritten',
                'products': 'Product Z'
            }
        }
    ]

    # First generation
    generator.create_mobile_structure(commands)

    # Modify the command to change the description
    commands[0]['attributes']['description'] = 'This is the updated description'

    # Second generation to overwrite the file
    generator.create_mobile_structure(commands)

    # Check the content of the generated HomeScreen.js
    screen_file = os.path.join(output_dir, 'HomeScreen.js')
    assert os.path.exists(screen_file), "HomeScreen.js was not created."

    with open(screen_file, 'r') as f:
        content = f.read()
        assert 'This is the updated description' in content, "HomeScreen.js was not overwritten correctly."


