# Ultron

**Local Markdown · SwiftUI workspace**

Ultron reads ordinary Markdown files and presents their checklist tasks in a native macOS workspace. The main engineering question is how to update a note when another editor can change the same file.

## Run the review

```sh
python checklist_review.py
```

The [standalone example](checklist_review.py) opens a temporary note, simulates an external change, and verifies that a stale save leaves the external edit intact. It then reopens the file, completes the task, and verifies that only the checkbox changed. It also rejects an ambiguous task label.

[Read the persistence case study](CASE_STUDY.md) · [Publication scope](PUBLICATION.md)

The AI-assisted Python example models the save decision independently of the SwiftUI application. It uses no personal notes.
