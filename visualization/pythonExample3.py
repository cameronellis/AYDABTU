from Tkinter import *

def show_entry_fields():
	#print("Database Name: %s\nTable Name: %s\nField Name 1: %s\nField name 2: %s" % (e4.get(), e1.get(), e2.get(), e3.get()))
	fo = open("sampleQueryFile.json", "wb")
	fo.write("{\n\t" + '"'+ e4.get() + '":{\n\t\t' + '"' + e1.get() +'":["' + e2.get()+'","'+e3.get()+'"]\n}\n}\n');
	fo.close();
	e1.delete(0,END)
	e2.delete(0,END)
	e3.delete(0,END)
	e4.delete(0,END)
	master.quit()

master = Tk()
Label(master, text="Table Name").grid(row=0)
Label(master, text="Field Name 1").grid(row=1)
Label(master, text="Field Name 2").grid(row=2)
Label(master, text="Database Name").grid(row=3)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)

e4.insert(10, "national_fire_protection.fire_problem_overview")
e1.insert(10,"names")
e2.insert(10,"Civilian Deaths")
e3.insert(10, "Firefighter deaths")

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

#Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
Button(master, text='Generate JSON file', command=show_entry_fields).grid(row=4, column=0, sticky=W, pady=4)

mainloop( )