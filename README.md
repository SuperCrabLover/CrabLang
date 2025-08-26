# CrabLang App

A powerful command-line flashcard application for efficient learning and memorization. Supports multiple file formats and study modes.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/packaging-poetry-cyan)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📁 **Multiple File Formats**: Support for TSV, CSV, custom delimiters (;, ##, |)
- 🎯 **Smart Format Detection**: Automatic detection of file formats
- 📊 **Study Modes**: Multiple learning modes (review, quiz, spaced repetition)
- 📈 **Progress Tracking**: Track your learning progress and identify weak areas
- 🔄 **Reverse Learning**: Study from term to definition or definition to term
- 💾 **Encoding Support**: Automatic encoding detection for international characters
- 🎨 **Rich CLI**: Beautiful command-line interface with progress indicators

## Installation

### Using Poetry 

```bash
# Clone the repository
git clone https://github.com/SuperCrabLover/CrabLang.git
cd CrabLang

# Install with Poetry
poetry install

# Install with development dependencies
poetry install --with dev
```

## Quick Start

1. **Create a flashcard file**:
```bash
# Create a simple vocabulary list
cat > vocabulary.txt << EOF
apple\tA sweet red fruit
book\tCollection of written pages
computer\tElectronic device for processing data
car\tVehicle with four wheels
house\tBuilding for living
EOF
```

2. **Start learning**:
```bash
# Study mode
poetry run crablang vocabulary.txt --study

# Quiz mode
poetry run crablang vocabulary.txt --quiz

# Reverse quiz (definition to term)
poetry run crablang vocabulary.txt --quiz --reverse
```

## File Formats Supported

The application supports multiple file formats:

### 1. Tab-Separated (TSV)
```text
apple   A sweet red fruit
book    Collection of written pages
```

### 2. Comma-Separated (CSV)
```text
apple,"A sweet red fruit"
book,"Collection of written pages"
```

### 3. Custom Delimiters
```text
apple;A sweet red fruit
book;Collection of written pages

apple##A sweet red fruit
book##Collection of written pages

apple|A sweet red fruit
book|Collection of written pages
```

### 4. With Comments
```text
# Fruits
apple   A sweet red fruit
banana  A yellow curved fruit

# Objects
book    Collection of written pages
computer Electronic device
```

## Usage

### Basic Commands

```bash
# Show help
crablang --help

# Show version
crablang --version

# Load and list crablang
crablang vocabulary.txt --list

# Study mode (term -> definition)
crablang vocabulary.txt --study

# Quiz mode (type the answer)
crablang vocabulary.txt --quiz

# Reverse mode (definition -> term)
crablang vocabulary.txt --study --reverse
crablang vocabulary.txt --quiz --reverse
```

### Creating Flashcard Files

You can create flashcard files using any text editor. The application automatically detects the format:

```bash
# Create a simple vocabulary list
echo -e "hello\tgreeting in English\nbonjour\tgreeting in French" > greetings.txt

# Create with custom delimiter
echo -e "python##programming language\njavascript##web language" > languages.txt
```

## Advanced Features

### Multiple Study Modes

- **Study Mode**: Reveal answers one by one
- **Quiz Mode**: Test your knowledge with scoring
- **Spaced Repetition**: Focus on difficult cards (coming soon)
- **Timed Challenges**: Answer under time pressure (coming soon)

### Progress Tracking

The application tracks your learning progress and helps you identify areas that need more practice.

```bash
# View learning statistics (coming soon)
crablang vocabulary.txt --stats
```

## Examples

Example flashcard files are provided in the `examples/` directory:

- `examples/vocabulary.tsv` - Basic vocabulary
- `examples/programming.csv` - Programming concepts
- `examples/languages.txt` - Language learning with custom format

## Development

### Project Structure

```
CrabLang/
├── src/
│   └── crablang/
│       ├── __init__.py
│       ├── file_parser.py
│       ├── flashcard_manager.py
│       ├── study_engine.py
│       ├── progress_tracker.py
│       └── cli.py
├── tests/
├── docs/
├── examples/
└── pyproject.toml
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various spaced repetition systems
- Built with [Poetry](https://python-poetry.org/) for dependency management
- Documentation powered by [Sphinx](https://www.sphinx-doc.org/)


**Happy Learning!** 🎓
