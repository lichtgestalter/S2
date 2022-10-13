from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import danskcargo_sql as dcsql


def remove_selected_container():  # Remove Many records
    x = tree_container.selection()
    for record in x:
        tree_container.delete(record)  # delete from treeview
        # kode mangler  # delete from database


def clear_container_entries():  # Clear entry boxes
    entry_id.delete(0, END)
    entry_weight.delete(0, END)
    entry_destination.delete(0, END)


def fill_container_entries(values):  # Fill entry boxes
    entry_id.insert(0, values[0])  # output to entry boxes
    entry_weight.insert(0, values[1])
    entry_destination.insert(0, values[2])


def edit_container():  # Select record
    clear_container_entries()  # Clear entry boxes
    selected = tree_container.focus()  # Grab record number
    values = tree_container.item(selected, 'values')  # Grab record values
    fill_container_entries(values)


def update_container():
    selected = tree_container.focus()  # Grab the record number
    record = (entry_id.get(), entry_weight.get(), entry_destination.get(),)
    tree_container.item(selected, text="", values=record)  # update treeview
    # kode mangler  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_container()


def add_container():  # add new record to database
    record = (entry_id.get(), entry_weight.get(), entry_destination.get(),)
    # kode mangler  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_container()


def read_container():  # fill tree from database
    count = 0
    result = dcsql.select_all(dcsql.Container)
    for record in result:
        if count % 2 == 0:
            tree_container.insert(parent='', index='end', iid=count, text='', values=(record.id, record.weight, record.destination), tags=('evenrow',))
        else:
            tree_container.insert(parent='', index='end', iid=count, text='', values=(record.id, record.weight, record.destination), tags=('oddrow',))
        count += 1


def empty_table(tree):
    tree.delete(*tree.get_children())


def refresh_container():
    empty_table(tree_container)  # Clear The Treeview Table
    read_container()  # fill tree from database


root = Tk()
root.title('AspIT S2: DanskCargo')
root.iconbitmap('AspIT.ico')
root.geometry("1000x500")
# data = [[1, 1000, "Las Vegas"], [2, 2222, "Chicago"]]  # Add fake data

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")  # Configure Treeview Colors
style.map('Treeview', background=[('selected', "#309070")])  # Change selected color

tree_frame_container = Frame(root)  # Create treeview frame
tree_frame_container.pack(pady=10)
tree_scroll_container = Scrollbar(tree_frame_container)  # Create treeview scrollbar
tree_scroll_container.pack(side=RIGHT, fill=Y)
tree_container = ttk.Treeview(tree_frame_container, yscrollcommand=tree_scroll_container.set, selectmode="extended")  # Create treeview
tree_container.pack()
tree_scroll_container.config(command=tree_container.yview)  # Configure scrollbar

tree_container['columns'] = ("id", "weight", "destination")  # Define columns
tree_container.column("#0", width=0, stretch=NO)  # Format columns
tree_container.column("id", anchor=E, width=40)
tree_container.column("weight", anchor=E, width=80)
tree_container.column("destination", anchor=W, width=200)
tree_container.heading("#0", text="", anchor=W)  # Create headings
tree_container.heading("id", text="Id", anchor=CENTER)
tree_container.heading("weight", text="Weight", anchor=CENTER)
tree_container.heading("destination", text="Destination", anchor=CENTER)

tree_container.tag_configure('oddrow', background="#dddddd")  # Create striped row tags
tree_container.tag_configure('evenrow', background="#cccccc")

data_frame = LabelFrame(root, text="Record")  # Add record entry boxes
data_frame.pack(fill="x", expand="yes", padx=20)

label_id = Label(data_frame, text="First Name")
label_id.grid(row=0, column=0, padx=10, pady=10)
entry_id = Entry(data_frame)
entry_id.grid(row=0, column=1, padx=10, pady=10)

label_weight = Label(data_frame, text="Last Name")
label_weight.grid(row=0, column=2, padx=10, pady=10)
entry_weight = Entry(data_frame)
entry_weight.grid(row=0, column=3, padx=10, pady=10)

label_destination = Label(data_frame, text="ID")
label_destination.grid(row=0, column=4, padx=10, pady=10)
entry_destination = Entry(data_frame)
entry_destination.grid(row=0, column=5, padx=10, pady=10)

button_frame = LabelFrame(root, text="Commands")  # Add Buttons
button_frame.pack(fill="x", expand="yes", padx=20)

button_edit_container = Button(button_frame, text="Edit Container", command=edit_container)
button_edit_container.grid(row=0, column=1, padx=10, pady=10)

button_update_container = Button(button_frame, text="Update Record", command=update_container)
button_update_container.grid(row=0, column=3, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_container)
add_button.grid(row=0, column=5, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Remove Selected", command=remove_selected_container)
remove_all_button.grid(row=0, column=7, padx=10, pady=10)

# remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
# remove_one_button.grid(row=0, column=3, padx=10, pady=10)
#
# remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
# remove_many_button.grid(row=0, column=4, padx=10, pady=10)
#
# move_up_button = Button(button_frame, text="Move Up", command=up)
# move_up_button.grid(row=0, column=5, padx=10, pady=10)
#
# move_down_button = Button(button_frame, text="Move Down", command=down)
# move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_container_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

tree_container.bind("select", edit_container)  # Bind the treeview

refresh_container()
root.mainloop()
