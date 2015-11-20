from Tkinter import *
import dbList

class ext_gui:
	def __init__(self,fieldCount,colCount):
		
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
			self.addField(1)

		Button(self.master, text='Done', command=self.show_entry_fields).grid(row=len(self.varSel)+1, column=0, sticky=W, pady=4)
		#Button(self.master, text='+ fields', command=self.addField).grid(row=len(self.varSel)+1, column=1, sticky=W, pady=4)
		
	def addField(self,inCol):
		i = len(self.varSel)
		self.varSel.append(StringVar(self.master))
		label = "Field Name " + str(i-1)
		self.labels.append(label)
		self.fields.append(OptionMenu(self.master,self.varSel[i],*self.field_options))
		self.fields[i].config(width=20)
		self.fields[i].grid(row=i, column=inCol)
		Label(self.master, text=self.labels[i]).grid(row=i)

	def show_entry_fields(self):
		fo = open("query.json", "wb")
		listr = [var.get() for var in self.varSel if len(var.get()) > 0]
		print listr
		fo.write("{\n\t" + '"'+ self.varSel[0].get() + '.' + self.varSel[1].get() + '":{\n\t\t' + '"names":["'+listr[2]+'"')
		for i in range(3,len(listr)):
			fo.write(',"'+listr[i]+'"')
		fo.write(']\n\t}\n}\n');
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
				menu.add_command(label=field, command=lambda value=[self.varSel[i],field]: value[0].set(value[1]))


def initGooey(inNum):
	gooey = ext_gui(int(inNum),1)
	mainloop( )

def closePrompt():
	inputVal = entry.get()
	entry.delete(0,END)
	prompt.quit()
	initGooey(inputVal)

prompt = Tk()
inputVal = 0
Label(prompt, text="Please insert desired # of fields").grid(row=0)
entry = Entry(prompt)
entry.insert(10, "NUMBERS ONLY")
entry.grid(row=1,column=0)	
Button(prompt, text='Continue', command=closePrompt).grid(row=2, column=0, sticky=W, pady=4)
mainloop( )

	

