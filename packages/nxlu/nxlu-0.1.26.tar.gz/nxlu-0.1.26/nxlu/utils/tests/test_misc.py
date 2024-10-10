import pytest

from nxlu.utils.misc import most_common_element, sanitize_input, scrub_braces


@pytest.fixture
def sample_context():
    return {
        "name": "John Doe",
        "description": "{A sample description}",
        "nested": {"message": "{A message with {nested} braces}"},
        "tags": ["{tag1}", "{tag2}", "{tag3}"],
        "numbers": (1, 2, "{3}", 4),
        "empty_dict": {},
    }


# Test for sanitize_input
@pytest.mark.parametrize(
    ("query", "expected_output"),
    [
        ("<script>alert('XSS')</script>", "scriptalert('XSS')script"),
        ("<<>>", ""),
        ("<tag>", "tag"),
        ("normal query", "normal query"),
        ("", ""),
    ],
)
def test_sanitize_input(query, expected_output):
    assert sanitize_input(query) == expected_output


# Test for most_common_element
@pytest.mark.parametrize(
    ("elements", "expected_output"),
    [
        ([1, 2, 2, 3], 2),  # Normal case with most common element
        (["apple", "banana", "apple"], "apple"),  # Most common string
        ([True, False, True], True),  # Booleans
        ([None, None, None], None),  # All None
        ([], None),  # Empty list
        ([1, 1, 2, 2], 1),  # Equal frequency, returns the first
        (["single"], "single"),  # Single element list
    ],
)
def test_most_common_element(elements, expected_output):
    assert most_common_element(elements) == expected_output


# Test for edge cases in most_common_element
def test_most_common_element_invalid_input():
    with pytest.raises(TypeError):
        most_common_element(1234)  # Not a list input


# Test for scrub_braces
@pytest.mark.parametrize(
    ("context", "expected_output"),
    [
        # Basic test cases
        ({"key": "{value}"}, {"key": "value"}),
        ({"key": "no_braces"}, {"key": "no_braces"}),  # No braces to scrub
        ({"key": "{{double braces}}"}, {"key": "{{double braces}}"}),  # Double braces
        ({"key": "{}"}, {"key": ""}),  # Empty braces
        # Nested dictionary
        ({"key": {"subkey": "{subvalue}"}}, {"key": {"subkey": "subvalue"}}),
        # List inside dictionary
        ({"key": ["{listitem1}", "{listitem2}"]}, {"key": ["listitem1", "listitem2"]}),
        # Tuple inside dictionary
        (
            {"key": ("{tupleitem1}", "{tupleitem2}")},
            {"key": ("tupleitem1", "tupleitem2")},
        ),
        # Set inside dictionary
        ({"key": {"{setitem1}", "{setitem2}"}}, {"key": {"setitem1", "setitem2"}}),
    ],
)
def test_scrub_braces(context, expected_output):
    assert scrub_braces(context) == expected_output


# Test for scrub_braces using fixture
def test_scrub_braces_complex_structure(sample_context):
    expected_output = {
        "name": "John Doe",
        "description": "A sample description",
        "nested": {"message": "A message with nested braces"},
        "tags": ["tag1", "tag2", "tag3"],
        "numbers": (1, 2, "3", 4),
        "empty_dict": {},
    }
    assert scrub_braces(sample_context) == expected_output


# Edge case for empty dictionary in scrub_braces
def test_scrub_braces_empty():
    assert scrub_braces({}) == {}


# Test invalid inputs for scrub_braces
@pytest.mark.parametrize(
    "invalid_context",
    [
        None,
        1234,
        "string",
        [1, 2, 3],  # Non-dict input
    ],
)
def test_scrub_braces_invalid_input(invalid_context):
    # Should return an empty dictionary and log a warning
    assert scrub_braces(invalid_context) == {}
