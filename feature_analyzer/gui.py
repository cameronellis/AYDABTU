from Tkinter import *
import dbList

def show_entry_fields():
	#print("Database Name: %s\nTable Name: %s\nField Name 1: %s\nField name 2: %s" % (e4.get(), e1.get(), e2.get(), e3.get()))
	fo = open("query.json", "wb")
	fo.write("{\n\t" + '"'+ dbSel.get() + '":{\n\t\t' + '"' + tableSel.get() +'":["' + fSel1.get()+'","'+fSel2.get()+'"]\n\t}\n}\n');
	fo.close();
	for f in fieldList:
		f.children["menu"].delete(0,END)
	master.quit()

def option_changed(a,b,c):
	menu = e2.children["menu"]
	menu.delete(0, "end")
	for table in (dbList.dbases[dbSel.get()]).keys():
		menu.add_command(label=table, command=lambda value=table: tableSel.set(value))


def table_choice(a,b,c):
	menu3 = e3.children["menu"]
	menu4 = e4.children["menu"]
	menu3.delete(0, "end")
	menu4.delete(0, "end")
	for field in dbList.dbases[dbSel.get()][tableSel.get()]:
		menu3.add_command(label=field, command=lambda value=field: fSel1.set(value))
		menu4.add_command(label=field, command=lambda value=field: fSel2.set(value))


master = Tk()

dbs = []
for key in dbList.dbases.keys(): dbs.append(key)	
tables = ['MUST SELECT DATABASE']
fields = ['MUST SELECT DATABASE AND TABLE']

dbSel = StringVar(master)
tableSel = StringVar(master)
fSel1 = StringVar(master)
fSel2 = StringVar(master)

dbSel.trace("w", option_changed)
tableSel.trace("w", table_choice)

Label(master, text="Database Name").grid(row=0)
Label(master, text="Table Name").grid(row=1)
Label(master, text="Field Name 1").grid(row=2)
Label(master, text="Field Name 2").grid(row=3)

e1 = OptionMenu(master,dbSel,*dbs)
e2 = OptionMenu(master,tableSel,*tables)
e3 = OptionMenu(master,fSel1,*fields)
e4 = OptionMenu(master,fSel2,*fields)
fieldList = [e1,e2,e3,e4]

#e1.insert(10, "national_fire_protection.fire_problem_overview")
#e2.insert(10,"names")
#e3.insert(10,"Civilian Deaths")
#e4.insert(10,"Firefighter deaths")


e1.config(width=20)
e2.config(width=20)
e3.config(width=20)
e4.config(width=20)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

	


#Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
Button(master, text='Generate JSON file', command=show_entry_fields).grid(row=5, column=0, sticky=W, pady=4)

mainloop( )



