from Tkinter import *
import dbList

class ext_gui:
	def __init__(self,fieldCount):
		
		master = Tk()
		
		
		dbs = []
		for key in dbList.dbases.keys(): dbs.append(key)	
		
		tablePreset = ['MUST SELECT DATABASE']
		fieldPreset = ['MUST SELECT DATABASE AND TABLE']
		
		varSel = []
		for i in range(0,5): varSel.append(StringVar(master))

		fields = [
				OptionMenu(master,varSel[0],*dbs),
				OptionMenu(master,varSel[1],*tables),
				OptionMenu(master,varSel[2],*fields),
				OptionMenu(master,varSel[3],*fields)
			]
		
		labels = [
				"Database Name", 
				"Table Name", 
				"Field Name 1", 
				"Field Name 2"
			]
	
		for i in range(0,len(fields)):
			fields[i].config(width=20)
			fields[i].grid(row=i, column=1)
			Label(master, text=labels[i]).grid(row=i)
	
		varSel[0].trace("w",self.update_table_options)
		varSel[1].trace("w",self.update_field_options)

		Button(master, text='Graph Charts', command=show_entry_fields).grid(row=5, column=0, sticky=W, pady=4)
		Button(master, text='Add more fields', command=show_entry_fields).grid(row=5, column=0, sticky=W, pady=4)

		
	def addField():
		

	def show_entry_fields():
		fo = open("query.json", "wb")
		fo.write("{\n\t" + '"'+ dbSel.get() + '":{\n\t\t' + '"' + tableSel.get() +'":["' + fSel1.get()+'","'+fSel2.get()+'"]\n\t}\n}\n');
		fo.close();
		for f in fields:
			f.children["menu"].delete(0,END)
		
		master.quit()

	def update_table_options(a,b,c):
		menu = self.fields[1].children["menu"]
		menu.delete(0, "end")
		for table in (dbList.dbases[dbSel.get()]).keys():
			menu.add_command(label=table, command=lambda value=table: tableSel.set(value))


	def update_field_options(a,b,c):
		menu3 = e3.children["menu"]
		menu4 = e4.children["menu"]
		menu3.delete(0, "end")
		menu4.delete(0, "end")
		for field in dbList.dbases[dbSel.get()][tableSel.get()]:
			menu3.add_command(label=field, command=lambda value=field: fSel1.set(value))
			menu4.add_command(label=field, command=lambda value=field: fSel2.set(value))


	

mainloop( )
