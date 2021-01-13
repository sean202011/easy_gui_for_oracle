import tkinter as tk
import tkinter.ttk as ttk
import cx_Oracle as cxo
import json
import tkinter.messagebox as msg
import traceback
import content as ct


class Main(tk.Tk):
    def __init__(self):
        # global variable
        self.db_info = {"host": "", "server_name": "", "user_name": "",
                        "user_password": "", "address": "", "port": ""
                        }
        self.file_name = 'config.txt'
        ####################
        super().__init__()
        self.set_window()

    def set_window(self):
        self.set_frame()
        self.set_widgets()

        self.title("simple GUI of oracle basic operations ")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width / 3
        y = screen_height / 3
        self.geometry("+%d+%d" % (x, y))
        self.resizable(0, 0)

    def set_frame(self):
        self.main_frame = ttk.Frame(self, borderwidth=5, padding="3 3 3 3", relief='groove')
        self.main_frame.pack(padx=5, pady=5)

    def set_widgets(self):
        self.cb_db_value = self.__get_db_value()
        self.text_db_value = tk.StringVar()
        self.cb_db = ttk.Combobox(self.main_frame, textvariable=self.text_db_value, value=self.cb_db_value)
        self.cb_db.state(['readonly'])
        self.cb_db.grid(row=0, column=1, columnspan=2, pady=5, sticky='n')

        self.bt_ok = ttk.Button(self.main_frame, text='OK',
                                command=self.__connect_db
                                )
        self.bt_ok.grid(row=1, column=1, sticky='s')
        self.bt_cancel = ttk.Button(self.main_frame, text='CANCEL',
                                    command=lambda: self.destroy())
        self.bt_cancel.grid(row=1, column=2, sticky='s')

    def __get_db_info(self, db_info):
        # n = db_info.find(':')
        # server_name = db_info[0:n]
        # user_name = db_info[n + 1:]
        try:
            with open(self.file_name, 'r') as f:
                temp_json = json.load(f)
            temp = temp_json.get("connection_info")
            for k in temp:
                # if server_name == k.get("server_name") and user_name == k.get("user_name"):
                self.db_info["host"] = k.get("host")
                self.db_info["server_name"] = k.get("server_name")
                self.db_info["user_name"] = k.get("user_name")
                self.db_info["user_password"] = k.get("user_password")
                self.db_info["port"] = k.get("port")
                break
        except:
            msg.showerror(title="configure error", message='your configure file has errors', parent=self)

    def __connect_db(self):
        if self.text_db_value.get() != '':
            try:
                self.__get_db_info(self.db_info)
                dsn = cxo.makedsn(self.db_info.get("host")
                                  , self.db_info.get("port")
                                  , self.db_info.get("server_name")
                                  )
                self.pool = cxo.SessionPool(
                    self.db_info.get("user_name")
                    , self.db_info.get("user_password")
                    , dsn
                    , min=1
                    , max=500
                    , increment=1
                    , threaded=True
                )
                msg.showinfo(title='connect succedd'
                             , message='connect succeed'
                             , parent=self)
                self.destroy()
                a = ct.Content(self.pool,self.file_name)
            except:
                msg.showerror(title='connection error',
                              message='error when try to connect the pool :\n' + traceback.format_exc(),
                              parent=self)
        else:
            msg.showerror(title='please choose one database'
                          , message='please choose one database'
                          , parent=self
                          )

    def __get_db_value(self):
        try:
            return_list = []
            with open(self.file_name, 'r') as f:
                temp_json = json.load(f)
            temp = temp_json.get("connection_info")
            for k in temp:
                return_list.append(k.get("server_name") + ' : ' + k.get("user_name"))
            return tuple(return_list)
        except:
            msg.showerror(title="configure error", message='your configure file has errors', parent=self)


if __name__ == '__main__':
    root = Main()
    tk.mainloop()
