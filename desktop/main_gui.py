#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student Management — Themed Desktop App (Tkinter + ttk)
v4 changes:
- Removed header texts: "Students" and the welcome subline.
- Card actions: removed per-card "Delete" (kept only "View / Edit").
- Refined spacing, paddings, and alignment.
- Pager: right-aligned with order Prev → Next.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests, csv

API_BASE = "http://127.0.0.1:8000"

def to_float(x):
    if x is None: return None
    s = str(x).strip()
    if s == "": return None
    try: return float(s)
    except: return None

def compute_gpa_4(m, l, e):
    vals = [v for v in (m,l,e) if v is not None]
    if not vals: return None
    avg10 = sum(vals)/len(vals)
    return round(avg10*0.4, 1)

def status_badge(gpa):
    if gpa is None: return ("unknown", "#E5E7EB", "#111827")
    if gpa >= 3.6:  return ("active", "#DCFCE7", "#166534")
    if gpa >= 3.0:  return ("active", "#E7F8EC", "#166534")
    if gpa >= 2.5:  return ("warning", "#FEF3C7", "#92400E")
    return ("at risk", "#FEE2E2", "#991B1B")

def api_get_students(page=1, page_size=12, search=""):
    params = {"page": page, "page_size": page_size}
    if search: params["search"] = search
    r = requests.get(f"{API_BASE}/students", params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list):
        total = len(data); start = (page-1)*page_size
        return {"meta": {"total": total, "page": page, "page_size": page_size}, "items": data[start:start+page_size]}
    return data

def api_create_student(payload):
    r = requests.post(f"{API_BASE}/students", json=payload, timeout=15)
    if r.status_code not in (200,201): raise RuntimeError(r.text)
    return r.json()

def api_update_student(sid, payload):
    r = requests.put(f"{API_BASE}/students/{sid}", json=payload, timeout=15); r.raise_for_status(); return r.json()

