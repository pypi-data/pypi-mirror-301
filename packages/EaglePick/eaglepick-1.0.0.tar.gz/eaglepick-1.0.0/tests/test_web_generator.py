import os
import shutil
import pytest
from web_generator import WebGenerator

@pytest.fixture(scope="function")
def setup_output_dir():
    """
    Fixture to create and clean up the output directory for tests.
    This ensures that we start with a clean environment for each test.
    """
    output_dir = "test_output/web"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Clean up before the test
    os.makedirs(output_dir)  # Create a fresh directory
    yield output_dir  # Provide the output_dir to the test
    shutil.rmtree(output_dir)  # Clean up after the test


def test_create_web_structure_with_title(setup_output_dir):
    """
    Test that WebGenerator correctly creates a web page with a given title.
    """
    output_dir = setup_output_dir
    generator = WebGenerator(output_dir=output_dir)

    # Define the commands for creating a web page
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Test Home Page',
                'description': 'Welcome to the test home page',
                'products': 'Product A, Product B'
            }
        }
    ]

    generator.create_web_structure(commands)

    # Check that index.html was created
    index_file = os.path.join(output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created."

    # Check the content of the generated index.html
    with open(index_file, 'r') as f:
        content = f.read()
        assert '<title>Test Home Page</title>' in content, "Title is missing in index.html"
        assert 'Welcome to the test home page' in content, "Description is missing in index.html"
        assert 'Product A' in content, "Product A is missing in index.html"
        assert 'Product B' in content, "Product B is missing in index.html"


def test_create_web_structure_with_empty_products(setup_output_dir):
    """
    Test that WebGenerator handles empty products attribute correctly.
    """
    output_dir = setup_output_dir
    generator = WebGenerator(output_dir=output_dir)

    # Define the commands with an empty products list
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Test Page Without Products',
                'description': 'A page without products',
                'products': ''
            }
        }
    ]

    generator.create_web_structure(commands)

    # Check that index.html was created
    index_file = os.path.join(output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created."

    # Check the content of the generated index.html
    with open(index_file, 'r') as f:
        content = f.read()
        assert '<title>Test Page Without Products</title>' in content, "Title is missing in index.html"
        assert 'A page without products' in content, "Description is missing in index.html"
        assert 'products' not in content, "Products section should be missing in index.html"


def test_create_web_structure_with_no_description(setup_output_dir):
    """
    Test that WebGenerator correctly handles commands without a description.
    """
    output_dir = setup_output_dir
    generator = WebGenerator(output_dir=output_dir)

    # Define the commands with no description
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Page Without Description',
                'products': 'Product X, Product Y'
            }
        }
    ]

    generator.create_web_structure(commands)

    # Check that index.html was created
    index_file = os.path.join(output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created."

    # Check the content of the generated index.html
    with open(index_file, 'r') as f:
        content = f.read()
        assert '<title>Page Without Description</title>' in content, "Title is missing in index.html"
        assert 'Product X' in content, "Product X is missing in index.html"
        assert 'Product Y' in content, "Product Y is missing in index.html"
        assert 'description' not in content, "Description section should be missing in index.html"


def test_create_web_structure_invalid_command(setup_output_dir):
    """
    Test that WebGenerator raises an error when an invalid command is provided.
    """
    output_dir = setup_output_dir
    generator = WebGenerator(output_dir=output_dir)

    # Define an invalid command (missing title)
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'description': 'A page without a title'
            }
        }
    ]

    # Expecting an error due to missing title
    with pytest.raises(ValueError, match="Title is required"):
        generator.create_web_structure(commands)


def test_overwrite_existing_files(setup_output_dir):
    """
    Test that WebGenerator correctly overwrites existing files if they already exist.
    """
    output_dir = setup_output_dir
    generator = WebGenerator(output_dir=output_dir)

    # Define the commands for creating a web page
    commands = [
        {
            'command': 'create',
            'object': 'web',
            'attributes': {
                'title': 'Test Overwrite',
                'description': 'This file should be overwritten',
                'products': 'Product Z'
            }
        }
    ]

    # First generation
    generator.create_web_structure(commands)

    # Modify the command to change the description
    commands[0]['attributes']['description'] = 'This is the updated description'

    # Second generation to overwrite the file
    generator.create_web_structure(commands)

    # Check the content of the generated index.html
    index_file = os.path.join(output_dir, 'index.html')
    assert os.path.exists(index_file), "index.html was not created."

    with open(index_file, 'r') as f:
        content = f.read()
        assert 'This is the updated description' in content, "index.html was not overwritten correctly."


