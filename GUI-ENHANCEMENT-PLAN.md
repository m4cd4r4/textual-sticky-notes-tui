# GUI Enhancement Plan for Timestamps & Attachments

Based on the original tutorial.gif and current TUI design, here's how to integrate the new features.

## 🎯 Current UI Design

**Layout:**
- 3-column grid of sticky note cards
- Keyboard-driven (vim-style navigation: h/j/k/l)
- Modal dialogs for edit/delete/search
- Color indicators for priority (0-4)
- Pin icon (📌) for pinned notes
- Priority icons (🔵🟡🟠🔴)

**Keyboard Shortcuts:**
- `a` - Add note
- `e` - Edit note
- `r` - Delete note
- `s` - Search notes
- `1-9` - Change color
- `d` - Toggle dark/light mode

---

## 🆕 Proposed Enhancements

### 1. **Timestamps Display**

#### Option A: Subtle Footer (Recommended)
```
┌─────────────────────────────────────┐
│ 📌 Meeting Notes 🔴                 │
├─────────────────────────────────────┤
│ Discuss Q1 goals and roadmap       │
│ - Budget planning                   │
│ - Team expansion                    │
│                                     │
│ 📅 Jan 16, 10:30 AM  ⏱️ Updated 2h │
└─────────────────────────────────────┘
```

**Implementation:**
- Add `border_subtitle` to StickyNote component
- Show: `📅 Created: [date] ⏱️ Updated: [relative time]`
- Relative time: "2h ago", "3d ago", "2w ago"

#### Option B: Compact Header
```
┌─────────────────────────────────────┐
│ 📌 Meeting Notes 🔴 (Jan 16 10:30) │
├─────────────────────────────────────┤
│ Content here...                     │
└─────────────────────────────────────┘
```

**Recommendation:** Use Option A for better readability

---

### 2. **Attachment Indicators**

#### Visual Approach: Icon + Count
```
┌─────────────────────────────────────┐
│ 📌 Receipt - Office Supplies 📎2   │
├─────────────────────────────────────┤
│ Purchased pens and paper            │
│                                     │
│ 📎 receipt.pdf (1.2MB)              │
│ 📎 invoice.jpg (856KB)              │
│                                     │
│ 📅 Jan 16, 2:30 PM  ⏱️ 5m ago      │
└─────────────────────────────────────┘
```

**Attachment Section:**
- Show at bottom of note content
- File icon based on type:
  - 📄 Documents (.pdf, .docx, .txt)
  - 🖼️ Images (.jpg, .png, .gif)
  - 📊 Spreadsheets (.xlsx, .csv)
  - 📦 Other files
- Show filename and size
- Clickable to open file

---

### 3. **New Keyboard Shortcuts**

Add these bindings to `app.py`:

```python
BINDINGS = [
    # Existing...
    ("ctrl+a", "attach_file", "Attach file"),      # NEW
    ("ctrl+o", "open_attachment", "Open file"),     # NEW
    ("ctrl+t", "toggle_timestamps", "Show times"),  # NEW
]
```

**Actions:**
- `Ctrl+A` - Open attachment modal (when editing note)
- `Ctrl+O` - Open first attachment in default app
- `Ctrl+T` - Toggle timestamp display on/off

---

### 4. **Enhanced Edit Modal**

Update `editModal.py` to include:

```
┌──────────────────────────────────────────────────┐
│              Edit Note                           │
├──────────────────────────────────────────────────┤
│ Title: [Meeting Notes__________________]         │
│                                                  │
│ Content:                                         │
│ ┌──────────────────────────────────────────┐   │
│ │ Discuss Q1 goals                         │   │
│ │ - Budget planning                        │   │
│ │ - Team expansion                         │   │
│ └──────────────────────────────────────────┘   │
│                                                  │
│ Tags: [work,planning,q1_________]               │
│ Priority: [●●●○○] Medium                        │
│ Color: [Yellow ▼]                               │
│                                                  │
│ Attachments: (2)                                │
│ 📄 receipt.pdf (1.2MB) [✕]                      │
│ 🖼️ screenshot.png (856KB) [✕]                   │
│ [+ Add Attachment] (Ctrl+A)                     │
│                                                  │
│ Created: Jan 16, 2026 at 10:30 AM               │
│ Updated: Jan 16, 2026 at 2:45 PM                │
│                                                  │
│      [Save]  [Cancel]                           │
└──────────────────────────────────────────────────┘
```

