import tkinter as tk
from tkinter import ttk
import danskcargo_data
import danskcargo_sql as dcsql


# region container
def read_container_entries():  # Read content of entry boxes
    return entry_id.get(), entry_weight.get(), entry_destination.get(),


def clear_container_entries():  # Clear entry boxes
    entry_id.delete(0, tk.END)  # Delete text in entry box, beginning with the first character (0) and ending with the last character (tk.END)
    entry_weight.delete(0, tk.END)
    entry_destination.delete(0, tk.END)


def write_container_entries(values):  # Fill entry boxes
    entry_id.insert(0, values[0])
    entry_weight.insert(0, values[1])
    entry_destination.insert(0, values[2])


def edit_container(event, tree):  # Copy selected record into entry boxes. Parameter event is mandatory but we don't use it.
    index_selected = tree.focus()  # Index of selected record
    values = tree.item(index_selected, 'values')  # Values of selected record
    clear_container_entries()  # Clear entry boxes
    write_container_entries(values)  # Fill entry boxes


def create_container(tree, record):  # add new record to database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.create_container(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree)  # Refresh treeview table


def update_container(tree, record):  # update record in database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.update_container(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree)  # Refresh treeview table


def delete_container(tree, record):  # delete record in database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.delete_soft_container(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree)  # Refresh treeview table


def read_container(tree):  # fill tree from database
    count = 0  # Used to keep track of odd and even rows, because these will be colored differently.
    result = dcsql.select_all(danskcargo_data.Container)  # Read all containers from database
    for record in result:
        if record.weight >= 0:  # this condition excludes soft deleted records from being shown in the data table
            if count % 2 == 0:  # even
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.container2tuple(record), tags=('evenrow',))  # Insert one row into the data table
            else:  # odd
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.container2tuple(record), tags=('oddrow',))  # Insert one row into the data table
            count += 1

# endregion container


def refresh_treeview(tree):  # Refresh treeview table
    empty_treeview(tree)  # Clear treeview table
    read_container(tree)  # Fill treeview from database


def empty_treeview(tree):  # Clear treeview table
    tree.delete(*tree.get_children())


# global constants
padx = 8  # Horizontal distance to neighboring objects
pady = 4  # Vertical distance to neighboring objects
rowheight = 24  # rowheight in treeview
treeview_background = "#eeeeee"  # color of background in treeview
treeview_foreground = "black"  # color of foreground in treeview
treeview_selected = "#206030"  # color of selected row in treeview
oddrow = "#dddddd"  # color of odd row in treeview
evenrow = "#cccccc"  # color of even row in treeview

root = tk.Tk()  # Define the main window
root.title('AspIT S2: DanskCargo')  # Text shown in the top window bar
root.iconbitmap('AspIT.ico')  # Icon in the upper left corner
root.geometry("1000x500")  # window size

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme

# Configure treeview colors and formatting. A treeview is an object that can contain a data table.
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=rowheight, fieldbackground=treeview_background)
style.map('Treeview', background=[('selected', treeview_selected)])  # Define color of selected row in treeview

# region containergui
# Define Labelframe which contains all container related GUI objects (data table, labels, buttons, ...)
frame_container = tk.LabelFrame(root, text="Container")    # https://www.tutorialspoint.com/python/tk_labelframe.htm
frame_container.grid(row=0, column=0, padx=padx, pady=pady)  # https://www.tutorialspoint.com/python/tk_grid.htm

# Define data table (Treeview) and its scrollbar. Put them in a Frame.
tree_frame_container = tk.Frame(frame_container)  # https://www.tutorialspoint.com/python/tk_frame.htm
tree_frame_container.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_container = tk.Scrollbar(tree_frame_container)
tree_scroll_container.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_container = ttk.Treeview(tree_frame_container, yscrollcommand=tree_scroll_container.set, selectmode="browse")  # https://docs.python.org/3/library/tkinter.ttk.html#treeview
tree_container.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_container.config(command=tree_container.yview)

# Define the data table's formatting and content
tree_container['columns'] = ("id", "weight", "destination")  # Define columns
tree_container.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_container.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_container.column("weight", anchor=tk.E, width=80)
tree_container.column("destination", anchor=tk.W, width=200)
tree_container.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_container.heading("id", text="Id", anchor=tk.CENTER)
tree_container.heading("weight", text="Weight", anchor=tk.CENTER)
tree_container.heading("destination", text="Destination", anchor=tk.CENTER)
tree_container.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_container.tag_configure('evenrow', background=evenrow)

tree_container.bind("<ButtonRelease-1>", lambda event: edit_container(event, tree_container))  # Define function to be called, when an item is selected.

# Define Frame which contains labels, entries and buttons
controls_frame_container = tk.Frame(frame_container)
controls_frame_container.grid(row=3, column=0, padx=padx, pady=pady)

# Define Frame which contains labels (text fields) and entries (input fields)
edit_frame_container = tk.Label(controls_frame_container)  # Add record entry boxes
edit_frame_container.grid(row=0, column=0, padx=padx, pady=pady)
# label and entry for container id
label_id = tk.Label(edit_frame_container, text="Id")  # https://www.tutorialspoint.com/python/tk_label.htm
label_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_id = tk.Entry(edit_frame_container, width=6)  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_id.grid(row=1, column=0, padx=padx, pady=pady)
# label and entry for container weight
label_weight = tk.Label(edit_frame_container, text="Weight")
label_weight.grid(row=0, column=1, padx=padx, pady=pady)
entry_weight = tk.Entry(edit_frame_container, width=8)
entry_weight.grid(row=1, column=1, padx=padx, pady=pady)
# label and entry for container destination
label_destination = tk.Label(edit_frame_container, text="Destination")
label_destination.grid(row=0, column=2, padx=padx, pady=pady)
entry_destination = tk.Entry(edit_frame_container, width=20)
entry_destination.grid(row=1, column=2, padx=padx, pady=pady)

# Define Frame which contains buttons
button_frame_container = tk.Label(controls_frame_container)
button_frame_container.grid(row=1, column=0, padx=padx, pady=pady)
# Define buttons
button_create_container = tk.Button(button_frame_container, text="Create", command=lambda: create_container(tree_container, read_container_entries()))
button_create_container.grid(row=0, column=1, padx=padx, pady=pady)
button_update_container = tk.Button(button_frame_container, text="Update", command=lambda: update_container(tree_container, read_container_entries()))
button_update_container.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_container = tk.Button(button_frame_container, text="Delete", command=lambda: delete_container(tree_container, read_container_entries()))
button_delete_container.grid(row=0, column=3, padx=padx, pady=pady)
select_record_button = tk.Button(button_frame_container, text="Clear Entry Boxes", command=clear_container_entries)
select_record_button.grid(row=0, column=4, padx=padx, pady=pady)

# endregion containergui

refresh_treeview(tree_container)  # Load data from database
root.mainloop()  # Wait for button clicks and act upon them
