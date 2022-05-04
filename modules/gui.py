#!/usr/bin/python

import os.path
import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter.tix import Tree
from lxml import etree
from io import BytesIO
from PIL import ImageTk, Image

if __name__ != "__main__":
    from modules.ISO_pacs008 import XML_PACS008, SCHEMA_PACS008, create_msg, write_msg, validate_msg
    from modules.custom_functions import get_now_datetime


script_dir  = os.path.dirname(os.path.abspath(__file__))

def start_transaction(root):
    xml = create_msg(XML_PACS008, root.main_entities.getISO_Msg(*root.main_entities.get_entity_values("msg")))
    xml_path = os.path.join(script_dir, "../msg/" + get_now_datetime(forNaming=True) + "_Pacs008.xml")

    write_msg(xml, xml_path)
    root.body.canvas.perform_transaction(
        root, root.main_entities.bank1, root.main_entities.party1, 
        root.main_entities.party2, root.main_entities.bank2, 
        float(root.main_entities.get_entity_dict("msg")["IntrBkSttlmAmt"]), xml_path
    )

def new_viewer(root, buttons):
    window_viewer = tk.Toplevel(root)
    window_viewer.resizable(False, False)
    Viewer(root.main_entities, window_viewer).pack(padx=10, pady=10, expand = True)

def write_logs(root, text):
    root.footer.txt_console.send_message(text+"")

def new_form(root, buttons, Win_class):
    global window_form
    window_form = tk.Toplevel(root)
    window_form.resizable(False, False)
    Win_class(root.main_entities, window_form).pack(pady=20, padx=30, fill="both", expand=True)
    def on_close():
        for btn in buttons: btn.configure(state="normal")
        window_form.destroy()
    for btn in buttons: btn.configure(state="disabled")
    window_form.protocol("WM_DELETE_WINDOW", on_close)

def clear_values(form):
    for entry in form.entries.values():
        entry.delete(0, 'end')

def get_form_values(form):
    return [val.get() for val in form.entries.values()]

def save_values(form, entities, role):
    entities.set_entity_value(role, get_form_values(form))
    print(*get_form_values(form), sep=", ")
    for btn in window_form.master.footer.config_bttns:
        btn.configure(state="normal") 
    if role != "msg":
        window_form.master.update_name()
    window_form.destroy()

def write_values(form, entities, role, is_default=False):
    if is_default:
        entity_dict = entities.get_entity_default_dict(role)
    else:
        entity_dict = entities.get_entity_dict(role)
    for key, entry in form.entries.items():
        entry.delete(0, 'end')
        entry.insert(0, entity_dict[key])



APP_WIDTH   = 960
APP_HEIGHT  = 768
HD_HEIGHT   = 140
BD_HEIGHT   = 328
FT_HEIGHT   = APP_HEIGHT - HD_HEIGHT - BD_HEIGHT

BANK_TYPEA_WIDTH    = 135
BANK_TYPEA_HEIGHT   = 135
BANK_TYPEB_WIDTH    = 180
BANK_TYPEB_HEIGHT   = 180

MESSAGE_WIDTH   = 50
MESSAGE_HEIGHT  = 30
ARROW_WIDTH     = 150
ARROW_HEIGHT    = 35

MESSAGE_DIS_X_1 = 125
MESSAGE_DIS_X_2 = 260
MESSAGE_DIS_Y   = 50


MOVE_INCREMENT   = 2
MOVES_PER_SECOND = 75
ANIMATION_SPEED  = 1000 // MOVES_PER_SECOND

TITLE       = "ISO 20022 Message Simulation"
LBL_TITLE   = "ISO 20022\nMessage Simulation"


class MainApplication(tk.Tk):
    def __init__(self, entities):
        super().__init__()
        self.main_entities = entities
        self.title(TITLE)
        self.minsize(APP_WIDTH, APP_HEIGHT)
        self.geometry(str(APP_WIDTH) + "x" + str(APP_HEIGHT))
        self.columnconfigure(0, minsize = APP_WIDTH, weight = 1)
        self.rowconfigure(1, minsize = BD_HEIGHT, weight = 2)
        self.rowconfigure(2, minsize = FT_HEIGHT, weight = 1)

        self.header = Header(self)
        self.header.grid(column = 0, row = 0, sticky = "nesw")
        self.header.columnconfigure( 1    , minsize = APP_WIDTH/2, weight = 10)
        self.header.columnconfigure([0, 2], minsize = APP_WIDTH/4, weight = 1)
        self.header.rowconfigure(0, minsize = 140, weight = 1)
        
        self.body = Body(self)
        self.body.grid(column=0, row=1,  sticky = "nesw")
        self.body.columnconfigure(1, weight = 1)
        self.body.rowconfigure(1, weight = 1)
        self.body.columnconfigure([0, 2], minsize=0, weight = 1)
        self.body.rowconfigure([0, 2], minsize=0, weight = 1)

        self.footer = Footer(self, bg="grey")
        self.footer.grid(column=0, row=2, sticky="nesw")
    
    def update_name(self):
        self.header.lbl_person1_name["text"] = self.main_entities.party1.name
        self.footer.lbl_party1_name["text"] = self.main_entities.party1.name
        self.header.lbl_person2_name["text"] = self.main_entities.party2.name
        self.footer.lbl_party2_name["text"] = self.main_entities.party2.name
        self.footer.lbl_bank1_name["text"] = self.main_entities.bank1.name
        self.footer.lbl_bank2_name["text"] = self.main_entities.bank2.name

    def update_balance(self):
        self.header.lbl_person1_balance["text"] = self.main_entities.party1.balance
        self.header.lbl_person2_balance["text"] = self.main_entities.party2.balance


