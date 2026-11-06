# Secure Document Verifier

A simple desktop app (Python + Tkinter) that checks whether a document has been modified, using **SHA-256** hashes.

1. **Upload Original File**: computes the file's SHA-256 hash and stores it in a local SQLite database.
2. **Verify File**: hashes the file again and compares it with the stored hash. The result is **ORIGINAL** or **MODIFIED**, and is saved to a verification history.

## Features

- SHA-256 hashing, read in chunks so large files are fine
- Supports `.txt`, `.pdf`, `.docx`, `.png`, `.jpg`, `.jpeg`
- Shows file name, size and hash
- Verification history with timestamps (clearable)
- Fully offline, no third-party dependencies

## Requirements

- Python 3.8+ (Tkinter is included with the standard Windows/macOS installers; on some Linux distros install it with `sudo apt install python3-tk`)

## Run

```bash
git clone https://github.com/<your-username>/secure_document_verifier.git
cd secure_document_verifier
python main.py
```

The database file `records.db` is created automatically next to the scripts on first run.

## Project structure

```
main.py       # Tkinter GUI and app logic
hashing.py    # SHA-256 file hashing
database.py   # SQLite storage (hashes + verification history)
```

## Limitations

- Original files are matched **by file name**, so the file you verify must have the same name as the one you registered.
- The stored hashes live in a local, unprotected SQLite file. Anyone with access to it could replace a hash, so this detects accidental or casual changes, not a determined attacker.
- Uploading an original again under the same name replaces its previous hash.
