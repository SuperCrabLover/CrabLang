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

    def test_parse_tsv_content(self):
        """Test parsing of TSV content."""
        content = (
            "apple\tred fruit\nbanana\tyellow fruit\norange\torange fruit"
        )
        flashcards = self.parser.parse_content(content, "\t")

        assert len(flashcards) == 3
        assert flashcards["apple"] == "red fruit"
        assert flashcards["banana"] == "yellow fruit"
        assert self.parser.parse_stats["valid_pairs"] == 3

    def test_parse_tsv_content_with_comments(self):
        """Test parsing content with comments and empty lines."""
        content = "# Fruits\napple\tred fruit\n\n# More fruits\nbanana\tyellow fruit"
        flashcards = self.parser.parse_content(content, "\t")

        assert len(flashcards) == 2
        assert (
            self.parser.parse_stats["skipped_lines"] >= 2
        )  # comments + empty lines

    def test_parse_tsv_content_malformed_lines(self):
        """Test parsing content with malformed lines."""
        content = "apple\tred fruit\nmalformed_line\nbanana\tyellow fruit"
        flashcards = self.parser.parse_content(content, "\t")

        assert len(flashcards) == 2
        assert (
            self.parser.parse_stats["errors"] == 1
            and self.parser.parse_stats["skipped_lines"] == 0
        )

    @pytest.mark.parametrize("delimeter", ["\t", ",", ";", "##"])
    def test_parse_content_with_comments_malformed_lines(self, delimeter):
        """Test parsing content with comments and empty lines."""
        content = f"\nmalformed_line# Fruits\napple{delimeter}red fruit\n\n# More fruits\nbanana{delimeter}yellow fruit\nmalformed_line"
        flashcards = self.parser.parse_content(content, delimeter)
        assert len(flashcards) == 2
        assert (
            self.parser.parse_stats["skipped_lines"] >= 2
        )  # comments + empty lines

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


class TestFileParserIntegration:
    """Integration tests for file parsing."""

    def test_parse_tsv_content_actual_file(self, tmp_path):
        """Test parsing an actual file on disk."""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("apple\tred fruit\nbanana\tyellow fruit")

        parser = FileParser()
        content, encoding = parser.read_file_with_encoding_detection(
            str(test_file)
        )
        flashcards = parser.parse_content(content, "\t")

        assert len(flashcards) == 2
        assert encoding in ["utf-8", "ascii"]