**New Elements:**
- Attachments section with list
- Add/Remove buttons for files
- Timestamp display (read-only)
- File size indicators

---

### 5. **Attachment Modal**

Create new modal: `attachModal.py` (already created!)

```
┌──────────────────────────────────────────────────┐
│         📎 Attach File (Max 10MB)                │
├──────────────────────────────────────────────────┤
│                                                  │
│ Paste or drag file path:                        │
│ ┌──────────────────────────────────────────┐   │
│ │ C:\Downloads\receipt.pdf_____________    │   │
│ └──────────────────────────────────────────┘   │
│                                                  │
│ ✅ receipt.pdf (1.2 MB)                         │
│    Valid - ready to attach                      │
│                                                  │
│ Tips:                                            │
│ • Max size: 10MB per file                       │
│ • Supported: All file types                     │
│ • File will be copied (original safe)           │
│                                                  │
│      [Attach]  [Cancel]                         │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Visual Design Updates

### **1. Sticky Note Component** (`stickyNote.py`)

**Current:**
```python
border_title = f"{pin_icon}{self.note.noteTitle} {priority_icon}"
```

**Enhanced:**
```python
# Title
attachment_count = len(self.note.attachments)
attach_icon = f" 📎{attachment_count}" if attachment_count > 0 else ""
border_title = f"{pin_icon}{self.note.noteTitle} {priority_icon}{attach_icon}"

# Subtitle (timestamps)
if show_timestamps:
    created = format_relative_time(self.note.created_at)
    border_subtitle = f"📅 {created} ⏱️ Updated {updated}"
```

**Content Rendering:**
```python
def compose(self):
    yield Static(self.note.content, id="noteContent")

    # Show attachments if any
    if self.note.attachments:
        yield Static("", classes="attachment-divider")
        for attachment in self.note.attachments:
            icon = get_file_icon(attachment)
            name = Path(attachment).name
            size = get_file_size(attachment)
            yield Static(f"{icon} {name} ({size})",
                        classes="attachment-item")
```

---

### **2. Color Scheme**

**Timestamp Colors:**
```css
.timestamp {
    color: #888;
    font-style: italic;
}

.timestamp-recent {
    color: #4CAF50; /* Green for recent */
}

.timestamp-old {
    color: #999;
}
```

**Attachment Colors:**
```css
.attachment-item {
    color: #2196F3;
    text-decoration: underline;
    cursor: pointer;
}

.attachment-item:hover {
    color: #1976D2;
}
```

---

## 🚀 Implementation Priority

### **Phase 1: Essential Features** (Do First)
1. ✅ Update `stickyNote.py` to display attachment count in title
2. ✅ Add timestamp subtitle to note cards
3. ✅ Integrate `attachModal.py` with edit modal
4. ✅ Add keyboard shortcut for attachments

### **Phase 2: Polish** (Nice to Have)
1. File icons based on type
2. Relative time formatting ("2h ago")
3. Clickable attachments (open in default app)
4. Attachment preview for images

### **Phase 3: Advanced** (Future)
1. Inline image preview (for .jpg, .png)
2. Attachment thumbnails
3. Drag & drop file support (if Textual supports it)
4. Attachment search

---

## 📝 Code Changes Needed

### **1. Update `stickyNote.py`**

Add to `__init__`:
```python
def __init__(self, note: Note, show_timestamps=True, **kwargs):
    super().__init__(**kwargs)
    self.note = note
    self.show_timestamps = show_timestamps
    self.priority_level = note.priority
    self.is_pinned = note.pinned
