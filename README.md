<img width="50" height="50" alt="Screenshot 2025-10-30 020515" src="https://github.com/user-attachments/assets/5cb7a5ad-15cd-48e2-9d46-5f29e508694e" />  Easy Report Maker -by Dulara Paranawidana
---

# Counseling Progress Notes Automation APP (Python + OpenAI) 



A lightweight desktop app that turns a counselor’s brief session summary into a structured **progress note** (preview → edit → export).  
Built as a **personal learning project** to practice Python automation, UI basics, and integrating the OpenAI API end-to-end.

---

## What it does (at a glance)
- Takes a **free-text session description** as input.
- Uses the **OpenAI API** to organize content into clear sections (e.g., Presenting Problem, Assessment, Intervention, Plan).
- **Previews** the generated note so the user can make edits.
- **Exports** the final note (e.g., DOCX/PDF) while keeping the clinic’s formatting style.

<img width="964" height="894" alt="Screenshot 2025-10-30 015937" src="https://github.com/user-attachments/assets/3abd6de4-aaad-4731-8bbd-853e9b44d4b6" />
---

## Why I built it
I wanted a focused project to **practice Python automation**, experiment with **desktop UI**, and learn how to connect to the **OpenAI API** safely and simply—turning unstructured text into a clean, usable document with minimal friction for the end user.

---
<img width="700" height="978" alt="Screenshot 2025-10-30 020147" src="https://github.com/user-attachments/assets/1f5ff5db-2f99-4593-9811-b206cf4e3b71" />

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

<img width="2550" height="1258" alt="Screenshot 2025-10-30 015150" src="https://github.com/user-attachments/assets/85649df7-c56a-42a0-963b-60c98a8fefa3" />

https://raw.githubusercontent.com/DuaneparkerGRC/Python-Automation-Project/fd74c98844cee8361f4a8c591bf42b69b6f4223f/app.py

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
