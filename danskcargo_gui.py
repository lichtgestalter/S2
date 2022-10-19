import tkinter as tk
from tkinter import ttk
import danskcargo_data
import danskcargo_sql as dcsql


# region container
def read_container_entries():  # Read content of entry boxes
    return entry_container_id.get(), entry_container_weight.get(), entry_container_destination.get(),


def clear_container_entries():  # Clear entry boxes
    entry_container_id.delete(0, tk.END)  # Delete text in entry box, beginning with the first character (0) and ending with the last character (tk.END)
    entry_container_weight.delete(0, tk.END)
    entry_container_destination.delete(0, tk.END)


def write_container_entries(values):  # Fill entry boxes
    entry_container_id.insert(0, values[0])
    entry_container_weight.insert(0, values[1])
    entry_container_destination.insert(0, values[2])


def edit_container(event, tree):  # Copy selected record into entry boxes. Parameter event is mandatory but we don't use it.
    index_selected = tree.focus()  # Index of selected record
    values = tree.item(index_selected, 'values')  # Values of selected record
    clear_container_entries()  # Clear entry boxes
    write_container_entries(values)  # Fill entry boxes


def create_container(tree, record):  # add new record to database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.create_record(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Container)  # Refresh treeview table


def update_container(tree, record):  # update record in database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.update_container(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Container)  # Refresh treeview table


def delete_container(tree, record):  # delete record in database
    container = danskcargo_data.tuple2container(record)  # Convert tuple to Container
    dcsql.delete_soft_container(container)  # Update database
    clear_container_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Container)  # Refresh treeview table


def read_table(tree, class_):  # fill tree from database
    count = 0  # Used to keep track of odd and even rows, because these will be colored differently.
    result = dcsql.select_all(class_)  # Read all containers from database
    for record in result:
next        if record.weight >= 0:  # this condition excludes soft deleted records from being shown in the data table
            if count % 2 == 0:  # even
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.container2tuple(record), tags=('evenrow',))  # Insert one row into the data table
            else:  # odd
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.container2tuple(record), tags=('oddrow',))  # Insert one row into the data table
            count += 1

# endregion container

# region aircraft


def read_aircraft_entries():  # Read content of entry boxes
    return entry_aircraft_id.get(), entry_aircraft_max_cargo_weight.get(), entry_aircraft_registration.get(),


def clear_aircraft_entries():  # Clear entry boxes
    entry_aircraft_id.delete(0, tk.END)  # Delete text in entry box, beginning with the first character (0) and ending with the last character (tk.END)
    entry_aircraft_max_cargo_weight.delete(0, tk.END)
    entry_aircraft_registration.delete(0, tk.END)


def write_aircraft_entries(values):  # Fill entry boxes
    entry_aircraft_id.insert(0, values[0])
    entry_aircraft_max_cargo_weight.insert(0, values[1])
    entry_aircraft_registration.insert(0, values[2])


def edit_aircraft(event, tree):  # Copy selected record into entry boxes. Parameter event is mandatory but we don't use it.
    index_selected = tree.focus()  # Index of selected record
    values = tree.item(index_selected, 'values')  # Values of selected record
    clear_aircraft_entries()  # Clear entry boxes
    write_aircraft_entries(values)  # Fill entry boxes


def create_aircraft(tree, record):  # add new record to database
    aircraft = danskcargo_data.tuple2aircraft(record)  # Convert tuple to Aircraft
    dcsql.create_record(aircraft)  # Update database
    clear_aircraft_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Aircraft)  # Refresh treeview table


def update_aircraft(tree, record):  # update record in database
    aircraft = danskcargo_data.tuple2aircraft(record)  # Convert tuple to Aircraft
    dcsql.update_aircraft(aircraft)  # Update database
    clear_aircraft_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Aircraft)  # Refresh treeview table


def delete_aircraft(tree, record):  # delete record in database
    aircraft = danskcargo_data.tuple2aircraft(record)  # Convert tuple to Aircraft
    dcsql.delete_soft_aircraft(aircraft)  # Update database
    clear_aircraft_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Aircraft)  # Refresh treeview table


def read_aircraft(tree):  # fill tree from database
    count = 0  # Used to keep track of odd and even rows, because these will be colored differently.
    result = dcsql.select_all(danskcargo_data.Aircraft)  # Read all aircrafts from database
    for record in result:
        if record.weight >= 0:  # this condition excludes soft deleted records from being shown in the data table
            if count % 2 == 0:  # even
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.aircraft2tuple(record), tags=('evenrow',))  # Insert one row into the data table
            else:  # odd
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.aircraft2tuple(record), tags=('oddrow',))  # Insert one row into the data table
            count += 1


# endregion aircraft

# region transport

