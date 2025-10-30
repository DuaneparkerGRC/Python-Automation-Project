import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import openai
from openai import OpenAI
from docx import Document
from dotenv import load_dotenv
import os
import shutil
from datetime import datetime

# Load API Key
app_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(app_dir, ".env"))
client = OpenAI()

# Constants
TEMPLATE_PATH = os.path.join(app_dir, "Progress Note Template.docx")
SAVE_DIR = os.path.join(app_dir, "Generated Reports")
SETTINGS_FILE = os.path.join(app_dir, "settings.txt")

# Default prompt
DEFAULT_PROMPT = """
You are a mental health professional. Analyze the following raw case notes and rewrite them into a formal progress note format under these headings:

Presenting Problem(s):
Assessment:
Intervention:
Plan:

Use simple, professional language. Maintain similar word count to the sample in the template. Do not fabricate or exaggerate. Follow a person-centred approach. I often use mindfulness and deep breathing. With kids I use play therapy and expressive arts. With some clients, I use psychoanalysis.

Case Notes:
"""

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return DEFAULT_PROMPT

def save_settings(new_prompt):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_prompt)

def generate_progress_notes(notes, base_prompt):
    full_prompt = f"{base_prompt}\n{notes}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content.strip()

def save_to_docx(mapping, client_name, session_count, full_date, full_time):
    from tkinter import filedialog

    default_filename = f"{client_name.replace(' ', '_')}_Session_{session_count}.docx"
    save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")], initialfile=default_filename)
    if not save_path:
        return None

    shutil.copy(TEMPLATE_PATH, save_path)
    doc = Document(save_path)

    replacements = {
        "[Replace with input Name]": client_name,
        "[Replace with input Date]": full_date,
        "[Replace with input Time]": full_time,
        "[Replace with input Sessions]": session_count,
        "[Replace with output of Presenting Problem(s): ]": mapping.get("Presenting Problem(s):", ""),
        "[Replace with output of Assessment:]": mapping.get("Assessment:", ""),
        "[Replace with output of Intervention: ]": mapping.get("Intervention:", ""),
        "[Replace with output of Plan:]": mapping.get("Plan:", "")
    }

    for para in doc.paragraphs:
        for key, val in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, val)

    doc.save(save_path)
    return save_path

