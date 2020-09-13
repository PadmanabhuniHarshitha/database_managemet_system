import tkinter
from tkinter import ttk
import datetime
import time
import sqlite3
from tkinter import messagebox
from tkinter import *


class Student_portal():
    db_name='new_database.db'

    def __init__(self,root):
        self.root=root
        self.root.title("Student data")
        #-------photo--------
        self.photo=PhotoImage(file='studentpic.png')
        self.label=Label(image=self.photo)
        self.label.grid(row=0,column=0)
        #-------text-------------
        self.label2=Label(font=('arial',18,'bold'),text='Student portal System',fg='black')
        self.label2.grid(row=8,column=0)
        #------------entry boxes-----------
        frame=LabelFrame(self.root,text='Add new Record')
        frame.grid(row=0,column=1)

        Label(frame,text='Username :').grid(row=1,column=1,sticky=W)
        self.Username=Entry(frame)
        self.Username.grid(row=1,column=2)
        Label(frame, text='Email id :').grid(row=2, column=1, sticky=W)
        self.Email_id = Entry(frame)
        self.Email_id.grid(row=2, column=2)
        Label(frame, text='Roll no :').grid(row=3, column=1, sticky=W)
        self.roll_no = Entry(frame)
        self.roll_no.grid(row=3, column=2)
        Label(frame, text='Deptname :').grid(row=4, column=1, sticky=W)
        self.deptname = Entry(frame)
        self.deptname.grid(row=4, column=2)
        #-------Button----------
        ttk.Button(frame,text="Add Record",command=self.add).grid(row=6,column=2)
        #-----------alert message display--------
        self.message=Label(text='',fg='red')
        self.message.grid(row=5,column=1)

        #------database display-------
        self.tree=ttk.Treeview(height=10,column=['','','','','',''])
        self.tree.grid(row=9,column=0,columnspan=4)
        self.tree.heading('#0',text='Id')
        self.tree.column('#0',width=40)
        self.tree.heading('#1', text='username')
        self.tree.column('#1', width=80)
        self.tree.heading('#2', text='Email id')
        self.tree.column('#2', width=80)
        self.tree.heading('#3', text='Roll_no')
        self.tree.column('#3', width=80)
        self.tree.heading('#4', text='DepartmentName')
        self.tree.column('#4', width=70)
        #------------date and time---------
        def tick():
            d=datetime.datetime.now()
            today='{:%B %d, %Y}'.format(d)

            mytime=time.strftime('%I:%M,%S%p')
            self.lblInfo.config(text=(mytime+'\t'+today))
            self.lblInfo.after(200,tick)
        self.lblInfo=Label(font=('arial',20,'bold'),fg='dark blue')
        self.lblInfo.grid(row=10,column=0,columnspan=4)
        tick()
        #----------TOP MENU BAR WITH DROP DOWN-------------
        Chooser=Menu()
        itemone=Menu()
        itemtwo=Menu()

        itemone.add_command(label='Add Record',command=self.add)
        itemone.add_command(label='Edit Record',command=self.edit)
        itemone.add_command(label='Delete Record',command=self.dele)
        itemone.add_separator()
        itemone.add_command(label='Help',command=self.help)
        itemone.add_command(label='Exit',command=self.ex)

        itemtwo.add_command(label='Add element')

        Chooser.add_cascade(label='File',menu=itemone)
        Chooser.add_cascade(label='Add',command=self.add)
        Chooser.add_cascade(label='Edit',command=self.edit)
        Chooser.add_cascade(label='Delete',command=self.dele)
        Chooser.add_cascade(label='Help',command=self.help)
        Chooser.add_cascade(label='Exit',command=self.ex)

        root.config(menu=Chooser)
        self.viewing_records()
        #----------------Viewing the database----------------------------
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            query_result=cursor.execute(query,parameters)
            conn.commit()
        return query_result
    def viewing_records(self):
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query= "SELECT * from hello"
        db_table=self.run_query(query)
        for data in db_table:
            self.tree.insert('',1000,text=data[0],values=data[1:])
    def validation(self):
        return len(self.Username.get())!=0 and len(self.Email_id.get())!=0 and len(self.roll_no.get()) != 0 and len(self.deptname.get())!=0
    def add_record(self):
        if self.validation():
            query='INSERT INTO hello VALUES (NULL,?,?,?,?)'
            parameters= (self.Username.get(),self.Email_id.get(),self.roll_no.get(),self.deptname.get())
            self.run_query(query,parameters)
            self.message['text']='Record {} is added'.format(self.Username.get())
            #---------Clear Fields---------

            self.Username.delete(0,END)
            self.Email_id.delete(0,END)
            self.roll_no.delete(0, END)
            self.deptname.delete(0, END)
        else:
            self.message['text']='Fields not completed! Fill all the fields...'
        self.viewing_records()
    def add(self):
        ad= tkinter.messagebox.askquestion('Add Record','Want to Add a New Record?')
        if ad=='yes':
            self.add_record()
    def delete_record(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.message['text']='Please select a record to delete'
            return
        self.message['text']=''
        number=self.tree.item(self.tree.selection())['text']
        query='DELETE FROM hello WHERE ID=?'
        self.run_query(query,(number,))
        self.message['text']='Record {} is deleted'.format(number)
        self.viewing_records()
    def dele(self):
        de=tkinter.messagebox.askquestion('Delete Record','Want to delete a record?')
        if de=='yes':
            self.delete_record()
    #-----------Edit Record--------------------
    def edit_box(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text']='Please,select a record to edit'
            return
        uname=self.tree.item(self.tree.selection())['values'][0]
        ename = self.tree.item(self.tree.selection())['values'][1]
        rname = self.tree.item(self.tree.selection())['values'][2]
        dname = self.tree.item(self.tree.selection())['values'][3]

        self.edit_root=Toplevel()
        self.edit_root.title('Edit Record')

        Label(self.edit_root,text='Old Username').grid(row=0,column=1,sticky=W)
        Entry(self.edit_root,textvariable=StringVar(self.edit_root,value=uname),state='readonly').grid(row=0,column=2)
        Label(self.edit_root,text='New Username').grid(row=1,column=1,sticky=W)
        new_uname=Entry(self.edit_root)
        new_uname.grid(row=1,column=2)

        Label(self.edit_root, text='Old Email_id').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=ename), state='readonly').grid(row=2,column=2)
        Label(self.edit_root, text='New Email_id').grid(row=3, column=1, sticky=W)
        new_ename = Entry(self.edit_root)
        new_ename.grid(row=3, column=2)

        Label(self.edit_root, text='Old Roll_no').grid(row=4, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=rname), state='readonly').grid(row=4,column=2)
        Label(self.edit_root, text='New Roll_no').grid(row=5, column=1, sticky=W)
        new_rname = Entry(self.edit_root)
        new_rname.grid(row=5, column=2)

        Label(self.edit_root, text='Old Dept_name').grid(row=6, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=dname), state='readonly').grid(row=6,column=2)
        Label(self.edit_root, text='New Dept_name').grid(row=7, column=1, sticky=W)
        new_dname = Entry(self.edit_root)
        new_dname.grid(row=7, column=2)

        Button(self.edit_root,text='Save Changes',command=lambda :self.edit_record(new_uname.get(),uname,new_ename.get(),ename,new_rname.get(),rname,new_dname.get(),dname)).grid(row=8,column=2,sticky=W)
        self.edit_root.mainloop()
    def edit_record(self,new_uname,uname,new_ename,ename,new_rname,rname,new_dname,dname):
        query='UPDATE hello SET Username=?,Email_id=?,roll_no=?,deptname=? WHERE Username=? AND Email_id=? AND roll_no=? AND deptname=?'
        parameters=(new_uname,new_ename,new_rname,new_dname,uname,ename,rname,dname)
        self.run_query(query,parameters)
        self.edit_root.destroy()
        self.message['text']='{} details were changed to {}'.format(uname,new_uname)
        self.viewing_records()
    def edit(self):
        ed=tkinter.messagebox.askquestion('Edit Record','Want to Edit Record?')
        if ed=='yes':
            self.edit_box()
    def help(self):
        tkinter.messagebox.showinfo('Log','Report_sent')
    def ex(self):
        exit=tkinter.messagebox.askquestion('Exit Application','Want to close app?')
        if exit=='yes':
            root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.geometry('630x520+500+200')
    app = Student_portal(root)
    root.mainloop()





