def read_transport_entries():  # Read content of entry boxes
    return entry_transport_id.get(), entry_transport_date.get(), entry_transport_container_id.get(), entry_transport_aircraft_id.get(),


def clear_transport_entries():  # Clear entry boxes
    entry_transport_id.delete(0, tk.END)  # Delete text in entry box, beginning with the first character (0) and ending with the last character (tk.END)
    entry_transport_date.delete(0, tk.END)
    entry_transport_container_id.delete(0, tk.END)
    entry_transport_aircraft_id.delete(0, tk.END)


def write_transport_entries(values):  # Fill entry boxes
    entry_transport_id.insert(0, values[0])
    entry_transport_date.insert(0, values[1])
    entry_transport_container_id.insert(0, values[2])
    entry_transport_aircraft_id.insert(0, values[3])


def edit_transport(event, tree):  # Copy selected record into entry boxes. Parameter event is mandatory but we don't use it.
    index_selected = tree.focus()  # Index of selected record
    values = tree.item(index_selected, 'values')  # Values of selected record
    clear_transport_entries()  # Clear entry
    # boxes
    write_transport_entries(values)  # Fill entry boxes


def create_transport(tree, record):  # add new record to database
    transport = danskcargo_data.tuple2transport(record)  # Convert tuple to  Transport
    dcsql.create_record(transport)  # Update database
    clear_transport_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Transport)  # Refresh treeview table


def update_transport(tree, record):  # update record in database
    transport = danskcargo_data.tuple2transport(record)  # Convert tuple to  Transport
    dcsql.update_transport(transport)  # Update database
    clear_transport_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Transport)  # Refresh treeview table


def delete_transport(tree, record):  # delete record in database
    transport = danskcargo_data.tuple2transport(record)  # Convert tuple to  Transport
    dcsql.delete_hard_transport(transport)  # Update database
    clear_transport_entries()  # Clear entry boxes
    refresh_treeview(tree, dcsql.Transport)  # Refresh treeview table


def read_transport(tree):  # fill tree from database
    count = 0  # Used to keep track of odd and even rows, because these will be colored differently.
    result = dcsql.select_all(danskcargo_data. Transport)  # Read all transports from database
    for record in result:
        if record.weight >= 0:  # this condition excludes soft deleted records from being shown in the data table
            if count % 2 == 0:  # even
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.transport2tuple(record), tags=('evenrow',))  # Insert one row into the data table
            else:  # odd
                tree.insert(parent='', index='end', iid=str(count), text='', values=danskcargo_data.transport2tuple(record), tags=('oddrow',))  # Insert one row into the data table
            count += 1


# endregion transport

def refresh_treeview(tree, class_):  # Refresh treeview table
    empty_treeview(tree)  # Clear treeview table
    read_table(tree, class_)  # Fill treeview from database


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
root.geometry("1200x500")  # window size

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme

# Configure treeview colors and formatting. A treeview is an object that can contain a data table.
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=rowheight, fieldbackground=treeview_background)
style.map('Treeview', background=[('selected', treeview_selected)])  # Define color of selected row in treeview

# region containergui
# Define Labelframe which contains all container related GUI objects (data table, labels, buttons, ...)
frame_container = tk.LabelFrame(root, text="Container")  # https://www.tutorialspoint.com/python/tk_labelframe.htm
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
label_container_id = tk.Label(edit_frame_container, text="Id")  # https://www.tutorialspoint.com/python/tk_label.htm
label_container_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_container_id = tk.Entry(edit_frame_container, width=6)  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_container_id.grid(row=1, column=0, padx=padx, pady=pady)
# label and entry for container weight
label_container_weight = tk.Label(edit_frame_container, text="Weight")
label_container_weight.grid(row=0, column=1, padx=padx, pady=pady)
entry_container_weight = tk.Entry(edit_frame_container, width=8)
entry_container_weight.grid(row=1, column=1, padx=padx, pady=pady)
# label and entry for container destination
label_container_destination = tk.Label(edit_frame_container, text="Destination")
label_container_destination.grid(row=0, column=2, padx=padx, pady=pady)
entry_container_destination = tk.Entry(edit_frame_container, width=20)
entry_container_destination.grid(row=1, column=2, padx=padx, pady=pady)

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

# region aircraftgui
# Define Labelframe which contains all aircraft related GUI objects (data table, labels, buttons, ...)
frame_aircraft = tk.LabelFrame(root, text="Aircraft")  # https://www.tutorialspoint.com/python/tk_labelframe.htm
frame_aircraft.grid(row=0, column=1, padx=padx, pady=pady)  # https://www.tutorialspoint.com/python/tk_grid.htm