def run_app():
    def on_generate():
        client_name = entry_name.get()
        session_count = entry_sessions.get()
        notes = text_notes.get("1.0", tk.END).strip()
        day = combo_day.get()
        month = combo_month.get()
        year = combo_year.get()
        hour = entry_hour.get()
        minute = entry_minute.get()
        ampm = combo_ampm.get()

        if not all([client_name, day, month, year, hour, minute, ampm, session_count, notes]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        full_date = f"{day}-{month}-{year}"
        full_time = f"{hour}:{minute} {ampm}"

        progress_bar.start()
        root.update()

        try:
            generated = generate_progress_notes(notes, base_prompt)
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, generated)
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")
        finally:
            progress_bar.stop()

    def on_export():
        generated = text_output.get("1.0", tk.END).strip()
        if not generated:
            messagebox.showerror("Error", "No generated content to export.")
            return

        mapping = {}
        section = None
        for line in generated.splitlines():
            line = line.strip()
            if line in ["Presenting Problem(s):", "Assessment:", "Intervention:", "Plan:"]:
                section = line
                mapping[section] = ""
            elif section:
                mapping[section] += line + " "

        client_name = entry_name.get()
        session_count = entry_sessions.get()
        full_date = f"{combo_day.get()}-{combo_month.get()}-{combo_year.get()}"
        full_time = f"{entry_hour.get()}:{entry_minute.get()} {combo_ampm.get()}"

        try:
            save_path = save_to_docx(mapping, client_name, session_count, full_date, full_time)
            if not save_path:
                return
            messagebox.showinfo("Success", f"Report successfully saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")

    def on_reset():
        entry_name.delete(0, tk.END)
        entry_sessions.delete(0, tk.END)
        text_notes.delete("1.0", tk.END)
        text_output.delete("1.0", tk.END)
        combo_day.set("01")
        combo_month.set("JAN")
        combo_year.set("2025")
        entry_hour.delete(0, tk.END)
        entry_hour.insert(0, "10")
        entry_minute.delete(0, tk.END)
        entry_minute.insert(0, "30")
        combo_ampm.set("AM")

    def open_settings():
        top = tk.Toplevel(root)
        top.title("Edit GPT Prompt")
        top.geometry("700x500")

        text_editor = scrolledtext.ScrolledText(top, wrap=tk.WORD, font=("Arial", 11))
        text_editor.pack(expand=True, fill='both', padx=10, pady=10)

        current = load_settings()
        text_editor.insert(tk.END, current)

        def save_prompt():
            new_prompt = text_editor.get("1.0", tk.END).strip()
            save_settings(new_prompt)
            messagebox.showinfo("Saved", "Prompt updated successfully.")
            top.destroy()

        tk.Button(top, text="Save Changes", command=save_prompt).pack(pady=5)

    global base_prompt
    base_prompt = load_settings()

    global root
    root = tk.Tk()
    root.iconbitmap(os.path.join(app_dir, "Report_Maker.ico"))
    root.title("Progress Note Generator")
    root.geometry("800x700")
    root.configure(padx=20, pady=20)

    menubar = tk.Menu(root)
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Edit GPT Prompt", command=open_settings)
    menubar.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menubar)

    form_frame = tk.Frame(root)
    form_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(0, weight=0)

    tk.Label(form_frame, text="Client Name:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    entry_name = tk.Entry(form_frame)
    entry_name.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

    tk.Label(form_frame, text="Date:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    date_frame = tk.Frame(form_frame)
    date_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
    combo_day = ttk.Combobox(date_frame, width=5, values=[str(d).zfill(2) for d in range(1, 32)])
    combo_day.grid(row=0, column=0)
    combo_day.set("01")
    month_abbr = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    combo_month = ttk.Combobox(date_frame, width=5, values=month_abbr)
    combo_month.grid(row=0, column=1)
    combo_month.set("JAN")
    combo_year = ttk.Combobox(date_frame, width=6, values=["2025"])
    combo_year.grid(row=0, column=2)
    combo_year.set("2025")

    tk.Label(form_frame, text="Time:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    time_frame = tk.Frame(form_frame)
    time_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    entry_hour = tk.Entry(time_frame, width=5)
    entry_hour.grid(row=0, column=0)
    entry_hour.insert(0, "10")
    entry_minute = tk.Entry(time_frame, width=5)
    entry_minute.grid(row=0, column=1)
    entry_minute.insert(0, "30")
    combo_ampm = ttk.Combobox(time_frame, width=5, values=["AM", "PM"])
    combo_ampm.grid(row=0, column=2)
    combo_ampm.set("AM")

    tk.Label(form_frame, text="# of Sessions:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    entry_sessions = tk.Entry(form_frame)
    entry_sessions.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

    tk.Label(root, text="Case Notes:").grid(row=4, column=0, sticky="ne")
    text_notes = scrolledtext.ScrolledText(root, width=70, height=8)
    text_notes.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Generated Output:").grid(row=5, column=0, sticky="ne")
    text_output = scrolledtext.ScrolledText(root, width=70, height=15)
    text_output.grid(row=5, column=1, padx=5, pady=5)

    progress_bar = ttk.Progressbar(root, orient="horizontal", mode='indeterminate', length=300)
    progress_bar.grid(row=6, column=1, pady=5, sticky="ew")

    button_frame = tk.Frame(root)
    button_frame.grid(row=7, column=1, sticky="e", pady=10)
    tk.Button(button_frame, text="Generate Draft", command=on_generate).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Export to Word", command=on_export).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Reset", command=on_reset).grid(row=0, column=2, padx=5)

    root.mainloop()

if __name__ == "__main__":
    run_app()
