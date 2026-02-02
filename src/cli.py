#!/usr/bin/env python3
"""
Sticky Notes CLI - Add notes from command line

Usage:
    python cli.py add --title "Title" --content "Content" --tags "tag1,tag2" --color yellow --priority 0
    python cli.py add --title "Session Summary" --content "..." --session-note
    python cli.py list
    python cli.py search "keyword"
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path


def get_storage_path():
    """Get the notes.json path based on platform."""
    if os.name == 'nt':  # Windows
        app_data = os.environ.get('APPDATA', os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming'))
        return Path(app_data) / 'StickyNotes' / 'notes.json'
    elif sys.platform == 'darwin':  # macOS
        return Path.home() / 'Library' / 'Application Support' / 'StickyNotes' / 'notes.json'
    else:  # Linux
        xdg_data = os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')
        return Path(xdg_data) / 'sticky-notes' / 'notes.json'


def load_notes(filepath: Path) -> list:
    """Load notes from JSON file."""
    if not filepath.exists():
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_notes(filepath: Path, notes: list):
    """Save notes to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def add_note(title: str, content: str, tags: str = '', color: str = 'yellow',
             priority: int = 0, pinned: bool = False, session_id: str = None,
             session_context: dict = None):
    """Add a new note to the sticky notes system."""
    filepath = get_storage_path()
    notes = load_notes(filepath)

    now = datetime.now().isoformat()

    note = {
        'noteTitle': title,
        'content': content,
        'tags': tags,
        'priority': priority,
        'pinned': pinned,
        'note_id': str(uuid.uuid4()),
        'color': color,
        'created_at': now,
        'updated_at': now,
        'attachments': []
    }

    # Add session metadata if provided
    if session_id:
        note['session_id'] = session_id
    if session_context:
        note['session_context'] = session_context

    notes.append(note)
    save_notes(filepath, notes)

    print(f"Added note: {title}")
    print(f"Note ID: {note['note_id']}")
    return note


def list_notes(limit: int = 10):
    """List recent notes."""
    filepath = get_storage_path()
    notes = load_notes(filepath)

    # Sort by updated_at descending
    notes.sort(key=lambda n: n.get('updated_at', ''), reverse=True)

    print(f"Found {len(notes)} notes (showing last {limit}):\n")

    for i, note in enumerate(notes[:limit]):
        title = note.get('noteTitle', note.get('title', 'Untitled'))
        color = note.get('color', 'white')
        tags = note.get('tags', '')
        if isinstance(tags, list):
            tags = ','.join(tags)

        print(f"[{i+1}] {title}")
        print(f"    Color: {color} | Tags: {tags or '(none)'}")
        print(f"    Content: {note.get('content', '')[:80]}...")
        print()


def search_notes(keyword: str):
    """Search notes by keyword."""
    filepath = get_storage_path()
    notes = load_notes(filepath)

    keyword_lower = keyword.lower()
    matches = []

    for note in notes:
        title = note.get('noteTitle', note.get('title', ''))
        content = note.get('content', '')
        tags = note.get('tags', '')
        if isinstance(tags, list):
            tags = ','.join(tags)

        if keyword_lower in title.lower() or keyword_lower in content.lower() or keyword_lower in tags.lower():
            matches.append(note)

    print(f"Found {len(matches)} notes matching '{keyword}':\n")

    for note in matches:
        title = note.get('noteTitle', note.get('title', 'Untitled'))
        print(f"- {title}")
        print(f"  {note.get('content', '')[:100]}...")
        print()


def main():
    parser = argparse.ArgumentParser(description='Sticky Notes CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new note')
    add_parser.add_argument('--title', '-t', required=True, help='Note title')
    add_parser.add_argument('--content', '-c', required=True, help='Note content')
    add_parser.add_argument('--tags', default='', help='Comma-separated tags')
    add_parser.add_argument('--color', default='yellow',
                          choices=['yellow', 'blue', 'green', 'pink', 'white', 'red', 'orange', 'purple', 'cyan'],
                          help='Note color')
    add_parser.add_argument('--priority', type=int, default=0, help='Priority (0-4)')
    add_parser.add_argument('--pinned', action='store_true', help='Pin the note')
    add_parser.add_argument('--session-note', action='store_true', help='Mark as session summary note')
    add_parser.add_argument('--session-id', help='Session ID for context')
    add_parser.add_argument('--machine', default=os.environ.get('COMPUTERNAME', 'unknown'), help='Machine name')
    add_parser.add_argument('--project', default='unknown', help='Project name')

    # List command
    list_parser = subparsers.add_parser('list', help='List recent notes')
    list_parser.add_argument('--limit', '-n', type=int, default=10, help='Number of notes to show')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search notes')
    search_parser.add_argument('keyword', help='Search keyword')

    args = parser.parse_args()

    if args.command == 'add':
        session_context = None
        if args.session_note:
            session_context = {
                'machine': args.machine,
                'project': args.project,
                'created_date': datetime.now().strftime('%Y-%m-%d')
            }
            # Default tags for session notes
            if not args.tags:
                args.tags = f'session-summary,{args.project}'

        add_note(
            title=args.title,
            content=args.content,
            tags=args.tags,
            color=args.color,
            priority=args.priority,
            pinned=args.pinned,
            session_id=args.session_id,
            session_context=session_context
        )

    elif args.command == 'list':
        list_notes(args.limit)

    elif args.command == 'search':
        search_notes(args.keyword)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
