"""
File parsing module for flashcard application.
This module handles reading and parsing various flashcard file formats
with robust error handling and automatic format detection.
"""

import re
from typing import Dict, List, Tuple, Optional
import chardet


class FileParser:
    """
    Handles parsing of various flashcard file formats.

    This class provides methods to parse content,
    and validate flashcard data.

    Attributes:
        detected_format (Optional[str]): The format
        detected in last parse operation.
        parse_stats (Dict[str, int]): Statistics from the last parse operation.
    """

    def __init__(self):
        """Initialize a new FileParser instance."""
        self.detected_format = None
        self.parse_stats = {
            "total_lines": 0,
            "valid_pairs": 0,
            "skipped_lines": 0,
            "errors": 0,
        }

    def read_file_with_encoding_detection(
        self, file_path: str
    ) -> Tuple[str, str]:
        """
        Read file with automatic encoding detection.

        Args:
            file_path: Path to the file to read

        Returns:
            Tuple[str, str]: (content, encoding) tuple

        Raises:
            IOError: If the file cannot be read

        Example:
            >>> parser = FileParser()
            >>> c, e = parser.read_file_with_encoding_detection("example.txt")
        """
        try:
            with open(file_path, "rb") as file:
                raw_data = file.read()
                encoding_result = chardet.detect(raw_data)
                encoding = encoding_result["encoding"] or "utf-8"

                content = raw_data.decode(encoding, errors="replace")
                return content, encoding

        except Exception as e:
            raise IOError(f"Failed to read file {file_path}: {e}")

    def parse_content(self, content: str, delimiter: str) -> Dict[str, str]:
        """
        Parse content with optional format specification.

        Args:
            content: The content to parse
            delimiter: delimiter for parsing

        Returns:
            Dict[str, str]: Dictionary of term->definition pairs

        Example:
            >>> parser = FileParser()
            >>> content = "apple\tred fruit\nbanana\tyellow fruit"
            >>> flashcards = parser.parse_content(content, delimiter='\t')
            >>> len(flashcards)
            2
        """
        self.parse_stats = {
            "total_lines": 0,
            "valid_pairs": 0,
            "skipped_lines": 0,
            "errors": 0,
        }
        flashcards = {}
        pattern = (
            r"^[^"
            + delimiter
            + r"]+"
            + delimiter
            + r"[^"
            + delimiter
            + r"]+$"
        )

        lines = content.split("\n")
        self.parse_stats["total_lines"] = len(lines)

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                self.parse_stats["skipped_lines"] += 1
                continue
            try:
                if re.match(pattern, line):
                    term, definition = self._parse_line(line, delimiter)
                    if term and definition:
                        if term in flashcards:
                            print(
                                f"Warning: Duplicate term '{term}' on \
                                        line {line_num}"
                            )
                        flashcards[term] = definition
                        self.parse_stats["valid_pairs"] += 1
                    else:
                        self.parse_stats["skipped_lines"] += 1
                else:
                    self.parse_stats["errors"] += 1
                    print(
                        f"Error parsing line {line_num}: {line} - malformed line."
                    )

            except Exception as e:
                self.parse_stats["errors"] += 1
                print(f"Error parsing line {line_num}: {e}")
                continue
        return flashcards

    def _parse_line(
        self, line: str, delimiter: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """Parse a single line based on the specified format."""
        parts = line.split(delimiter, 1)
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return self._parse_fallback(line)

    def _parse_fallback(
        self, line: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """Fallback parsing for malformed lines."""
        # Try multiple space separation
        if "  " in line:  # Double space
            parts = line.split("  ", 1)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()

        # Try colon separation
        if ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()

        # Last resort: split on first whitespace
        parts = line.split(None, 1)
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

        return None, None

    def validate_flashcards(
        self, flashcards: Dict[str, str]
    ) -> List[Tuple[str, str]]:
        """
        Validate parsed flashcards and return issues.

        Args:
            flashcards: Dictionary of term->definition pairs

        Returns:
            List[Tuple[str, str]]: List of (term, issue_description) pairs

        Example:
            >>> parser = FileParser()
            >>> flashcards = {"": "empty term", "term": ""}
            >>> issues = parser.validate_flashcards(flashcards)
            >>> len(issues)
            2
        """
        issues = []

        for term, definition in flashcards.items():
            if not term.strip():
                issues.append((term, "Empty term"))
            if not definition.strip():
                issues.append((term, "Empty definition"))
            if len(term) > 100:
                issues.append((term, "Term too long"))
            if len(definition) > 500:
                issues.append((term, "Definition too long"))

        return issues

    def get_parse_stats(self) -> Dict[str, int]:
        """
        Get statistics from the last parse operation.

        Returns:
            Dict[str, int]: Dictionary with parse statistics
        """
        return self.parse_stats.copy()
