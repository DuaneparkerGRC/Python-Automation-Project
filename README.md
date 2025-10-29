# Counseling Progress Notes Automation (Python + OpenAI)

A lightweight desktop app that turns a counselor’s brief session summary into a structured **progress note** (preview → edit → export).  
Built as a **personal learning project** to practice Python automation, UI basics, and integrating the OpenAI API end-to-end.

---

## What it does (at a glance)
- Takes a **free-text session description** as input.
- Uses the **OpenAI API** to organize content into clear sections (e.g., Presenting Problem, Assessment, Intervention, Plan).
- **Previews** the generated note so the user can make edits.
- **Exports** the final note (e.g., DOCX/PDF) while keeping the clinic’s formatting style.

---

## Why I built it
I wanted a focused project to **practice Python automation**, experiment with **desktop UI**, and learn how to connect to the **OpenAI API** safely and simply—turning unstructured text into a clean, usable document with minimal friction for the end user.

---

## Key Highlights
- **Simple UI**: a clean window to paste notes, generate, and preview results.
- **Template-aware output**: preserves headings and spacing in the final document.
- **Human-in-the-loop**: counselor reviews and edits before exporting.
- **Packaged app**: built an executable with a **custom icon** for easy use.
- **Debugging practice**: used VS Code and ChatGPT to troubleshoot quickly.

---

## How it works (short)
1. Counselor enters a short **session summary**.
2. App calls the OpenAI API to **structure** the content into preset sections.
3. User **reviews/edits** the preview.
4. Click **Export** to generate the final document.

---

## Screenshots
> _(Replace these with your own)_

![App – Input & Generate](screenshots/01_input_generate.png)
![App – Preview & Edit](screenshots/02_preview_edit.png)
![App – Exported Note](screenshots/03_exported_note.png)

---

## What I learned
- Connecting a Python app to the **OpenAI API** and handling responses reliably.
- Building a **small desktop UI** that feels responsive and easy to use.
- Automating **document generation** while keeping formatting consistent.
- Packaging to a **single executable** so non-technical users can run it.
- Iterative debugging with **VS Code** and **ChatGPT** to speed up development.

---

## Status
This is a personal learning project. I’m polishing the templates and minor UI details, and I plan to share a simplified demo build soon.

---
