from tkinter import *
from tkinter import messagebox
import sqlite3

# Database class which will perform queries to manipulate sqlite3 database.
class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Mosques (id, name, type, address, cordinates, Imam_Name)")
        self.conn.commit() 

    def display(self):
        self.cur.execute("SELECT * FROM Mosques")
        rows = self.cur.fetchall()
        return rows

     # Inserting the data into the database with the entered data from the user using INSERT query.
    def insert (self,id, name, type,address,cor,I_name):
        self.cur.execute("INSERT INTO Mosques VALUES (?,?,?,?,?,?)",(id, name, type,address,cor,I_name))
        self.conn.commit() 
        messagebox.showinfo("Successful", "The data was inserted successfully")
        
       # Deleteing based on the id given by the user using DELETE  query.
    def delete(self,id):
        self.cur.execute("DELETE FROM Mosques WHERE id=?",(id,))
        self.conn.commit()
        messagebox.showinfo("Successful", "The data was deleted successfully")  
       
     # Updating the data based on the ID given using the UPDATE query. 
    def update(self, name,I_name):
        self.cur.execute("UPDATE Mosques SET Imam_Name=? WHERE name=?",(I_name, name))
        self.cur.execute("SELECT * FROM Mosques WHERE name=?", (name,))
        data = self.cur.fetchone()
        self.conn.commit()
        return data

    # Searching the data based on the name.
    def search(self, name):
        self.cur.execute("SELECT * FROM Mosques WHERE name=?", (name,))
        data = self.cur.fetchone()
        return data

    def __del__(self):
        self.conn.close() # Closing the connection on delete object.

# For resetting al the fields.
def clear_all():
    idlable.set("")
    namelable.set("")
    value_inside.set("Select type")
    addreslable.set("")
    corlable.set("")
    imamlable.set("")

# For showing data in the listbox.
def populate_list():
    if len(db.display()) == 0:
        messagebox.showerror("No Data", "No data available in the database.")
        return
    listbox.delete(0, END)
    listbox.insert(END, "ID, Name, Type, Address, Coordinates, Imam Name")
    for row in db.display():
        listbox.insert(END, f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}")

# For adding item, and calling the database to store data.
def add_item():
    if identry.get() == "" or nameentry.get() == "" or value_inside.get() == "Select type" or corentry.get() == "" or imamentry.get() == "":
        messagebox.showerror("All Inputs required!", "Please input all the entries.")
        return
    if not identry.get().isdecimal(): # Chekcing if the ID was an integer.
        messagebox.showerror("Wrong Input", "Please enter a valid Integer ID.")
        return
    for row in db.display():
        if row[0] == identry.get():
            messagebox.showerror("Present Data", "The given ID is already present in the database.")
            return
    listbox.delete(0, END)
    
    db.insert(identry.get(),nameentry.get(), value_inside.get(), addresentry.get(), corentry.get(), imamentry.get())
    clear_all()
    populate_list()


def remove_item():
    if len(db.display()) == 0:
        messagebox.showerror("No Data", "No data available in the database.")
        return
    if identry.get() == "": # Checking if the ID was given to remove the data.
        messagebox.showerror("ID requried!", "Please enter an ID to delete")
        return
    if not identry.get().isdecimal(): # Checking if the ID was an integer or not.
        messagebox.showerror("Wrong Input", "Please enter a valid Integer ID.")
    db.delete(identry.get()) # Calling the database function for deleting the data.
    listbox.delete(0, END)
    clear_all()

def update_item():
    if len(db.display()) == 0:
        messagebox.showerror("No Data", "No data available in the database.")
        return
    if nameentry.get() == "" or imamentry.get() == "": # Checking if hte Imam entry is given.
        messagebox.showerror("Input Required", "Please input both Imam and Name entry to update.")
        return
    listbox.delete(0, END)
    data = db.update(nameentry.get(), imamentry.get())
    if not data:
        messagebox.showerror("Error", "No data was found with name " + nameentry.get()) 
    else:
        messagebox.showinfo("Successful", "The data was updated successfully")
    clear_all()
    populate_list()


def search_by_name():
    if len(db.display()) == 0: # Checking if the database is empty.
        messagebox.showerror("No Data", "No data available in the database.")
        return
    if nameentry.get() == "": # Checking if the name was entered.
        messagebox.showerror("Name requried!", "Please enter a name to search by.")
        return
    data = db.search(nameentry.get())
    if not data:
        messagebox.showerror("No data", "No data was found with " + nameentry.get())
        return
    listbox.delete(0, END)
    listbox.insert(END, "ID, Name, Type, Address, Coordinates, Imam Name")
    clear_all()
    listbox.insert(END, f"{data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}")

db = Database('store.db')

app = Tk()
app.title('Mosques Management System')
app.geometry('900x350') 

idlable = StringVar() 
idlable1 =Label(app, text='ID',font=('bold',14),pady=20)
idlable1.grid(row=0,column=0,sticky=W)
identry =Entry(app,textvariable=idlable) 
identry.grid(row=0,column=1)

namelable = StringVar() 
namelable1 =Label(app, text='Name',font=('bold',14) ,pady=20)
namelable1.grid(row=0,column=2,sticky=W)
nameentry =Entry(app,textvariable=namelable)
nameentry.grid(row=0,column=3)

typelable = StringVar()
typelable =Label(app, text='Type',font=('bold',14) ,pady=20)
typelable.grid(row=1,column=0,sticky=W)
options_list = ["Type 1", "Type 2", "Type 3", "Type 4"] 

value_inside =StringVar(app) 

value_inside.set("Select type")

question_menu = OptionMenu(app, value_inside, *options_list)
question_menu.grid(row=1,column=1,sticky=W)


addreslable = StringVar()
addreslable1 =Label(app, text='Address',font=('bold',14) ,pady=20)
addreslable1.grid(row=1,column=2,sticky=W)
addresentry =Entry(app,textvariable=addreslable)
addresentry.grid(row=1,column=3)

corlable = StringVar()
corlable1 =Label(app, text='Coordinates',font=('bold',14) ,pady=20)
corlable1.grid(row=3,column=0,sticky=W)
corentry =Entry(app,textvariable=corlable)
corentry.grid(row=3,column=1)


imamlable = StringVar()
imamlable1 =Label(app, text='Imam_Name',font=('bold',14) ,pady=20)
imamlable1.grid(row=3,column=2,sticky=W)
imamentry =Entry(app,textvariable=imamlable)
imamentry.grid(row=3,column=3)

listbox =Listbox(app,height=20,width=65) 
listbox.grid(row=0,column=4,columnspan=4,rowspan=6,padx=20)

scrollbar = Scrollbar(app,orient='vertical',command=listbox.yview)
scrollbar.grid(row=0,column=7, rowspan=6, sticky='nse')
listbox['yscrollcommand'] = scrollbar.set 


add_btn = Button(app,text='Add Entry',width=12, bg="#89f589", command=add_item)
add_btn.grid(row=4,column=0)

Update_btn = Button(app,text='Update Entry',width=12, bg="#f5bb89", command=update_item)
Update_btn.grid(row=4,column=1)

Delete_btn = Button(app,text='Delete Entry',width=12, bg="#f7a69e", command=remove_item)
Delete_btn.grid(row=4,column=2)
display_all = Button(app,text='Display All',width=12, bg="#87b5ed", command=populate_list)
display_all.grid(row=4,column=3)
search_name = Button(app,text='Search By Name',width=25, bg="#eff589", command=search_by_name)
search_name.grid(row=5,column=0, columnspan=4)

#start program
app.mainloop()
