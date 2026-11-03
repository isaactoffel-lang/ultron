"""Executable model of a checklist edit using a temporary Markdown note."""

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


class StaleNoteError(Exception):
    """The current file differs from the one displayed to the editor."""


@dataclass(frozen=True)
class ChecklistEdit:
    note: Path
    snapshot: bytes

    @classmethod
    def open(cls, note):
        return cls(note, note.read_bytes())

    def complete(self, label):
        lines = self.snapshot.decode().splitlines(keepends=True)
        original = f"- [ ] {label}"
        matches = [
            index for index, line in enumerate(lines)
            if line.rstrip("\r\n") == original
        ]
        if not matches:
            raise ValueError("The requested task is missing or already complete")
        index, *duplicates = matches
        if duplicates:
            raise ValueError("The task label is ambiguous")

        lines[index] = lines[index].replace(original, f"- [x] {label}")
        if self.note.read_bytes() != self.snapshot:
            raise StaleNoteError("Reload the note before applying this edit")
        self.note.write_bytes("".join(lines).encode())


def main():
    with TemporaryDirectory() as directory:
        note = Path(directory) / "sample.md"
        label = "Review the outline"
        original = b"# Sample\r\n\r\n- [ ] Review the outline\r\n"
        note.write_bytes(original)
        editor = ChecklistEdit.open(note)

        external = original + b"\r\nAn external edit.\r\n"
        note.write_bytes(external)
        try:
            editor.complete(label)
        except StaleNoteError:
            if note.read_bytes() != external:
                raise AssertionError("An external edit was lost")
            print("PASS | Refused a stale edit and preserved the external change")
        else:
            raise AssertionError("A stale edit was accepted")

        ChecklistEdit.open(note).complete(label)
        expected = external.replace(b"[ ]", b"[x]")
        if note.read_bytes() != expected:
            raise AssertionError("The fresh edit changed more than the checkbox")
        print("PASS | Reopened the note and changed only the requested checkbox")

        ambiguous = original + original
        note.write_bytes(ambiguous)
        try:
            ChecklistEdit.open(note).complete(label)
        except ValueError as error:
            if "ambiguous" not in str(error) or note.read_bytes() != ambiguous:
                raise AssertionError("Ambiguous edit handled incorrectly") from error
            print("PASS | Refused an ambiguous label and preserved the file")
        else:
            raise AssertionError("An ambiguous edit was accepted")


if __name__ == "__main__":
    main()
