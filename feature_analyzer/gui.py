from Tkinter import *
import dbList

class ext_gui:
	def __init__(self,fieldCount):
		
		self.master = Tk()

		self.datab_options = []
		for key in dbList.dbases.keys(): self.datab_options.append(key)	
		
		self.table_options = ['MUST SELECT DATABASE']
		self.field_options = ['MUST SELECT DATABASE AND TABLE']
		self.options = [self.datab_options, self.table_options, self.field_options]
		
		self.labels = ["Database Name", "Table Name"]
		
		self.varSel = []
		self.fields = []
		
		for i in range(0,2):
			self.varSel.append(StringVar(self.master))
			self.fields.append(OptionMenu(self.master,self.varSel[i],*(self.options[i])))
			self.fields[i].config(width=20)
			self.fields[i].grid(row=i, column=1)
			Label(self.master, text=self.labels[i]).grid(row=i)
	
		self.varSel[0].trace("w",self.update_table_options)
		self.varSel[1].trace("w",self.update_field_options)

		for i in range(0,fieldCount):
			self.addField()

		Button(self.master, text='Done', command=self.show_entry_fields).grid(row=len(self.varSel)+1, column=0, sticky=W, pady=4)
		#Button(self.master, text='+ fields', command=self.addField).grid(row=len(self.varSel)+1, column=1, sticky=W, pady=4)

		
	def addField(self):
		i = len(self.varSel)
		self.varSel.append(StringVar(self.master))
		label = "Field Name " + str(i-1)
		self.labels.append(label)
		self.fields.append(OptionMenu(self.master,self.varSel[i],*self.field_options))
		self.fields[i].config(width=20)
		self.fields[i].grid(row=i, column=1)
		Label(self.master, text=self.labels[i]).grid(row=i)

	def show_entry_fields():
		fo = open("query.json", "wb")
		fo.write("{\n\t" + '"'+ varSel[0].get() + '":{\n\t\t' + '"' + varSel[1].get() +'":["' + varSel[2].get()+'","'+varSel[3].get()+'"]\n\t}\n}\n');
		fo.close();
		for f in self.fields:
			f.children["menu"].delete(0,END)
		self.master.quit()

	def update_table_options(self,a,b,c):
		db_name = self.varSel[0].get()
		menu = self.fields[1].children["menu"]
		menu.delete(0, "end")
		for table in (dbList.dbases[db_name]).keys():
			menu.add_command(label=table, command=lambda value=table: self.varSel[1].set(value))


	def update_field_options(self,a,b,c):
		db_name = self.varSel[0].get()
		t_name = self.varSel[1].get()
		for i in range(2,len(self.varSel)):
			menu = self.fields[i].children["menu"]
			menu.delete(0, "end")
			for field in dbList.dbases[db_name][t_name]:
				menu.add_command(label=field, command=lambda value=field: self.varSel[i].set(value))


	
gooey = ext_gui(6)
mainloop( )
