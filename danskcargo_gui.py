import tkinter as tk
from tkinter import ttk
# from tkinter import messagebox
import danskcargo_sql as dcsql


def read_container_entries():
    return entry_id.get(), entry_weight.get(), entry_destination.get(),


def delete_container_entries():  # Clear entry boxes
    entry_id.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    entry_destination.delete(0, tk.END)


def write_container_entries(values):  # Fill entry boxes
    entry_id.insert(0, values[0])
    entry_weight.insert(0, values[1])
    entry_destination.insert(0, values[2])


def container2tuple(record):
    return record.id, record.weight, record.destination


def tuple2container(record):
    container = dcsql.Container(id=record[0], weight=record[1], destination=record[2])
    return container


def remove_selected_container():  # Remove Many records
    x = tree_container.selection()
    for record in x:
        tree_container.delete(record)  # delete from treeview
        # kode mangler  # delete from database


def edit_container():  # Select record
    delete_container_entries()  # Clear entry boxes
    selected = tree_container.focus()  # Grab record number
    values = tree_container.item(selected, 'values')  # Grab record values
    write_container_entries(values)


def create_container():  # add new record to database
    record = read_container_entries()
    container = tuple2container(record)
    dcsql.create_container(container)  # Update database
    delete_container_entries()  # Clear entry boxes
    refresh_container()


def update_container():
    record = read_container_entries()
    container = tuple2container(record)
    dcsql.update_container(container)  # Update database
    delete_container_entries()  # Clear entry boxes
    refresh_container()


def delete_container():
    record = read_container_entries()
    container = tuple2container(record)
    dcsql.delete_container(container)  # Update database
    delete_container_entries()  # Clear entry boxes
    refresh_container()


def read_container():  # fill tree from database
    count = 0
    result = dcsql.select_all(dcsql.Container)
    for record in result:
        if count % 2 == 0:
            tree_container.insert(parent='', index='end', iid=str(count), text='', values=container2tuple(record), tags=('evenrow',))
        else:
            tree_container.insert(parent='', index='end', iid=str(count), text='', values=container2tuple(record), tags=('oddrow',))
        count += 1


def empty_table(tree):
    tree.delete(*tree.get_children())


def refresh_container():  # Refresh treeview table
    empty_table(tree_container)  # Clear treeview table
    read_container()  # Fill treeview from database


root = tk.Tk()
root.title('AspIT S2: DanskCargo')
root.iconbitmap('AspIT.ico')
root.geometry("1000x500")  # window size

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")  # Configure treeview colors
style.map('Treeview', background=[('selected', "#206030")])  # Change selected color in treeview

frame_container = tk.LabelFrame(root, text="Container")    # https://www.tutorialspoint.com/python/tk_labelframe.htm
frame_container.grid(row=0, column=0, padx=10, pady=10)  # https://www.tutorialspoint.com/python/tk_grid.htm

tree_frame_container = tk.Frame(frame_container)  # Create treeview frame
tree_frame_container.grid(row=0, column=0, padx=10, pady=10)
tree_scroll_container = tk.Scrollbar(tree_frame_container)  # Create treeview scrollbar
tree_scroll_container.grid(row=0, column=1, padx=0, pady=10, sticky='ns')
tree_container = ttk.Treeview(tree_frame_container, yscrollcommand=tree_scroll_container.set, selectmode="extended")  # Create treeview
tree_container.grid(row=0, column=0, padx=0, pady=10)
tree_scroll_container.config(command=tree_container.yview)  # Configure scrollbar

tree_container['columns'] = ("id", "weight", "destination")  # Define columns
tree_container.column("#0", width=0, stretch=tk.NO)  # Format columns
tree_container.column("id", anchor=tk.E, width=40)
tree_container.column("weight", anchor=tk.E, width=80)
tree_container.column("destination", anchor=tk.W, width=200)
tree_container.heading("#0", text="", anchor=tk.W)  # Create headings
tree_container.heading("id", text="Id", anchor=tk.CENTER)
tree_container.heading("weight", text="Weight", anchor=tk.CENTER)
tree_container.heading("destination", text="Destination", anchor=tk.CENTER)

tree_container.tag_configure('oddrow', background="#dddddd")  # Create striped row tags
tree_container.tag_configure('evenrow', background="#cccccc")

controls_frame_container = tk.LabelFrame(frame_container, bd=0)
controls_frame_container.grid(row=3, column=0, padx=10, pady=10)

edit_frame_container = tk.LabelFrame(controls_frame_container, bd=0)  # Add record entry boxes
edit_frame_container.grid(row=0, column=0, padx=10, pady=10)

label_id = tk.Label(edit_frame_container, text="Id")
label_id.grid(row=0, column=0, padx=10, pady=0)
entry_id = tk.Entry(edit_frame_container, width=6)  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_id.grid(row=1, column=0, padx=10, pady=10)

label_weight = tk.Label(edit_frame_container, text="Weight")
label_weight.grid(row=0, column=1, padx=10, pady=0)
entry_weight = tk.Entry(edit_frame_container, width=8)
entry_weight.grid(row=1, column=1, padx=10, pady=0)

label_destination = tk.Label(edit_frame_container, text="Destination")
label_destination.grid(row=0, column=2, padx=10, pady=0)
entry_destination = tk.Entry(edit_frame_container, width=20)
entry_destination.grid(row=1, column=2, padx=10, pady=0)

button_frame_container = tk.LabelFrame(controls_frame_container, bd=0)  # Add Buttons
button_frame_container.grid(row=1, column=0, padx=10, pady=0)

button_edit_container = tk.Button(button_frame_container, text="Edit", command=edit_container)
button_edit_container.grid(row=0, column=0, padx=10, pady=10)

button_update_container = tk.Button(button_frame_container, text="Update", command=update_container)
button_update_container.grid(row=0, column=1, padx=10, pady=10)

button_create_container = tk.Button(button_frame_container, text="Create", command=create_container)
button_create_container.grid(row=0, column=2, padx=10, pady=10)

button_delete_container = tk.Button(button_frame_container, text="Delete", command=delete_container)
button_delete_container.grid(row=0, column=3, padx=10, pady=10)

select_record_button = tk.Button(button_frame_container, text="Clear Entry Boxes", command=delete_container_entries)
select_record_button.grid(row=0, column=4, padx=10, pady=10)

refresh_container()
root.mainloop()
