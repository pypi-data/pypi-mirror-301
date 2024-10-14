import pytest
from ai_service import AIService


@pytest.fixture(scope="function")
def ai_service():
    """
    Fixture to initialize the AIService for NLP testing.
    """
    return AIService()


def test_parse_simple_web_command(ai_service):
    """
    Test that AIService correctly parses a simple natural language command for web generation.
    """
    command = "Create a homepage with products Smartphone X, Laptop Pro"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'create', "Command should be 'create'"
    assert parsed_command['object'] == 'web', "Object should be 'web'"
    assert parsed_command['attributes']['title'] == 'homepage', "Title should be 'homepage'"
    assert parsed_command['attributes']['products'] == 'Smartphone X, Laptop Pro', "Products should be correctly parsed"


def test_parse_mobile_command_with_description(ai_service):
    """
    Test that AIService correctly parses a natural language command for mobile screen generation.
    """
    command = "Generate a mobile screen called ShopEasy with description 'The best shop app' and products Smartphone X, Laptop Pro"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'create', "Command should be 'create'"
    assert parsed_command['object'] == 'mobile', "Object should be 'mobile'"
    assert parsed_command['attributes']['title'] == 'shopeasy', "Title should be 'shopeasy'"
    assert parsed_command['attributes']['description'] == 'the best shop app', "Description should be correctly parsed"
    assert parsed_command['attributes']['products'] == 'Smartphone X, Laptop Pro', "Products should be correctly parsed"


def test_parse_backend_api_command(ai_service):
    """
    Test that AIService correctly parses a natural language command for backend API generation.
    """
    command = "Create a backend API for products, users, and orders"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'generate', "Command should be 'generate'"
    assert parsed_command['object'] == 'backend', "Object should be 'backend'"
    assert parsed_command['attributes']['api'] == 'products, users, orders', "API entities should be correctly parsed"


def test_parse_command_with_missing_title(ai_service):
    """
    Test that AIService handles cases where the title is missing.
    """
    command = "Create a web page with description 'This is a test page'"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'create', "Command should be 'create'"
    assert parsed_command['object'] == 'web', "Object should be 'web'"
    assert 'title' not in parsed_command['attributes'], "Title should be missing"
    assert parsed_command['attributes']['description'] == 'this is a test page', "Description should be correctly parsed"


def test_parse_invalid_command(ai_service):
    """
    Test that AIService returns None or raises an error for unrecognized commands.
    """
    command = "Fly a rocket to Mars"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['object'] == 'web', "Default object should be 'web'"
    assert parsed_command['attributes'] == {}, "No attributes should be parsed for an invalid command"


def test_parse_complex_web_command(ai_service):
    """
    Test that AIService correctly parses a complex natural language command for web generation with multiple attributes.
    """
    command = "Create a homepage with title 'Welcome to ShopEasy' and description 'The best online store' and products 'Smartphone X, Laptop Pro, Wireless Headphones'"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'create', "Command should be 'create'"
    assert parsed_command['object'] == 'web', "Object should be 'web'"
    assert parsed_command['attributes']['title'] == 'welcome to shopeasy', "Title should be correctly parsed"
    assert parsed_command['attributes']['description'] == 'the best online store', "Description should be correctly parsed"
    assert parsed_command['attributes']['products'] == 'Smartphone X, Laptop Pro, Wireless Headphones', "Products should be correctly parsed"


def test_parse_mobile_command_without_description(ai_service):
    """
    Test that AIService handles a mobile command with no description provided.
    """
    command = "Create a mobile app screen called 'ShopEasy App' with products 'Smartphone X, Laptop Pro'"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'create', "Command should be 'create'"
    assert parsed_command['object'] == 'mobile', "Object should be 'mobile'"
    assert parsed_command['attributes']['title'] == 'shopeasy app', "Title should be correctly parsed"
    assert 'description' not in parsed_command['attributes'], "Description should be missing"
    assert parsed_command['attributes']['products'] == 'Smartphone X, Laptop Pro', "Products should be correctly parsed"


def test_parse_backend_command_with_no_entities(ai_service):
    """
    Test that AIService handles a backend API generation command with no entities.
    """
    command = "Generate a backend API"
    parsed_command = ai_service.parse_natural_language(command)

    assert parsed_command['command'] == 'generate', "Command should be 'generate'"
    assert parsed_command['object'] == 'backend', "Object should be 'backend'"
    assert 'api' not in parsed_command['attributes'], "API entities should be missing if not provided"