# Define data table (Treeview) and its scrollbar. Put them in a Frame.
tree_frame_aircraft = tk.Frame(frame_aircraft)  # https://www.tutorialspoint.com/python/tk_frame.htm
tree_frame_aircraft.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_aircraft = tk.Scrollbar(tree_frame_aircraft)
tree_scroll_aircraft.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_aircraft = ttk.Treeview(tree_frame_aircraft, yscrollcommand=tree_scroll_aircraft.set, selectmode="browse")  # https://docs.python.org/3/library/tkinter.ttk.html#treeview
tree_aircraft.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_aircraft.config(command=tree_aircraft.yview)

# Define the data table's formatting and content
tree_aircraft['columns'] = ("id", "weight", "destination")  # Define columns
tree_aircraft.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_aircraft.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_aircraft.column("weight", anchor=tk.E, width=80)
tree_aircraft.column("destination", anchor=tk.W, width=200)
tree_aircraft.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_aircraft.heading("id", text="Id", anchor=tk.CENTER)
tree_aircraft.heading("weight", text="Weight", anchor=tk.CENTER)
tree_aircraft.heading("destination", text="Destination", anchor=tk.CENTER)
tree_aircraft.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_aircraft.tag_configure('evenrow', background=evenrow)

tree_aircraft.bind("<ButtonRelease-1>", lambda event: edit_aircraft(event, tree_aircraft))  # Define function to be called, when an item is selected.

# Define Frame which contains labels, entries and buttons
controls_frame_aircraft = tk.Frame(frame_aircraft)
controls_frame_aircraft.grid(row=3, column=0, padx=padx, pady=pady)

# Define Frame which contains labels (text fields) and entries (input fields)
edit_frame_aircraft = tk.Label(controls_frame_aircraft)  # Add record entry boxes
edit_frame_aircraft.grid(row=0, column=0, padx=padx, pady=pady)
# label and entry for aircraft id
label_aircraft_id = tk.Label(edit_frame_aircraft, text="Id")  # https://www.tutorialspoint.com/python/tk_label.htm
label_aircraft_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_aircraft_id = tk.Entry(edit_frame_aircraft, width=6)  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_aircraft_id.grid(row=1, column=0, padx=padx, pady=pady)
# label and entry for aircraft weight
label_aircraft_max_cargo_weight = tk.Label(edit_frame_aircraft, text="Weight")
label_aircraft_max_cargo_weight.grid(row=0, column=1, padx=padx, pady=pady)
entry_aircraft_max_cargo_weight = tk.Entry(edit_frame_aircraft, width=8)
entry_aircraft_max_cargo_weight.grid(row=1, column=1, padx=padx, pady=pady)
# label and entry for aircraft destination
label_aircraft_registration = tk.Label(edit_frame_aircraft, text="Destination")
label_aircraft_registration.grid(row=0, column=2, padx=padx, pady=pady)
entry_aircraft_registration = tk.Entry(edit_frame_aircraft, width=20)
entry_aircraft_registration.grid(row=1, column=2, padx=padx, pady=pady)

# Define Frame which contains buttons
button_frame_aircraft = tk.Label(controls_frame_aircraft)
button_frame_aircraft.grid(row=1, column=0, padx=padx, pady=pady)
# Define buttons
button_create_aircraft = tk.Button(button_frame_aircraft, text="Create", command=lambda: create_aircraft(tree_aircraft, read_aircraft_entries()))
button_create_aircraft.grid(row=0, column=1, padx=padx, pady=pady)
button_update_aircraft = tk.Button(button_frame_aircraft, text="Update", command=lambda: update_aircraft(tree_aircraft, read_aircraft_entries()))
button_update_aircraft.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_aircraft = tk.Button(button_frame_aircraft, text="Delete", command=lambda: delete_aircraft(tree_aircraft, read_aircraft_entries()))
button_delete_aircraft.grid(row=0, column=3, padx=padx, pady=pady)
select_record_button = tk.Button(button_frame_aircraft, text="Clear Entry Boxes", command=clear_aircraft_entries)
select_record_button.grid(row=0, column=4, padx=padx, pady=pady)

# endregion aircraftgui

# regiontransportgui
# Define Labelframe which contains all transport related GUI objects (data table, labels, buttons, ...)
frame_transport = tk.LabelFrame(root, text="Transport")  # https://www.tutorialspoint.com/python/tk_labelframe.htm
frame_transport.grid(row=0, column=2, padx=padx, pady=pady)  # https://www.tutorialspoint.com/python/tk_grid.htm

# Define data table (Treeview) and its scrollbar. Put them in a Frame.
tree_frame_transport = tk.Frame(frame_transport)  # https://www.tutorialspoint.com/python/tk_frame.htm
tree_frame_transport.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_transport = tk.Scrollbar(tree_frame_transport)
tree_scroll_transport.grid(row=0, column=1, padx=0, pady=pady, sticky='ns')
tree_transport = ttk.Treeview(tree_frame_transport, yscrollcommand=tree_scroll_transport.set, selectmode="browse")  # https://docs.python.org/3/library/tkinter.ttk.html#treeview
tree_transport.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_transport.config(command=tree_transport.yview)

