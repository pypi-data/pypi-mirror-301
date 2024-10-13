# long-ebook-generator-ai

**Author**: Alexis Kirke (narrative.layer)

## Overview

`long-ebook-generator-ai` is a Python library designed to generate long-form eBooks using AI-powered language models. It automates the process of creating structured book outlines, chapters, and converting them into an EPUB format, with optional Kindle compatibility. The package also supports AI-generated book covers and MathML conversion for LaTeX equations in the text.

The package integrates with OpenAI's API to generate book content based on customizable prompts, making it a powerful tool for authors, content creators, or developers looking to create AI-generated books.

## Features

- **AI-Powered Outline and Content Generation**: Automatically generate book outlines with chapters, sections, and subsections using OpenAI's GPT models.
- **EPUB Book Creation**: Convert AI-generated content into an EPUB format, compatible with major eReaders.
- **Customizable Book Structures**: Define the number of chapters, sections, and subsections for your book.
- **AI-Generated Book Covers**: Automatically generate a cover for your book using image generation AI models.
- **LaTeX Equation Support**: Convert LaTeX equations to MathML for display in the eBook.
- **Kindle Compatibility**: Optionally force compatibility with Amazon Kindle devices.

## Installation

Install the package using pip:

```bash
pip install long-ebook-generator-ai
```

## Quick Start

Here's an example of how to generate an outline and an EPUB book using `long-ebook-generator-ai`.

### 1. Import and Initialize the Client

```python
from book_writer import BookWriter

# Initialize the BookWriter
title = "The AI Revolution"
writer = BookWriter(title=title, client=client, openai_api_key=openai_api_key))
```

### 2. Generate an Outline

```python
outline = writer.generate_outline(
    num_chapters=5, 
    sections_per_chapter=3, 
    subsections_per_section=2, 
    paras_per_subsection=4
)
print(outline)
```

### 3. Generate the EPUB Book

```python
writer.generate_ebook(
    author="Your Name",
    generate_cover=True,
    force_kindle_compatibility=True,
    image_prompt="A futuristic book cover showing an AI revolution"
)
```

## Dependencies

- `openai` - For OpenAI GPT integration.
- `ebooklib` - To create and manage EPUB files.
- `Pillow` - For image manipulation (used in cover generation).
- `tiktoken` - Token management for GPT models.
- `json`, `html`, `re` - Standard libraries for handling text formatting and file management.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