```

Update `update_title`:
```python
def update_title(self):
    pin_icon = "📌 " if self.is_pinned else ""
    priority_icon = self.get_priority_icon()

    # Add attachment indicator
    attachment_count = len(getattr(self.note, 'attachments', []))
    attach_icon = f" 📎{attachment_count}" if attachment_count > 0 else ""

    self.border_title = f"{pin_icon}{self.note.noteTitle} {priority_icon}{attach_icon}"

    # Add timestamp subtitle
    if self.show_timestamps and hasattr(self.note, 'created_at'):
        created = self.format_timestamp(self.note.created_at)
        self.border_subtitle = f"📅 {created}"
```

Add helper method:
```python
def format_timestamp(self, iso_timestamp):
    """Format ISO timestamp to readable form"""
    from datetime import datetime
    if not iso_timestamp:
        return ""

    dt = datetime.fromisoformat(iso_timestamp)
    return dt.strftime("%b %d, %I:%M %p")
```

### **2. Update `editModal.py`**

Add attachment section to compose:
```python
def compose(self):
    # Existing fields...

    # Attachments section
    if hasattr(self.note, 'attachments'):
        yield Static("Attachments:", classes="label")
        for att in self.note.attachments:
            # Show attachment with remove button
            pass
        yield Button("+ Add Attachment (Ctrl+A)", id="add-attachment")
```

### **3. Update `app.py`**

Add keyboard binding:
```python
BINDINGS = [
    # ... existing bindings
    ("ctrl+a", "attach_file", "Attach file"),
]

def action_attach_file(self):
    """Open attachment modal"""
    from components.attachModal import AttachModal
    focused = self.focused
    if hasattr(focused, 'note'):
        self.push_screen(AttachModal(focused.note.note_id),
                        self.handle_attachment)
```

---

## 🎯 Recommended Tutorial.gif Updates

**New demo should show:**

1. **Creating note with timestamp**
   - Press `a`
   - Note shows "📅 Jan 16, 10:30 AM"

2. **Adding attachment**
   - Press `e` to edit
   - Press `Ctrl+A` to attach
   - Show file path input
   - Note title updates with "📎1"

3. **Viewing note with attachments**
   - Note displays with attachment count
   - Bottom shows file list
   - Timestamps visible

4. **Opening attachment**
   - Focus on note with attachment
   - Press `Ctrl+O`
   - File opens in default app

---

## 📊 Before/After Comparison

### **Before (Original):**
```
┌─────────────────────────┐
│ 📌 Meeting Notes 🔴     │
├─────────────────────────┤
│ Discuss Q1 goals        │
│ - Budget planning       │
│ - Team expansion        │
└─────────────────────────┘
```

### **After (Enhanced):**
```
┌──────────────────────────────────┐
│ 📌 Meeting Notes 🔴 📎2          │
├──────────────────────────────────┤
│ Discuss Q1 goals                 │
│ - Budget planning                │
│ - Team expansion                 │
│                                  │
│ 📄 agenda.pdf (234KB)            │
│ 🖼️ budget.png (1.1MB)            │
│                                  │
│ 📅 Jan 16, 10:30 AM  ⏱️ 2h ago  │
└──────────────────────────────────┘
```

**Key Differences:**
- ✅ Attachment count in title (📎2)
- ✅ File list with icons and sizes
- ✅ Timestamps at bottom
- ✅ Relative time ("2h ago")

---

## 🛠️ Tools Needed

1. **File type detection** - Add to `file_utils.py`
2. **Relative time formatter** - "2 hours ago", "3 days ago"
3. **File icon mapper** - Map extensions to emojis
4. **Attachment click handler** - Open files on Ctrl+O

---

## ✅ Summary

**Must-Have Changes:**
1. Show attachment count in note title (📎2)
2. Display timestamps in subtitle
3. List attachments in note content
4. Add Ctrl+A shortcut for attaching files

**Should-Have Changes:**
1. File type icons (📄🖼️📊)
2. Relative time display ("2h ago")
3. File sizes in human-readable format

**Nice-to-Have:**
1. Clickable attachments (Ctrl+O)
2. Image previews
3. Toggle timestamp visibility
4. Attachment search

---

**Created:** 2026-01-16
**Status:** Planning
**Next Step:** Implement Phase 1 changes to stickyNote.py
