import tkinter as tk
from tkinter import ttk
from datetime import date, datetime

root = tk.Tk()
root.title("StudyPlanner - ToDoリスト")
root.geometry("600x400")

tasks = []

# --- タスク追加処理 ---
def add_task():
    task_name = entry_task.get()
    deadline = entry_date.get()
    priority = combo_priority.get()

    if task_name and deadline:
        tasks.append((task_name, deadline, priority))
        update_task_list()
        entry_task.delete(0, tk.END)

# --- タスクリスト更新処理 ---
def update_task_list():
    for item in tree.get_children():
        tree.delete(item)
    for t in tasks:
        tree.insert("", "end", values = t)

# --- ソート処理 ---
sort_state = {"期限": False, "優先度": False}

def sort_tasks(key):
    reverse = sort_state[key]
    sort_state[key] = not reverse

    if key == "期限":
        tasks.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"), reverse=reverse)
    elif key == "優先度":
        priority_order = {"高":0, "中":1, "低":2}
        tasks.sort(key=lambda x: priority_order.get(x[2], 3), reverse=reverse)

    update_task_list()

# --- 入力欄 ---
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="タスク名：").grid(row=0, column=0)
entry_task = tk.Entry(frame_input, width=30)
entry_task.grid(row=0, column=1)

tk.Label(frame_input, text="期限：").grid(row=0, column=2)
entry_date = tk.Entry(frame_input, width=10)
entry_date.insert(0, str(date.today()))
entry_date.grid(row=0, column=3)

tk.Label(frame_input, text="優先度：").grid(row=0, column=4)
combo_priority = ttk.Combobox(frame_input, values=["高", "中", "低"], width=5)
combo_priority.set("中")
combo_priority.grid(row=0, column=5)

tk.Button(frame_input, text="追加", command=add_task).grid(row=0, column=6)

# タスクリスト表示（TreeView）
columns = ("タスク名", "期限", "優先度")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("タスク名", text="タスク名")
tree.heading("期限", text="期限", command=lambda: sort_tasks("期限"))
tree.heading("優先度", text="優先度", command=lambda: sort_tasks("優先度"))

for col in columns:
    tree.column(col, width=150)
tree.pack(fill="both", expand=True)

root.mainloop()