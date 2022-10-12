from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def remove_selected():  # Remove Many records
    x = my_tree.selection()
    for record in x:
        my_tree.delete(record)  # delete from treeview
        # kode mangler  # delete from database


def clear_entries():  # Clear entry boxes
    entry_id.delete(0, END)
    entry_weight.delete(0, END)
    entry_destination.delete(0, END)


def select_record(e):  # Select Record
    entry_id.delete(0, END)  # Clear entry boxes
    entry_weight.delete(0, END)
    entry_destination.delete(0, END)

    selected = my_tree.focus()  # Grab record Number
    values = my_tree.item(selected, 'values')  # Grab record values

    entry_id.insert(0, values[0])  # output to entry boxes
    entry_weight.insert(0, values[1])
    entry_destination.insert(0, values[2])


def update_record():
    # Grab the record number
    selected = my_tree.focus()
    # Update record
    my_tree.item(selected, text="", values=(entry_id.get(), entry_weight.get(), entry_destination.get(), address_entry.get(), city_entry.get(), state_entry.get(), zipcode_entry.get(),))

    # Update the database
    # Create a database or connect to one that exists
    conn = sqlite3.connect('tree_crm.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("""UPDATE customers SET
		first_name = :first,
		last_name = :last,
		address = :address,
		city = :city,
		state = :state,
		zipcode = :zipcode

		WHERE oid = :oid""",
              {
                  'first': entry_id.get(),
                  'last': entry_weight.get(),
                  'address': address_entry.get(),
                  'city': city_entry.get(),
                  'state': state_entry.get(),
                  'zipcode': zipcode_entry.get(),
                  'oid': entry_destination.get(),
              })

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

    # Clear entry boxes
    entry_id.delete(0, END)
    entry_weight.delete(0, END)
    entry_destination.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    zipcode_entry.delete(0, END)


# add new record to database
def add_record():
    # Update the database
    # Create a database or connect to one that exists
    conn = sqlite3.connect('tree_crm.db')

    # Create a cursor instance
    c = conn.cursor()

    # Add New Record
    c.execute("INSERT INTO customers VALUES (:first, :last, :id, :address, :city, :state, :zipcode)",
              {
                  'first': entry_id.get(),
                  'last': entry_weight.get(),
                  'id': entry_destination.get(),
                  'address': address_entry.get(),
                  'city': city_entry.get(),
                  'state': state_entry.get(),
                  'zipcode': zipcode_entry.get(),
              })

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

    # Clear entry boxes
    entry_id.delete(0, END)
    entry_weight.delete(0, END)
    entry_destination.delete(0, END)
    address_entry.delete(0, END)
    city_entry.delete(0, END)
    state_entry.delete(0, END)
    zipcode_entry.delete(0, END)

    # Clear The Treeview Table
    my_tree.delete(*my_tree.get_children())

    # Run to pull data from database on start
    # query_database()


def data2table(data, tree):
    count = 0
    for record in data:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]), tags=('oddrow',))
        # increment counter
        count += 1


def empty_table(tree):
    tree.delete(*tree.get_children())

root = Tk()
root.title('AspIT S2: DanskCargo')
root.iconbitmap('AspIT.ico')
root.geometry("1000x500")

data = [[1, 1000, "Las Vegas"], [2, 2222, "Chicago"]]  # Add fake data

style = ttk.Style()  # Add style
style.theme_use('default')  # Pick theme
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")  # Configure Treeview Colors
style.map('Treeview', background=[('selected', "#347083")])  # Change selected color

tree_frame = Frame(root)  # Create treeview frame
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)  # Create treeview scrollbar
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")  # Create treeview
my_tree.pack()
tree_scroll.config(command=my_tree.yview)  # Configure scrollbar

my_tree['columns'] = ("id", "weight", "destination")  # Define columns

my_tree.column("#0", width=0, stretch=NO)  # Format columns
my_tree.column("id", anchor=E, width=40)
my_tree.column("weight", anchor=E, width=80)
my_tree.column("destination", anchor=W, width=200)

my_tree.heading("#0", text="", anchor=W)  # Create headings
my_tree.heading("id", text="Id", anchor=CENTER)
my_tree.heading("weight", text="Weight", anchor=CENTER)
my_tree.heading("destination", text="Destination", anchor=CENTER)

my_tree.tag_configure('oddrow', background="#dddddd")  # Create striped row tags
my_tree.tag_configure('evenrow', background="#cccccc")

data2table(data, my_tree)

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



# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

# update_button = Button(button_frame, text="Update Record", command=empty_table(my_tree))#update_record)
# update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Remove Selected", command=remove_selected)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

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

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
# my_tree.bind("", select_record)

# Run to pull data from database on start
# query_database()

root.mainloop()
