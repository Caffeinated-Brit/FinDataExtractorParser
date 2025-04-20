import json
from extractJSON import fix_truncated_json, extract_json

def test_fix_truncated_json_valid():
    """Test fully valid JSON"""
    valid_json = '[{"key": "value"}]'
    assert fix_truncated_json(valid_json) == json.loads(valid_json)

def test_fix_truncated_json_truncated():
    """Test truncated JSON"""
    truncated_json = '[{"key": "value"'
    assert fix_truncated_json(truncated_json) is None, "Should return None for incomplete JSON"

def test_fix_truncated_json_extra_text():
    """Test extra text around JSON, main usage due to AI explanations"""
    extra_text_json = "Some AI response... [ {\"key\": \"value\"} ] More text"
    assert fix_truncated_json(extra_text_json) == [{"key": "value"}]

def test_fix_truncated_json_no_json():
    """Test input without any JSON"""
    assert fix_truncated_json("No JSON here.") is None

def test_extract_json_valid():
    """Test extracting JSON from mixed text"""
    ai_output = "Before JSON {\"test\": 123} After JSON"
    assert extract_json(ai_output) == '{"test": 123}'

def test_extract_json_list():
    """Test extracting JSON when it's a list"""
    ai_output = "Before JSON [1, 2, 3] After JSON"
    assert extract_json(ai_output) == "[1, 2, 3]"

def test_extract_json_no_json():
    """Test when no JSON exists in the text"""
    assert extract_json("No valid JSON here.") is None
