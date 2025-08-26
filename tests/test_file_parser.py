"""
Unit tests for the FileParser class.

Tests file format detection, parsing, and error handling.
"""

import pytest
from crablang.file_parser import FileParser


class TestFileParser:
    """Test suite for FileParser functionality."""

    def setup_method(self):
        """Set up a fresh FileParser instance for each test."""
        self.parser = FileParser()

    def test_detect_tsv_format(self):
        """Test detection of tab-separated format."""
        content = "apple\tred fruit\nbanana\tyellow fruit"
        format_name = self.parser.detect_file_format(content)
        assert format_name == "tsv"

    def test_detect_csv_format(self):
        """Test detection of comma-separated format."""
        content = "apple,red fruit\nbanana,yellow fruit"
        format_name = self.parser.detect_file_format(content)
        assert format_name == "csv"

    def test_detect_semicolon_format(self):
        """Test detection of semicolon-separated format."""
        content = "apple;red fruit\nbanana;yellow fruit"
        format_name = self.parser.detect_file_format(content)
        assert format_name == "semicolon"

    def test_detect_double_hash_format(self):
        """Test detection of double-hash separated format."""
        content = "apple##red fruit\nbanana##yellow fruit"
        format_name = self.parser.detect_file_format(content)
        assert format_name == "double_hash"

    def test_parse_tsv_content(self):
        """Test parsing of TSV content."""
        content = "apple\tred fruit\nbanana\tyellow fruit"
        flashcards = self.parser.parse_content(content, "tsv")

        assert len(flashcards) == 2
        assert flashcards["apple"] == "red fruit"
        assert flashcards["banana"] == "yellow fruit"
        assert self.parser.parse_stats["valid_pairs"] == 2

    def test_parse_with_comments(self):
        """Test parsing content with comments and empty lines."""
        content = "# Fruits\napple\tred fruit\n\n# More fruits\nbanana\tyellow fruit"
        flashcards = self.parser.parse_content(content)

        assert len(flashcards) == 2
        assert (
            self.parser.parse_stats["skipped_lines"] >= 2
        )  # comments + empty lines

    def test_parse_malformed_lines(self):
        """Test parsing content with malformed lines."""
        content = "apple\tred fruit\nmalformed_line\nbanana\tyellow fruit"
        flashcards = self.parser.parse_content(content)

        assert len(flashcards) == 2
        assert (
            self.parser.parse_stats["errors"] == 1
            or self.parser.parse_stats["skipped_lines"] == 1
        )

    def test_validate_flashcards(self):
        """Test flashcard validation."""
        flashcards = {
            "apple": "red fruit",
            "": "empty term",  # invalid
            "term": "",  # invalid
            "x" * 101: "too long term",  # invalid
        }

        issues = self.parser.validate_flashcards(flashcards)
        assert (
            len(issues) == 3
        )  # empty term, empty definition, too long term

    def test_parse_nonexistent_file(self):
        """Test error handling for non-existent files."""
        with pytest.raises(IOError):
            self.parser.read_file_with_encoding_detection("nonexistent.txt")

    def test_get_supported_formats(self):
        """Test retrieval of supported formats."""
        formats = self.parser.get_supported_formats()
        expected_formats = ["tsv", "csv", "semicolon", "double_hash", "pipe"]
        assert all(fmt in formats for fmt in expected_formats)


class TestFileParserIntegration:
    """Integration tests for file parsing."""

    def test_parse_actual_file(self, tmp_path):
        """Test parsing an actual file on disk."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("apple\tred fruit\nbanana\tyellow fruit")

        parser = FileParser()
        content, encoding = parser.read_file_with_encoding_detection(
            str(test_file)
        )
        flashcards = parser.parse_content(content)

        assert len(flashcards) == 2
        assert encoding == "utf-8"