# ================================================================================================================
# ================================================================================================================

class Header(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        # ============= >>> FRAMES <<< =============
        # ---------- Header Frames -----------
        self.frm_hd_stats    = tk.Frame(master = self, width = APP_WIDTH/4, bg = "#acacac")
        self.frm_hd_title    = tk.Frame(master = self, width = APP_WIDTH/2, bg = "#bcbcbc")
        self.frm_hd_bttns    = tk.Frame(master = self, width = APP_WIDTH/4, bg = "#acacac")
        self.frm_hd_title.rowconfigure([0, 2], weight = 1)
        self.frm_hd_title.columnconfigure([0, 2], weight = 1)
        self.frm_hd_stats.rowconfigure([1, 2], weight = 1)
        self.frm_hd_stats.columnconfigure(1, weight = 3)
        self.frm_hd_stats.rowconfigure([0, 3], weight = 4)
        self.frm_hd_stats.columnconfigure([0, 2], weight = 1)
        self.frm_hd_bttns.rowconfigure([1,2,3], weight=1)
        self.frm_hd_bttns.columnconfigure(1, weight=1)
        self.frm_hd_bttns.rowconfigure([0, 4], weight=2)
        self.frm_hd_bttns.columnconfigure([0, 2], weight=1)
        self.frm_hd_stats.grid(column = 0, row = 0, sticky = "nesw")
        self.frm_hd_title.grid(column = 1, row = 0, sticky = "nesw")
        self.frm_hd_bttns.grid(column = 2, row = 0, sticky = "nesw")

        self.frm_person1 = tk.Frame(master = self.frm_hd_stats, bg = "#dadada")
        self.frm_person2 = tk.Frame(master = self.frm_hd_stats, bg = "#dadada")
        self.frm_person1.columnconfigure(1, weight = 1)
        self.frm_person2.columnconfigure(1, weight = 1)
        self.frm_person1.grid(column = 1, row = 1, pady = 5, sticky = "we")
        self.frm_person2.grid(column = 1, row = 2, pady = 5, sticky = "we")

        # ============= >>> WIDGETS <<< =============
        # --------------Title------------
        self.lbl_title = tk.Label(master = self.frm_hd_title, text = LBL_TITLE, font = ("arial bold", 25), bg="#bcbcbc")
        self.lbl_title.grid(column=1, row=1, sticky="nesw")

        # --------------Buttons------------
        self.btn_transaction_story   = tk.Button(master = self.frm_hd_bttns, 
                                                    text = "View Message", 
                                                    command=lambda:new_viewer(self.master, self.config_bttns))
        # self.btn_create_transaction  = tk.Button(master = self.frm_hd_bttns, text = "...")
        self.btn_start_animation     = tk.Button(master = self.frm_hd_bttns, 
                                                    text = "Start Transaction",
                                                    command=lambda:start_transaction(self.master))
        self.btn_transaction_story.grid( column = 1, row = 1, ipady = 5, ipadx = 10, sticky = "ew")
        # self.btn_create_transaction.grid(column = 1, row = 2, ipady = 5, ipadx = 10, sticky = "ew")
        self.btn_start_animation.grid(   column = 1, row = 3, ipady = 5, ipadx = 10, sticky = "ew")
        self.config_bttns=[self.btn_start_animation, self.btn_transaction_story]

        # --------------Statistics------------
        self.img_person_file = Image.open(os.path.join(script_dir, '../img/p_person.png'))
        self.img_person_file = self.img_person_file.resize((35, 35))
        self.img_person = ImageTk.PhotoImage(self.img_person_file)
        self.lbl_person1_logo    = tk.Label(master = self.frm_person1, image = self.img_person, width = 45, height = 45, bg = "#dfdfdf")
        self.lbl_person1_name    = tk.Label(master = self.frm_person1, text  = self.master.main_entities.party1.name, bg = "#dadada",
                                                font=("arial", 9))
        self.lbl_person1_balance = tk.Label(master = self.frm_person1, text  = self.master.main_entities.party1.balance, bg = "#dadada",
                                                font=("arial bold", 12), fg="#333")
        self.lbl_person1_logo.grid(column = 0, row = 0, rowspan = 2, padx = 5, sticky = "nesw")
        self.lbl_person1_name.grid(column = 1, row = 0, sticky = "sw")
        self.lbl_person1_balance.grid(column = 1, row = 1, sticky = "nw")
        self.lbl_person2_logo    = tk.Label(master = self.frm_person2, image = self.img_person, width = 45, height = 45, bg = "#dfdfdf")
        self.lbl_person2_name    = tk.Label(master = self.frm_person2, text  = self.master.main_entities.party2.name, bg = "#dadada",
                                                font=("arial", 9))
        self.lbl_person2_balance = tk.Label(master = self.frm_person2, text  = self.master.main_entities.party2.balance, bg = "#dadada",
                                                font=("arial bold", 12), fg="#333")
        self.lbl_person2_logo.grid(column = 0, row = 0, rowspan = 2, padx = 5, sticky = "nesw")
        self.lbl_person2_name.grid(column = 1, row = 0, sticky = "sw")
        self.lbl_person2_balance.grid(column = 1, row = 1, sticky = "nw")

class Body(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.canvas = Animation(master=self)
        self.canvas.grid(column=1, row=1, sticky="nsew") 

class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.columnconfigure(0, minsize=APP_WIDTH*2/3, weight=2)
        self.columnconfigure(1, minsize=APP_WIDTH*1/3, weight=1)
        self.rowconfigure(0, minsize=FT_HEIGHT)

        self.frm_ft_console = tk.Frame(self)
        self.frm_ft_console.grid(column=0, row=0, sticky="nsew")

        self.frm_ft_bttns   = tk.Frame(self)
        self.frm_ft_bttns.grid(column=1, row=0, sticky="nsew")
        self.frm_ft_bttns.columnconfigure([0, 3], weight=1)
        self.frm_ft_bttns.columnconfigure(1, weight=1)
        self.frm_ft_bttns.columnconfigure(2, weight=3)
        self.frm_ft_bttns.rowconfigure(0, weight=1, minsize=0)
        self.frm_ft_bttns.rowconfigure(7, weight=2, minsize=0)
        self.frm_ft_bttns.rowconfigure(1, weight=2)
        self.frm_ft_bttns.rowconfigure([2, 3, 4, 5, 6], weight=1)

        self.txt_console = Logs(self.frm_ft_console, bg="#444", fg="#eee", padx=10, pady=10, height=10, borderwidth=3, font=("Courier New CE", 10))
        self.txt_console.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.lbl_bttns_label = tk.Label(self.frm_ft_bttns, text="CONFIGURATION", relief=tk.RIDGE)
        self.lbl_bttns_label.grid(column=1, row=1, columnspan=2, sticky="nesw", padx=5, pady=5, ipadx=15, ipady=0)
        self.btn_party1 = tk.Button(self.frm_ft_bttns, command=lambda:new_form(self.master, self.config_bttns, Form_Prvt), text="Set Party A")
        self.btn_party2 = tk.Button(self.frm_ft_bttns, command=lambda:new_form(self.master, self.config_bttns, Form_Org), text="Set Party B")
        self.btn_bank1  = tk.Button(self.frm_ft_bttns, command=lambda:new_form(self.master, self.config_bttns, Form_FI_1), text="Set Bank A")
        self.btn_bank2  = tk.Button(self.frm_ft_bttns, command=lambda:new_form(self.master, self.config_bttns, Form_FI_2), text="Set Bank B")
        self.btn_msg    = tk.Button(self.frm_ft_bttns, command=lambda:new_form(self.master, self.config_bttns, Form_Msg), text="Transaction Details")
        self.config_bttns = [self.btn_party1, self.btn_party2, self.btn_bank1, self.btn_bank2, self.btn_msg]

        self.btn_party1.grid(column=1, row=2, sticky="nesw", pady=7)
        self.btn_party2.grid(column=1, row=3, sticky="nesw", pady=7)
        self.btn_bank1.grid( column=1, row=4, sticky="nesw", pady=7)
        self.btn_bank2.grid( column=1, row=5, sticky="nesw", pady=7)
        self.btn_msg.grid(   column=1, row=6, sticky="nesw", pady=7, columnspan=2)
        
        self.lbl_party1_name = tk.Label(self.frm_ft_bttns, anchor="w", text=self.master.main_entities.party1.name)
        self.lbl_party2_name = tk.Label(self.frm_ft_bttns, anchor="w", text=self.master.main_entities.party2.name)
        self.lbl_bank1_name  = tk.Label(self.frm_ft_bttns, anchor="w", text=self.master.main_entities.bank1.name)
        self.lbl_bank2_name  = tk.Label(self.frm_ft_bttns, anchor="w", text=self.master.main_entities.bank2.name)
        # self.lbl_msg    = tk.Label(self.frm_ft_bttns, anchor="w", text="[--- --- --- --- --- --- ---]")
        self.lbl_party1_name.grid(column=2, row=2, sticky="nesw", padx=(15,0), pady=7)
        self.lbl_party2_name.grid(column=2, row=3, sticky="nesw", padx=(15,0), pady=7)
        self.lbl_bank1_name.grid( column=2, row=4, sticky="nesw", padx=(15,0), pady=7)
        self.lbl_bank2_name.grid( column=2, row=5, sticky="nesw", padx=(15,0), pady=7)
        # self.lbl_msg.grid(   column=2, row=6, sticky="nesw", padx=(15,0), pady=7)

        # self.frm = 


# ================================================================================================================
# ================================================================================================================


CNV_WIDTH   = 960
CNV_HEIGHT  = 328 


BANK_TYPEA_WIDTH    = 6.4   #150
BANK_TYPEA_HEIGHT   = 2.187 #150
BANK_TYPEB_WIDTH    = 4.8   # 200
BANK_TYPEB_HEIGHT   = 1.64  # 200

MESSAGE_WIDTH   = 19.2  #50
MESSAGE_HEIGHT  = 10.93 #30
ARROW_WIDTH     = 6.4   #150
ARROW_HEIGHT    = 9.371 #35

DIV_X_1 = 7.9
DIV_X_2 = 3.75
DIV_Y   = 6

MOVE_INCREMENT   = 10
MOVES_PER_SECOND = 5
ANIMATION_SPEED  = 1000 // MOVES_PER_SECOND

class Animation(tk.Canvas):
    def __init__(self, master):
        super().__init__(master=master, width = CNV_WIDTH, height = CNV_HEIGHT, highlightthickness = 0)
        self.bind("<Configure>", self.on_resize)
        self.height     = self.winfo_reqheight()
        self.width      = self.winfo_reqwidth()
        self.direction  = None
        self.path       = None
        self.pause_time = 1000
        self.trx_events = 0
        self.trx_animations = [("e", "nw"), ("e", "se"), ("w", "ne"), ("w", "sw")]
        
        self.running_animation = False
        self.load_assets()
        self.create_objects()

    def perform_transaction(self, root, creditorAgent, creditor, debtor, debtorAgent, amount, xml_path):
        if self.trx_events == 0:
            write_logs(root, "Simulating a transaction")
            write_logs(root, "= = = = = = = = = = = = = = = ")
            write_logs(root, "Starting in 3 seconds...")
            self.direction, self.path = self.trx_animations[0]
            self.trx_events += 1
            self.pause_time = 3000
        elif self.trx_events == 1 and not self.running_animation:
            self.trx_events += 1
            self.pause_time = 2000
            write_logs(root, "Sending PACS008 Message to Central Node.")
            self.inisiate_message_animation(self.direction, self.path)
        elif self.trx_events == 2 and not self.running_animation:
            self.direction, self.path = self.trx_animations[1]
            write_logs(root, "\nCENTRAL NODE:\nValidating..")
            self.trx_events += 1
            self.pause_time = 2500
        elif self.trx_events == 3 and not self.running_animation:
            if validate_msg(SCHEMA_PACS008, xml_path):
                write_logs(root, " -> Message is Valid")
            else:
                write_logs(root, " -> Message is Invalid")
                write_logs(root, "Transaction is cancelled")
                self.path, self.direction = None, None
                self.trx_events = 0
                return
            self.trx_events += 1
            self.pause_time = 2500
        elif self.trx_events == 4 and not self.running_animation:
            write_logs(root, "Checking balance..")
            self.trx_events += 1
            self.pause_time = 2500
        elif self.trx_events == 5 and not self.running_animation:
            if (debtorAgent.validate_transaction(debtor, amount, send_money=False) and
                creditorAgent.validate_transaction(creditor, amount)):
                write_logs(root, " -> The balance is sufficient")
            else:
                write_logs(root, " -> Insufficient fund")
                write_logs(root, "Transaction is cancelled")
                self.path, self.direction = None, None
                self.trx_events = 0
                return
            self.trx_events += 1
            self.pause_time = 2500
        elif self.trx_events == 6 and not self.running_animation:
            write_logs(root, "Transferring  money from 'Creditor' to 'Debitor'")
            creditorAgent.send_money(creditor, amount)
            debtorAgent.receive_money(debtor, amount)
            root.update_balance()
            self.trx_events += 1
            self.pause_time = 2000
        elif self.trx_events == 7 and not self.running_animation:
            write_logs(root, "\nSending PACS008 Message to 'Debtor Agent'")
            self.trx_events += 1
            self.pause_time = 1000
        elif self.trx_events == 8 and not self.running_animation:
            self.trx_events += 1
            self.pause_time = 1000
            self.inisiate_message_animation(self.direction, self.path) 
        elif self.trx_events == 9 and not self.running_animation:
            self.direction, self.path = self.trx_animations[2]
            write_logs(root, "Sending confirmation PACS002 Message to 'Central Node'")
            self.trx_events += 1
            self.pause_time = 1000
        elif self.trx_events == 10 and not self.running_animation:
            self.trx_events += 1
            self.pause_time = 1000
            self.inisiate_message_animation(self.direction, self.path)
        elif self.trx_events == 11 and not self.running_animation:
            self.direction, self.path = self.trx_animations[3]
            write_logs(root, "Sending confirmation PACS002 Message to 'Creditor Agent'")
            self.trx_events += 1
            self.pause_time = 1000
        elif self.trx_events == 12 and not self.running_animation:
            self.trx_events += 1
            self.pause_time = 1000
            self.inisiate_message_animation(self.direction, self.path)
        elif self.trx_events == 13 and not self.running_animation:
            self.path, self.direction = None, None
            write_logs(root, "\nTransaction Success..")
            write_logs(
                root, 
                "IDR " + str(amount) + " of money has been transferred from "  + root.main_entities.party1.name + " to "
                + root.main_entities.party2.name + "\n\n\n"
            )
            self.trx_events = 0
            self.pause_time = 1000
            return None
        self.after(self.pause_time, self.perform_transaction, root, creditorAgent, creditor, debtor, debtorAgent, amount, xml_path)


    def inisiate_message_animation(self, direction, path):
        if self.running_animation:
            self.after(ANIMATION_SPEED, self.inisiate_message_animation, direction, path)
            return None
        else:
            self.running_animation = True
        if direction == "e":
            if path == "nw":
                start_x, end_x  = self.width/2  - self.width/DIV_X_2, self.width/2 - self.width/DIV_X_1
                coord_y         = self.height/2 - self.height/DIV_Y
            elif path == "sw":
                start_x, end_x  = self.width/2  - self.width/DIV_X_2, self.width/2 - self.width/DIV_X_1
                coord_y         = self.height/2 + self.height/DIV_Y
            elif path == "ne":
                start_x, end_x  = self.width/2  + self.width/DIV_X_1, self.width/2 + self.width/DIV_X_2 
                coord_y         = self.height/2 - self.height/DIV_Y
            elif path == "se":
                start_x, end_x  = self.width/2  + self.width/DIV_X_1, self.width/2 + self.width/DIV_X_2 
                coord_y         = self.height/2 + self.height/DIV_Y
            else: return None
        elif direction == "w":
            if path == "nw":
                start_x, end_x  = self.width/2 - self.width/DIV_X_1, self.width/2  - self.width/DIV_X_2
                coord_y         = self.height/2 - self.height/DIV_Y
            elif path == "sw":
                start_x, end_x  = self.width/2 - self.width/DIV_X_1, self.width/2  - self.width/DIV_X_2
                coord_y         = self.height/2 + self.height/DIV_Y
            elif path == "ne":
                start_x, end_x  = self.width/2 + self.width/DIV_X_2, self.width/2  + self.width/DIV_X_1
                coord_y         = self.height/2 - self.height/DIV_Y
            elif path == "se":
                start_x, end_x  = self.width/2 + self.width/DIV_X_2, self.width/2  + self.width/DIV_X_1
                coord_y         = self.height/2 + self.height/DIV_Y
            else: return None
        else: return None
        
        self.start_x = start_x
        self.end_x   = end_x
        self.coord_x  = start_x
        self.coord_y  = coord_y
        self.create_image(self.coord_x, self.coord_y, image = self.message_icon,
                            tag = "message")
        self.message_animation()

    def message_animation(self):        
        if self.direction == "e":
            if self.coord_x > self.end_x:
                self.delete(self.find_withtag("message"))
                self.running_animation = False
                return
            self.coord_x += MOVE_INCREMENT
        elif self.direction == "w":
            if self.coord_x < self.end_x:
                self.delete(self.find_withtag("message"))
                self.running_animation = False
                return
            self.coord_x -= MOVE_INCREMENT
        
        self.coords(self.find_withtag("message"), [self.coord_x, self.coord_y])
        self.after(ANIMATION_SPEED, self.message_animation)

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

    def load_assets(self):
        try:
            self.bank_icon_file     = Image.open(os.path.join(script_dir, "../img/p_bank.png"))
            self.arrow_icon_file    = Image.open(os.path.join(script_dir, "../img/p_arrow.png"))
            self.message_icon_file  = Image.open(os.path.join(script_dir, "../img/p_message.png"))

            self.bank_typeA_icon    = ImageTk.PhotoImage(self.bank_icon_file.resize((   int(CNV_WIDTH//BANK_TYPEA_WIDTH), int(CNV_HEIGHT/BANK_TYPEA_HEIGHT) )))
            self.bank_typeB_icon    = ImageTk.PhotoImage(self.bank_icon_file.resize((   int(CNV_WIDTH//BANK_TYPEB_WIDTH), int(CNV_HEIGHT/BANK_TYPEB_HEIGHT) )))
            self.arrow_icon         = ImageTk.PhotoImage(self.arrow_icon_file.resize((  int(CNV_WIDTH//ARROW_WIDTH     ), int(CNV_HEIGHT/ARROW_HEIGHT     ) )))
            self.message_icon       = ImageTk.PhotoImage(self.message_icon_file.resize((int(CNV_WIDTH//MESSAGE_WIDTH   ), int(CNV_HEIGHT/MESSAGE_HEIGHT   ) )))
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        self.create_image(self.width/2, self.height/2, image = self.bank_typeB_icon,
                            tag = "central_node")
        self.create_image(self.width/2 - self.width*.375, self.height/2, image = self.bank_typeA_icon,
                            tag = "bank1_node")
        self.create_image(self.width/2 + self.width*.375, self.height/2, image = self.bank_typeA_icon,
                            tag = "bank2_node")
        self.create_image(self.width/2 - self.width*.2, self.height/2, image = self.arrow_icon,
                            tag = "arrow1")
        self.create_image(self.width/2 + self.width*.2, self.height/2, image = self.arrow_icon,
                            tag = "arrow2")






PAD_Y = 3
ENTRIES_WIDTH = 40

LABELS_PRIVATEPARTY = [
    "Name", "StreetName", "Building Number", "Building Name", "Floor", "Postal Card", "Town Name", 
    "Country Sub Division", "Country", 
    "Birth Date", "Province of Birth", "City of Birth", "Country of Birth", "ID", "Issuer", 
    "Country of Resident", "Phone Number", "Mobile Number", "Fax Number", "Email Address"
]
IDS_PRIVATEPARTY = [
    "Nm", "StrtNm", "BldgNb", "BldgNm", "Flr", "PstCd", "TwnNm", 
    "CtrySubDvsn", "Ctry", 
    "BirthDt", "PrvcOfBirth", "CityOfBirth", "CtryOfBirth", "Id", "Issr", 
    "CtryOfRes", "PhneNb", "MobNb", "FaxNb", "EmailAdr"
]
LABELS_ORGPARTY = [
    "Name", "StreetName", "Building Number", "Building Name", "Floor", "Postal Card", "Town Name", 
    "Country Sub Division", "Country", 
    "AnyBIC", "LEI", "Ientification", "Issuer", 
    "Country of Resident", "Phone Number", "Mobile Number", "Fax Number", "Email Address"
]
IDS_ORGPARTY = [
    "Nm", "StrtNm", "BldgNb", "BldgNm", "Flr", "PstCd", "TwnNm",
    "CtrySubDvsn", "Ctry",
    "AnyBIC", "LEI", "Id", "Issr", 
    "CtryOfRes", "PhneNb", "MobNb", "FaxNb", "EmailAdr"  
]

LABELS_FI = [
    "BICFI", "Member ID", "LEI", "Name", 
    "StreetName", "Building Number", "Building Name", "Floor", "Postal Card", "Town Name", "Country Sub Division", "Country"
]
IDS_FI = [
    "BICFI", "MmbId", "LEI", "Nm", "StrtNm", "BldgNb", "BldgNm", "Flr", "PstCd", "TwnNm", "CtrySubDvsn", "Ctry"
]

LABELS_MSG = [
    "Message ID", "Nb of Transactions", "Instruction ID", 
    "End-to-End ID", "Transaction ID", "UETR", "Clearing System Ref", 
    "Settlement Amount", "Charge Bearer"    
]
IDS_MSG = [
    "MsgId", "NbOfTxs", "InstrId", "EndToEndId", "TxId", "UETR", "ClrSysRef", "IntrBkSttlmAmt", "ChrgBr"
]



class Form(tk.Frame):
    def __init__(self, entities, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.main_entities = entities
        self.columnconfigure(0, minsize=150)
        self.frm_label = tk.Frame(self)
        self.frm_entry = tk.Frame(self)
        self.frm_button= tk.Frame(self)
        self.frm_label.grid(column=0, row=0, sticky="nes")
        self.frm_entry.grid(column=1, row=0, sticky="nesw")
        self.frm_button.grid(column=1, row=1, sticky="nesw")

        # ===== CONTROL BUTTONS =====
        self.btn_clear  = tk.Button(self.frm_button, text="Clear", width=9, pady=3, command=lambda:clear_values(self))
        self.btn_clear.pack(side="right", padx=10, pady=(10,5))

        # ===== Vars =====
        self.entries = {}
        self.Labels  = {}



class Form_Prvt(Form):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # =========>>>  FORM LABELS  <<<=========
        self.labels = {
            IDS_PRIVATEPARTY[i]:tk.Label(self.frm_label, anchor="w", text=LABELS_PRIVATEPARTY[i]) 
            for i in range(len(LABELS_PRIVATEPARTY))
        }
        [lbl.grid(column=0, pady=PAD_Y, padx=(5, 5), sticky = "nsew") for lbl in self.labels.values()]
        [tk.Label(self.frm_label, text=":").grid(column=1, pady=PAD_Y, padx=5, row=i, sticky = "ns") for i in range(len(self.labels))]
        
        # =========>>>  FORM ENTRIES  <<<=========
        self.entries = {ent:tk.Entry(self.frm_entry, width=ENTRIES_WIDTH) for ent in IDS_PRIVATEPARTY}
        [ent.grid(column=0, pady=PAD_Y+1, padx=(3, 3), sticky = "nsew") for ent in self.entries.values()]

        # =========>>>  BUTTONS  <<<=========
        self.btn_default= tk.Button(self.frm_button, text="Default", width=9, pady=3, command=lambda:write_values(self, self.main_entities, "party1", True))
        self.btn_save   = tk.Button(self.frm_button, text="Save", width=9, pady=3, command=lambda:save_values(self, self.main_entities, "party1"))
        self.btn_default.pack(side="left", padx=5, pady=(10,5))
        self.btn_save.pack(side="right", pady=(10,5))
        write_values(self, self.main_entities, "party1")


class Form_Org(Form):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # =========>>>  FORM LABELS  <<<=========
        self.labels = {
            IDS_ORGPARTY[i]:tk.Label(self.frm_label, anchor="w", text=LABELS_ORGPARTY[i]) 
            for i in range(len(LABELS_ORGPARTY))
        }
        [lbl.grid(column=0, pady=PAD_Y, padx=(5, 5), sticky = "nsew") for lbl in self.labels.values()]
        [tk.Label(self.frm_label, text=":").grid(column=1, pady=PAD_Y, padx=5, row=i, sticky = "ns") for i in range(len(self.labels))]
        
        # =========>>>  FORM ENTRIES  <<<=========
        self.entries = {lbl:tk.Entry(self.frm_entry, width=ENTRIES_WIDTH) for lbl in IDS_ORGPARTY}
        [ent.grid(column=0, pady=PAD_Y+1, padx=(3, 3), sticky = "nsew") for ent in self.entries.values()]

        # =========>>>  BUTTONS  <<<=========
        self.btn_default= tk.Button(self.frm_button, text="Default", width=9, pady=3, command=lambda:write_values(self, self.main_entities, "party2", True))
        self.btn_save   = tk.Button(self.frm_button, text="Save", width=9, pady=3, command=lambda:save_values(self, self.main_entities, "party2"))
        self.btn_default.pack(side="left", padx=5, pady=(10,5))
        self.btn_save.pack(side="right", pady=(10,5))
        write_values(self, self.main_entities, "party2")

class Form_FI(Form):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # =========>>>  FORM LABELS  <<<=========
        self.labels = {
            IDS_FI[i]:tk.Label(self.frm_label, anchor="w", text=LABELS_FI[i]) 
            for i in range(len(LABELS_FI))
        }
        [lbl.grid(column=0, pady=PAD_Y, padx=(5, 5), sticky = "nsew") for lbl in self.labels.values()]
        [tk.Label(self.frm_label, text=":").grid(column=1, pady=PAD_Y, padx=5, row=i, sticky = "ns") for i in range(len(self.labels))]
        
        # =========>>>  FORM ENTRIES  <<<=========
        self.entries = {lbl:tk.Entry(self.frm_entry, width=ENTRIES_WIDTH) for lbl in IDS_FI}
        [ent.grid(column=0, pady=PAD_Y+1, padx=(3, 3), sticky = "nsew") for ent in self.entries.values()]

class Form_FI_1(Form_FI):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # =========>>>  BUTTONS  <<<=========
        self.btn_default= tk.Button(self.frm_button, text="Default", width=9, pady=3, command=lambda:write_values(self, self.main_entities, "bank1", True))
        self.btn_save   = tk.Button(self.frm_button, text="Save", width=9, pady=3, command=lambda:save_values(self, self.main_entities, "bank1"))
        self.btn_default.pack(side="left", padx=5, pady=(10,5))
        self.btn_save.pack(side="right", pady=(10,5))
        write_values(self, self.main_entities, "bank1")

class Form_FI_2(Form_FI):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # =========>>>  BUTTONS  <<<=========
        self.btn_default= tk.Button(self.frm_button, text="Default", width=9, pady=3, command=lambda:write_values(self, self.main_entities, "bank2", True))
        self.btn_save   = tk.Button(self.frm_button, text="Save", width=9, pady=3, command=lambda:save_values(self, self.main_entities, "bank2"))
        self.btn_default.pack(side="left", padx=5, pady=(10,5))
        self.btn_save.pack(side="right", pady=(10,5))
        write_values(self, self.main_entities, "bank2")

class Form_Msg(Form):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # =========>>>  FORM LABELS  <<<=========
        self.labels = {
            IDS_MSG[i]:tk.Label(self.frm_label, anchor="w", text=LABELS_MSG[i]) 
            for i in range(len(LABELS_MSG))
        }
        [lbl.grid(column=0, pady=PAD_Y, padx=(5, 5), sticky = "nsew") for lbl in self.labels.values()]
        [tk.Label(self.frm_label, text=":").grid(column=1, pady=PAD_Y, padx=5, row=i, sticky = "ns") for i in range(len(self.labels))]
        
        # =========>>>  FORM ENTRIES  <<<=========
        self.entries = {lbl:tk.Entry(self.frm_entry, width=ENTRIES_WIDTH) for lbl in IDS_MSG}
        [ent.grid(column=0, pady=PAD_Y+1, padx=(3, 3), sticky = "nsew") for ent in self.entries.values()]

        # =========>>>  BUTTONS  <<<=========
        self.btn_default= tk.Button(self.frm_button, text="Default", width=9, pady=3, command=lambda:write_values(self, self.main_entities, "msg", True))
        self.btn_save   = tk.Button(self.frm_button, text="Save", width=9, pady=3, command=lambda:save_values(self, self.main_entities, "msg"))
        self.btn_default.pack(side="left", padx=5, pady=(10,5))
        self.btn_save.pack(side="right", pady=(10,5))
        write_values(self, self.main_entities, "msg")


# ================================================================================================================
# ================================================================================================================

class Logs(tk.Text):
    def __init__(self, parent, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.insert(
            "1.0", 
            "==================================\n"
            + "ISO 20022 PACS.008 Message Simulation\n" 
            + "==================================\n"
            + "{} - {}\n\n".format(datetime.date.today(), datetime.datetime.now().time().strftime("%H:%M:%S"))
            + "Starting..\n"
            + "Assigning default values to corresponding parties and FIs..\n\n"
        )
        self.configure(state="disabled")

    def send_message(self, text):
        self.configure(state="normal")
        self.insert("end", "\n"+text)
        self.see("end")
        self.configure(state="disabled")



# ================================================================================================================
# ================================================================================================================

class Viewer(tk.Frame):
    def __init__(self, entities, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.main_entities = entities

        self.txt_msg = tk.Text(self, borderwidth=3, height=40)
        self.txt_msg.pack(expand=True, fill="both")
        self.btn_validity = tk.Button(self, text="Check Validity", command=lambda:self.validate_msg())
        self.btn_validity.pack(pady=(15,0))
        self.write_msg()

    def validate_msg(self):
        xml_string = self.get_msg()
        msg = etree.parse(BytesIO(xml_string.encode()))
        try:
            SCHEMA_PACS008.assertValid(msg)
        except Exception as e:
            tkinter.messagebox.showinfo("", "The message is INVALID:\n\n\n{e}".format(e=e))
        else:
            tkinter.messagebox.showinfo("", "The message is VALID")

    def write_msg(self):
        xml = create_msg(XML_PACS008, self.main_entities.getISO_Msg(*self.main_entities.get_entity_values("msg")))
        txt=etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
        self.txt_msg.insert("1.0", txt)

    def get_msg(self):
        return self.txt_msg.get("1.0", "end")





if __name__ == "__main__":
    from entities import Entities
    from ISO_pacs008 import XML_PACS008, SCHEMA_PACS008, create_msg, write_msg, validate_msg
    
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    main_entities = Entities()
    root = MainApplication(main_entities)
    # write_logs(root, "hahahahahahaha\n\n\n\n\n\n\n\nhahahaha")
    root.mainloop()