# Stickynotes Enhanced

Enhanced fork with timestamps and file attachments (up to 10MB per file).

## New Features

- Timestamps: created_at, updated_at (ISO 8601)
- File attachments: images, PDFs, documents
- Files copied to: %APPDATA%\StickyNotes\attachments\

## Usage

Launch: stickynotes-enhanced

Add with attachment:
python add-note-enhanced.py "Title" "Content" yellow "" "C:/path/to/file.pdf"

## Storage

Attachments: %APPDATA%\StickyNotes\attachments\{note_id}\{timestamp}_{filename}

Max file size: 10MB per file

Created: 2026-01-16
