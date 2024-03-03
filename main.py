from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector


class demo:
    def __init__(self, root):
        self.root = root
        self.root.title("Push data")
        self.root.geometry("900x900+0+0")

        self.var_name= StringVar()

        # title
        title_lbl = Label(root, text="Insert data", font=(
            "times-new-roman", 35, 'bold'), bg='white', fg='red')
        title_lbl.place(x=0, y=0, width=900, height=50)

        # main frame
        main_frame = Frame(root, bd=2)
        main_frame.place(x=20, y=70, width=880, height=800)

        # name area
        name_label = Label(main_frame, text="Name:",
                           font=('times-new-roman', 13, 'bold'))
        name_label.place(x=250, y=70)

        # name entry area
        name_entry = ttk.Entry(
            main_frame, textvariable=self.var_name, width=16)
        name_entry.place(x=310, y=70, width=170)

        # save button
        save_btn = Button(main_frame, text="Save", command=self.add_data, font=(
            "times-new-roman", 13, "bold"), bg='green', fg='white', width=15, height=1)
        save_btn.place(x=500, y=70, width=60)

        # delete button
        delete_btn = Button(main_frame, text="Delete", command=self.delete_data, font=(
            'times-new-roman', 13, 'bold'), bg='red', fg='white', width=15, height=1)
        delete_btn.place(x=580, y=70, width=60)

        # display frame
        display_frame = LabelFrame(main_frame, bd=2, bg='white', relief=RIDGE,
                                   text="Details", font=('times-new-roman', 12, 'bold'))
        display_frame.place(x=0, y=110, width=870, height=480)


        # create treeview widget
        self.name = ttk.Treeview(display_frame, column=("name_column"), show="headings")

        # set column headings
        self.name.heading("name_column", text="Name Field")
        self.name.pack(fill=BOTH, expand=1)


    # fetch data
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="bhakari", database="name")
        my_cursor = conn.cursor()

        my_cursor.execute("SELECT * FROM name")
        data=my_cursor.fetchall()

        if len(data) != 0:
            self.name.delete(*self.name.get_children())
            for i in data:
                self.name.insert("", END, values=(i[0], ))
            conn.commit()
        conn.close()


    # add data
    def add_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="bhakari", database="name")
            my_cursor = conn.cursor()

            my_cursor.execute("INSERT INTO name(name_column) values(%s)", (self.var_name.get(),))
            conn.commit()
            self.fetch_data()
            conn.close()

            messagebox.showinfo("Success", "Added successfully!", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due to {str(es)}", parent=self.root)


    # delete data
    def delete_data(self):
        if self.var_name.get()=="":
            messagebox.showerror("Error", "Name field must be selected...", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to delete this record?", parent=self.root)
                if delete:

                    conn=mysql.connector.connect(host="localhost", username="root", password="bhakari", database="name")

                    my_cursor= conn.cursor()
                    selected_name= self.name.item(self.name.selection(), "values")[0]
                    my_cursor.execute("DELETE FROM name WHERE name_column = %s", (selected_name,))

                    conn.commit()
                    self.fetch_data()
                    conn.close()

                    messagebox.showinfo("Delete", "Record deleted successfully!", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due to {str(es)}", parent=self.root)

     


if __name__ == "__main__":
    root = Tk()
    obj = demo(root)
    root.mainloop()