def api_delete_student(sid):
    r = requests.delete(f"{API_BASE}/students/{sid}", timeout=15)
    if r.status_code not in (200,204): r.raise_for_status()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management")
        self.geometry("1240x780"); self.minsize(1000,680); self.configure(bg="#F7F8FA")
        self.page, self.page_size = 1, 12; self.search = tk.StringVar(); self.selected=None
        self._style(); self._ui(); self.refresh()

    def _style(self):
        s = ttk.Style(self); s.theme_use("clam")
        s.configure("Page.TFrame", background="#F7F8FA")
        s.configure("Section.TFrame", background="#F7F8FA")
        s.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        s.configure("Title.TLabel", background="#F7F8FA", font=("Inter",18,"bold"))
        s.configure("Sub.TLabel", background="#F7F8FA", foreground="#6B7280", font=("Inter",11))
        s.configure("CardTitle.TLabel", background="#FFFFFF", font=("Inter",12,"bold"))
        s.configure("Meta.TLabel", background="#FFFFFF", foreground="#6B7280", font=("Inter",10))
        s.configure("TButton", padding=(10,6))

    def _ui(self):
        head = ttk.Frame(self, style="Page.TFrame"); head.pack(fill="x", padx=20, pady=(16,4))
        ttk.Label(head, text="Student Management", style="Title.TLabel").pack(anchor="w")

        tools = ttk.Frame(self, style="Page.TFrame"); tools.pack(fill="x", padx=20, pady=(6,10))
        entry = ttk.Entry(tools, textvariable=self.search, width=54); entry.pack(side="left", padx=(0,8))
        entry.insert(0,"Search by name or email...")
        entry.bind("<FocusIn>", lambda e: self.search.set("") if self.search.get().startswith("Search ") else None)
        ttk.Button(tools, text="Search", command=lambda: self._go_page(1)).pack(side="left")
        ttk.Button(tools, text="Clear", command=self._clear_search).pack(side="left", padx=(6,12))
        ttk.Button(tools, text="Import CSV", command=self.import_csv).pack(side="right")
        ttk.Button(tools, text="Export CSV", command=self.export_csv).pack(side="right", padx=(0,8))

        self.canvas = tk.Canvas(self, bg="#F7F8FA", highlightthickness=0); self.canvas.pack(fill="both", expand=True, padx=14, pady=(0,6))
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview); self.scroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.inner = ttk.Frame(self.canvas, style="Section.TFrame")
        self.win = self.canvas.create_window((14,0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: (self.canvas.itemconfig(self.win, width=self.canvas.winfo_width()-28),
                                                   self.canvas.configure(scrollregion=self.canvas.bbox("all"))))
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        pager = ttk.Frame(self, style="Page.TFrame"); pager.pack(fill="x", padx=20, pady=(4,12))
        self.page_label = ttk.Label(pager, text="", style="Sub.TLabel"); self.page_label.pack(side="left")
        right_box = ttk.Frame(pager, style="Page.TFrame"); right_box.pack(side="right")
        ttk.Button(right_box, text="Prev", command=self.prev_page).pack(side="left", padx=(0,6))
        ttk.Button(right_box, text="Next", command=self.next_page).pack(side="left")

        form = ttk.LabelFrame(self, text="Edit Student", style="Section.TFrame"); form.pack(fill="x", padx=20, pady=(0,16))
        grid = ttk.Frame(form, style="Section.TFrame"); grid.pack(fill="x", padx=8, pady=8)

        self.vars = {k: tk.StringVar() for k in ["student_code","first_name","last_name","email","dob","home_town","math_score","literature_score","english_score"]}

        def row(r, label, key, col):
            ttk.Label(grid, text=label, width=16).grid(row=r, column=col, sticky="w", pady=4, padx=(0,6))
            ttk.Entry(grid, textvariable=self.vars[key], width=28).grid(row=r, column=col+1, sticky="w", pady=4)

        row(0,"Student Code","student_code",0); row(0,"First Name","first_name",2)
        row(1,"Last Name","last_name",0);      row(1,"Email","email",2)
        row(2,"DOB (YYYY-MM-DD)","dob",0);     row(2,"Home Town","home_town",2)
        row(3,"Math","math_score",0);          row(3,"Literature","literature_score",2)
        row(4,"English","english_score",0)

        bar = ttk.Frame(form, style="Section.TFrame"); bar.pack(fill="x", padx=8, pady=(4,4))
        ttk.Button(bar, text="Add New", command=self.on_add).pack(side="left")
        ttk.Button(bar, text="Update", command=self.on_update).pack(side="left", padx=6)
        ttk.Button(bar, text="Delete", command=self.on_delete).pack(side="left")
        ttk.Button(bar, text="Clear Form", command=self.clear_form).pack(side="left", padx=6)

    def _go_page(self, p): self.page=max(1,p); self.refresh()
    def next_page(self): self.page+=1; self.refresh()
    def prev_page(self): self.page=max(1,self.page-1); self.refresh()
    def _clear_search(self): self.search.set(""); self._go_page(1)

    def refresh(self):
        try:
            data = api_get_students(self.page, self.page_size, self.search.get().strip())
        except Exception as e:
            messagebox.showerror("Load Error", str(e)); return
        meta = data.get("meta", {"total": len(data.get("items", [])), "page": self.page, "page_size": self.page_size})
        items = data.get("items", [])
        total_pages = max(1, (meta["total"]-1)//meta["page_size"] + 1)
        if self.page > total_pages: self.page = total_pages
        self.page_label.config(text=f"Page {meta['page']} / {total_pages} • Total {meta['total']}")
        self.render_cards(items)

    def render_cards(self, items):
        for w in self.inner.winfo_children(): w.destroy()
        cols=3
        for i,it in enumerate(items):
            r,c = divmod(i, cols)
            card = ttk.Frame(self.inner, style="Card.TFrame"); card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            self.inner.grid_columnconfigure(c, weight=1)
            wrap = ttk.Frame(card, style="Card.TFrame"); wrap.pack(fill="both", expand=True, padx=14, pady=14)

            initials = (it.get("first_name","")[:1] + it.get("last_name","")[:1]).upper() or "ST"
            avatar = tk.Canvas(wrap, width=44, height=44, highlightthickness=0, bg="white")
            avatar.create_oval(2,2,42,42, fill="#111827", outline="#111827")
            avatar.create_text(22,22, text=initials, fill="white", font=("Inter",10,"bold"))
            avatar.grid(row=0, column=0, rowspan=2, sticky="w")

            name = f"{it.get('first_name','')} {it.get('last_name','')}".strip() or "(No name)"
            ttk.Label(wrap, text=name, style="CardTitle.TLabel").grid(row=0, column=1, sticky="w", padx=(8,0))
            ttk.Label(wrap, text=it.get("student_code",""), style="Meta.TLabel").grid(row=1, column=1, sticky="w", padx=(8,0), pady=(2,6))
            ttk.Label(wrap, text=f"📧 {it.get('email','')}", style="Meta.TLabel").grid(row=2, column=0, columnspan=2, sticky="w")
            hometown = it.get("home_town") or "-"
            ttk.Label(wrap, text=f"🏠 {hometown}", style="Meta.TLabel").grid(row=3, column=0, columnspan=2, sticky="w")

            m,l,e = it.get("math_score"), it.get("literature_score"), it.get("english_score")
            gpa = compute_gpa_4(m,l,e)
            ttk.Label(wrap, text="GPA", style="Meta.TLabel").grid(row=4, column=0, sticky="w", pady=(8,0))
            ttk.Label(wrap, text=str(gpa) if gpa is not None else "-", style="CardTitle.TLabel").grid(row=4, column=1, sticky="w", pady=(8,0))

            text,bg,fg = status_badge(gpa)
            badge = tk.Label(wrap, text=text, bg=bg, fg=fg, font=("Inter",9,"bold"), padx=8, pady=2)
            badge.grid(row=5, column=0, sticky="w", pady=(6,0))

            actions = ttk.Frame(wrap, style="Card.TFrame"); actions.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10,0))
            ttk.Button(actions, text="View / Edit", command=lambda it=it: self.load_form(it)).pack(side="left")

    def load_form(self, it):
        self.selected = it
        for k,v in self.vars.items():
            val = it.get(k,""); v.set("" if val is None else str(val))
        self.canvas.yview_moveto(1.0)

    def clear_form(self):
        self.selected=None
        for v in self.vars.values(): v.set("")

    def _payload_from_form(self):
        v = {k: s.get().strip() for k,s in self.vars.items()}
        for k in ("math_score","literature_score","english_score"): v[k] = to_float(v[k])
        for k,val in list(v.items()):
            if val=="": v[k]=None
        return v

    def on_add(self):
        try:
            api_create_student(self._payload_from_form()); self.clear_form(); self._go_page(1)
            messagebox.showinfo("Success","Student created.")
        except Exception as e:
            messagebox.showerror("Create failed", str(e))

    def on_update(self):
        if not self.selected:
            messagebox.showwarning("No selection","Load a card first."); return
        try:
            api_update_student(self.selected.get("id"), self._payload_from_form()); self.refresh()
            messagebox.showinfo("Success","Student updated.")
        except Exception as e:
            messagebox.showerror("Update failed", str(e))

    def confirm_delete(self, it):
        if messagebox.askyesno("Confirm", f"Delete {it.get('student_code','this student')}?"):
            try:
                api_delete_student(it["id"]); self.refresh()
            except Exception as e:
                messagebox.showerror("Delete failed", str(e))

    def on_delete(self):
        if not self.selected:
            messagebox.showwarning("No selection","Load a card first."); return
        self.confirm_delete(self.selected)

    def import_csv(self):
        fp = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV","*.csv")])
        if not fp: return
        ok=fail=0
        try:
            with open(fp, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    payload = {
                        "student_code": row.get("student_code") or row.get("code") or row.get("id"),
                        "first_name": row.get("first_name") or row.get("fname"),
                        "last_name": row.get("last_name") or row.get("lname"),
                        "email": row.get("email"),
                        "dob": row.get("dob") or row.get("date_of_birth"),
                        "home_town": row.get("home_town") or row.get("hometown"),
                        "math_score": to_float(row.get("math_score") or row.get("math")),
                        "literature_score": to_float(row.get("literature_score") or row.get("literature")),
                        "english_score": to_float(row.get("english_score") or row.get("english")),
                    }
                    payload = {k:v for k,v in payload.items() if v not in (None,"")}
                    try: api_create_student(payload); ok+=1
                    except Exception: fail+=1
            self._go_page(1)
            messagebox.showinfo("Import CSV", f"Imported OK={ok}, FAIL={fail}")
        except Exception as e:
            messagebox.showerror("Import CSV", str(e))

    def export_csv(self):
        fp = filedialog.asksaveasfilename(title="Save CSV", defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="export_students.csv")
        if not fp: return
        try:
            data = api_get_students(1, 100000, self.search.get().strip())
            rows = data.get("items", [])
            if not rows:
                with open(fp, "w", encoding="utf-8") as f: f.write("")
                messagebox.showinfo("Export CSV","No data to export."); return
            keys = sorted({k for r in rows for k in r.keys()})
            with open(fp, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
                for r in rows: w.writerow(r)
            messagebox.showinfo("Export CSV", f"Wrote {len(rows)} rows.")
        except Exception as e:
            messagebox.showerror("Export CSV", str(e))

if __name__ == "__main__":
    App().mainloop()
