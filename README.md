# Ultron

A native macOS workspace for reading notes and working with Markdown tasks.

## The problem

Personal information can become scattered across files and applications. Ultron provides a common interface while keeping the underlying notes accessible as ordinary files.

## Implementation

The private application uses SwiftUI and a local Markdown vault. The previously extracted workflow component reads checklist tasks, updates their completion state, and checks whether a note changed before saving.

| Layer | Responsibility |
| --- | --- |
| Local records | Keep notes in readable Markdown |
| Parsing | Turn note content into display models |
| Presentation | Provide native reading and workflow views |
| Persistence | Write to the intended record and report failures |

## Design decisions

Keep the files useful outside the application. Report read and write failures. Check for external edits before saving so the application can ask the user to review a changed note.

The compare-before-save behavior is not a file lock. The presence of connection code does not establish that a live service is connected.

## Public scope

This repository is a qualitative architecture writeup. Application code, sample vaults, screenshots, personal records, connection settings, and earlier development history are retained privately.

AI assisted with implementation, debugging, checks, and documentation. Publishing this writeup does not revalidate the full application.
