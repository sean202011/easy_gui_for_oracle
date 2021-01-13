import tkinter as tk
import tkinter.ttk as ttk
import json
import tkinter.messagebox as msg
import tkinter.filedialog as fl
import openpyxl as xl
import err_collection as err
import traceback


class Content(tk.Tk):
    def __init__(self, connection, file_path):
        self.conn = connection
        self.file_path = file_path
        super().__init__()
        self.set_window()
        self.set_widgets_on_frm_main()
        # get a db session
        self.conn_session = self.conn.acquire()
        # define close window
        self.protocol("WM_DELETE_WINDOW",self.close_control)

    def set_window(self):
        self.title("simple GUI of oracle basic operations ")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width / 3
        y = screen_height / 3
        self.geometry("+%d+%d" % (x, y))
        self.resizable(0, 0)
        # set frame on window
        self.frm_main = ttk.Frame(self, borderwidth=7, relief='groove')
        self.frm_main.pack(padx=5, pady=5, anchor=tk.CENTER)

    def set_widgets_on_frm_main(self):
        ttk.Label(self.frm_main, text='table_name:').grid(row=0, column=1, sticky=tk.E)
        self.value_table = tk.StringVar()
        self.list_table = self.get_table_list()
        self.ccb_table = ttk.Combobox(self.frm_main, textvariable=self.value_table, value=self.list_table)
        self.ccb_table.grid(row=0, column=2, sticky=tk.W)
        ttk.Label(self.frm_main, text='columns_list:').grid(row=1, column=1, sticky=tk.E)
        self.txt_column = tk.Text(self.frm_main, height=3)
        self.txt_column.grid(row=1, column=2, sticky=tk.W, pady=5)

        self.bt_import = ttk.Button(self.frm_main, text='import', command=self.call_import)
        self.bt_import.grid(row=2, column=2, sticky=tk.W)

    def get_table_list(self):
        with open(self.file_path, 'r') as f:
            temp = json.load(f)
        return tuple(temp.get("import_table_list"))

    def close_control(self):
        self.conn.close()
        self.destroy()

    def call_import(self):
        try:
            v_value = []
            v_temp_row = []
            if self.txt_column == '' or self.txt_column == '\n':
                raise err.No_Column_Err
            # open file
            self.bt_import.state(["disabled"])
            file = fl.askopenfilename(defaultextension='.xlsx', parent=self,
                                      filetypes=[("excel file type", "*.xlsx"), ("excel file type", "*.xls")],
                                      title="open file")
            if file:
                # read file via openpyxl package
                wb = xl.load_workbook(file)
                ws = wb.active
                for row in ws.rows:
                    v_temp_row.clear()
                    for cell in row:
                        v_temp_row.append(str(cell.value))
                    v_value.append(v_temp_row.copy())
                    # print(v_value)
                # make sql string
                temp_value_list = ':'
                for i in self.txt_column.get("0.0", tk.END).strip():
                    temp_value_list += i
                    if i == ',':
                        temp_value_list = temp_value_list + ':'

                v_sql = """
                        begin
                        insert into """ + self.value_table.get() + """
                        (""" + \
                        self.txt_column.get("0.0", tk.END).strip() + """)
                        values
                        (
                        """ + \
                        temp_value_list + """
                        );
                        end;
                """
                cursor = self.conn_session.cursor()
                cursor.executemany(v_sql, v_value)
                self.conn_session.commit()
                msg.showinfo(title='import over', message='import successful', parent=self)
                self.bt_import.state(["!disabled"])
        except err.No_Column_Err:
            msg.showerror(title='no columns',
                          message="you need give columns that you will insert" + traceback.format_exc(),
                          parent=self
                          )
        except:
            self.bt_import.state(["!disabled"])
            msg.showerror(title='import error',
                          message="database connection issue or column or table you give is invalid: \n" + traceback.format_exc(),
                          parent=self
                          )