# Define the data table's formatting and content
tree_transport['columns'] = ("id", "date", "container_id", "aircraft_id")  # Define columns
tree_transport.column("#0", width=0, stretch=tk.NO)  # Format columns. Suppress the irritating first empty column.
tree_transport.column("id", anchor=tk.E, width=40)  # "E" stands for East, meaning Right. Possible anchors are N, NE, E, SE, S, SW, W, NW and CENTER
tree_transport.column("date", anchor=tk.E, width=80)
tree_transport.column("container_id", anchor=tk.W, width=90)
tree_transport.column("aircraft_id", anchor=tk.W, width=90)
tree_transport.heading("#0", text="", anchor=tk.W)  # Create column headings
tree_transport.heading("id", text="Id", anchor=tk.CENTER)
tree_transport.heading("date", text="Date", anchor=tk.CENTER)
tree_transport.heading("container_id", text="Container Id", anchor=tk.CENTER)
tree_transport.heading("aircraft_id", text="Aircraft Id", anchor=tk.CENTER)
tree_transport.tag_configure('oddrow', background=oddrow)  # Create tags for rows in 2 different colors
tree_transport.tag_configure('evenrow', background=evenrow)

tree_transport.bind("<ButtonRelease-1>", lambda event: edit_transport(event, tree_transport))  # Define function to be called, when an item is selected.

# Define Frame which contains labels, entries and buttons
controls_frame_transport = tk.Frame(frame_transport)
controls_frame_transport.grid(row=3, column=0, padx=padx, pady=pady)

# Define Frame which contains labels (text fields) and entries (input fields)
edit_frame_transport = tk.Label(controls_frame_transport)  # Add record entry boxes
edit_frame_transport.grid(row=0, column=0, padx=padx, pady=pady)
# label and entry for transport id
label_transport_id = tk.Label(edit_frame_transport, text="Id")  # https://www.tutorialspoint.com/python/tk_label.htm
label_transport_id.grid(row=0, column=0, padx=padx, pady=pady)
entry_transport_id = tk.Entry(edit_frame_transport, width=6)  # https://www.tutorialspoint.com/python/tk_entry.htm
entry_transport_id.grid(row=1, column=0, padx=padx, pady=pady)
# label and entry for transport weight
label_transport_date = tk.Label(edit_frame_transport, text="Date")
label_transport_date.grid(row=0, column=1, padx=padx, pady=pady)
entry_transport_date = tk.Entry(edit_frame_transport, width=8)
entry_transport_date.grid(row=1, column=1, padx=padx, pady=pady)
# label and entry for transport destination
label_transport_container_id = tk.Label(edit_frame_transport, text="Container Id")
label_transport_container_id.grid(row=0, column=2, padx=padx, pady=pady)
entry_transport_container_id = tk.Entry(edit_frame_transport, width=6)
entry_transport_container_id.grid(row=1, column=2, padx=padx, pady=pady)
# label and entry for transport destination
label_transport_aircraft_id = tk.Label(edit_frame_transport, text="Aircraft Id")
label_transport_aircraft_id.grid(row=0, column=3, padx=padx, pady=pady)
entry_transport_aircraft_id = tk.Entry(edit_frame_transport, width=6)
entry_transport_aircraft_id.grid(row=1, column=3, padx=padx, pady=pady)

# Define Frame which contains buttons
button_frame_transport = tk.Label(controls_frame_transport)
button_frame_transport.grid(row=1, column=0, padx=padx, pady=pady)
# Define buttons
button_create_transport = tk.Button(button_frame_transport, text="Create", command=lambda: create_transport(tree_transport, read_transport_entries()))
button_create_transport.grid(row=0, column=1, padx=padx, pady=pady)
button_update_transport = tk.Button(button_frame_transport, text="Update", command=lambda: update_transport(tree_transport, read_transport_entries()))
button_update_transport.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_transport = tk.Button(button_frame_transport, text="Delete", command=lambda: delete_transport(tree_transport, read_transport_entries()))
button_delete_transport.grid(row=0, column=3, padx=padx, pady=pady)
select_record_button = tk.Button(button_frame_transport, text="Clear Entry Boxes", command=clear_transport_entries)
select_record_button.grid(row=0, column=4, padx=padx, pady=pady)

# endregiontransportgui

refresh_treeview(tree_container, dcsql.Container)  # Load data from database
refresh_treeview(tree_aircraft, dcsql.Aircraft)  # Load data from database
refresh_treeview(tree_transport, dcsql.Transport)  # Load data from database
root.mainloop()  # Wait for button clicks and act upon them
