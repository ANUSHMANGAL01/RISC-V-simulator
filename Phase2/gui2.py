from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from ctypes import alignment, windll
from tkinter import filedialog
from time import strftime
import os
from tkinter import messagebox
from typing import overload
import simul2

# Defining root
root = Tk()
root.title("risc-v-simulator")

global line_number, ran_before
line_number = 0
ran_before = False   # used in the step by step running function

# Prompts
def info_prompt(msg1,msg2):
    messagebox.showinfo(msg1,msg2)

# Status messages
def status_display(str1):
    system_time = strftime('%H:%M:%S %p')
    status_text.configure(state='normal',bg='black',fg='cyan')
    status_text.delete("1.0","end")
    status_text.tag_config('time', foreground="#FF0000")
    status_text.insert(END,system_time+" : ",'time')
    status_text.insert(END, str1 + "\n")
    status_text.pack(side=TOP, fill=X)
    scroll_status.config(command=code_text.yview)
    status_text.configure(state='disabled')

def status_display_3(str1,str2,str3):
    system_time = strftime('%H:%M:%S %p')
    status_text.configure(state='normal',bg='black',fg='cyan')
    status_text.delete("1.0","end")
    status_text.tag_config('time', foreground="#FF0000")
    status_text.tag_config('file_upload', foreground="#03A062")
    status_text.insert(END,system_time+" : ",'time')
    status_text.insert(END,str1)
    status_text.insert(END,str2,'file_upload')
    status_text.insert(END, str3 + "\n")
    status_text.pack(side=TOP, fill=X)
    scroll_status.config(command=code_text.yview)
    status_text.configure(state='disabled')

# Enabling dpi scaling
windll.shcore.SetProcessDpiAwareness(1)

# Simulator body panel
simulator_body= PanedWindow(orient = VERTICAL,width=1600, height=800,bg="black");
simulator_body.pack(fill=BOTH,expand=1)

# Top panel
top_panel = PanedWindow(simulator_body,bd=1,relief="raised",bg="white");
top_panel.pack(fill=BOTH,expand=1)
simulator_body.add(top_panel);

# Button animations
# Hover
def custom_button(my_panel,text,bgcolor,fgcolor,wid,cmd):
    def on_enter(e):
        my_button['background']=bgcolor
        my_button['foreground']=fgcolor

    def on_leave(e):
        my_button['background']=fgcolor
        my_button['foreground']=bgcolor

    my_button=Button(my_panel,width=wid,height=1,font=("Roboto", 14),text=text,fg=bgcolor,bg=fgcolor,border=0,activeforeground=fgcolor,activebackground=bgcolor,command=cmd)
    my_button.bind("<Enter>",on_enter)
    my_button.bind("<Leave>",on_leave)
    return my_button
# Top panel functions
# Function to upload a file
def upload_file():
    root.filename=filedialog.askopenfilename(initialdir="../RISC-V-simulator/Phase1",title="Select a file",filetypes=(("assembly files",".s"),("assembly files",".asm")))
    simul2.new_file_name=root.filename
    clear_all()
    try:
        simul2.load_code()
    except Exception as e:
        info_prompt('error',e)
    display_data()
    if(reg_button.cget('bg')=='cyan'):
        display_registers()
    else:
        display_memory()
    status_display_3("New file - ",os.path.basename(root.filename)," uploaded.")

# Top panel buttons
file_upload_button=custom_button(top_panel,"Upload File","cyan","black",10, upload_file)
file_upload_button.pack(side=LEFT, pady=2)

help_button=custom_button(top_panel,"Help","cyan","black",10,lambda:info_prompt("Work in progress","Sorry , we don't have that functionality yet."))
help_button.pack(side=LEFT, padx=15, pady=2)

quit_button = custom_button(top_panel,"Exit","cyan","black",10, root.quit)
quit_button.pack(side=RIGHT, padx=15, pady=2)

# Title panel
title_panel=PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(title_panel);

title_label = Label(title_panel, text="RISC-V SIMULATOR", font=("Roboto", 25,'bold'))
title_panel.add(title_label)

# Body Panel
body_panel = PanedWindow(simulator_body, orient=HORIZONTAL, relief="raised", bg="black")
simulator_body.add(body_panel)

# Register Panel
reg_mem_panel = PanedWindow( body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(reg_mem_panel)

# Code Panel
code_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(code_panel)

# Title Panels
reg_mem_panel_title = PanedWindow(reg_mem_panel, bd=1, relief="raised")
code_panel_title = PanedWindow(code_panel, bd=1, relief="raised")
reg_mem_panel.add(reg_mem_panel_title)
code_panel.add(code_panel_title)

# Toggle function -> Toggles the view of memory and registers on click
def change_button_colour(but_1,but_2,status):
    if(but_1.cget('bg') == "cyan" and status==1):
        but_1.configure(bg="white")
        but_2.configure(bg="cyan")
        display_memory()
    elif(but_2.cget('bg') == "cyan" and status==0):
        but_2.configure(bg="white")
        but_1.configure(bg="cyan")
        display_registers()

def clear_reg_mem_fields():
    global ran_before,line_number
    ran_before=False
    simul2.clear_all()
    simul2.load_code()
    reg_mem_text.delete("1.0", "end")
    code_text.config(state='normal')
    code_text.tag_remove("start", str(line_number)+str('.0'),str(line_number)+str('.')+str(1000))
    if(reg_button.cget('bg')=='cyan'):
        display_registers()
    else:
        display_memory()
    line_number=0
    status_display("Registers and memory cleared")

# Buttons for register-memory panel
reg_button = Button(reg_mem_panel_title, text="REGISTERS", height=1, font=("Roboto", 14),bg="cyan",command =lambda: change_button_colour(reg_button,mem_button,0))
reg_button.pack(side=LEFT)

mem_button = Button(reg_mem_panel_title, text="MEMORY", height=1, font=("Roboto", 14), bg="white",command=lambda:change_button_colour(reg_button,mem_button,1))
mem_button.pack(side=LEFT)

clear_fields_button = custom_button(reg_mem_panel_title,"Clear Fields","cyan","black",10, clear_reg_mem_fields)
clear_fields_button.pack(side=RIGHT,padx=10)

# Functions for code panel
# Function to clear the code panel and reset the memory and register values
def clear_all():
    global ran_before
    ran_before=False
    simul2.clear_all()
    code_text.configure(state='normal')
    code_text.delete("1.0","end")
    code_text.configure(state='disabled')
    reg_mem_text.delete("1.0", "end")
    if(reg_button.cget('bg')=='cyan'):
        display_registers()
    else:
        display_memory()
    status_display("Registers and memory cleared")

# Function to run the code at once
def run_at_once():
    global ran_before
    ran_before=False
    if(simul2.PROCESSED_LINES == []):
         info_prompt("Blank File","Please upload an assembly file")
    else:
        try:
            simul2.run()
            if(reg_button.cget('bg')=='cyan'):
                display_registers()
            else:
                display_memory()
            status_display("Finished simulation")
        except Exception as e:
            info_prompt("Error occurred", e)

#Define a function to highlight the text
def add_highlighter(text, line_number):
   text.tag_add("start", "1.11","1.17")
   text.tag_config("start", background="OliveDrab1", foreground="black")

# Function for step by step execution
def run_step():
    global line_number, ran_before
    if(line_number == len(simul2.PROCESSED_LINES)):
        code_text.config(state='disabled')
        info_prompt("Program end","The program has ended")
        status_display("Finished simulation")
        return
    if(simul2.PROCESSED_LINES == []):
         info_prompt("Blank File","Please upload an assembly file")
    else: 
        try:
            if(ran_before):
                code_text.config(state='normal')
                code_text.tag_remove("start", str(line_number)+str('.0'),str(line_number)+str('.')+str(1000))
                simul2.run_one_by_one(line_number=line_number-1)
                line_number = simul2.i+1   
                code_text.tag_add("start", str(line_number)+str('.0'),str(line_number)+str('.')+str(1000))
                if(simul2.PROCESSED_LINES[line_number-1]==""):
                    code_text.tag_config("start", background="black", foreground="cyan")
                else: 
                    code_text.tag_config("start", background="black", foreground="yellow")
                code_text.config(state='disabled')
            else:
                simul2.find_labels(0)
                line_number=simul2.LABELS["main"]
                simul2.run_one_by_one(line_number=line_number)
                line_number = simul2.i+1
                code_text.config(state='normal')
                code_text.tag_add("start", str(line_number)+str('.0'),str(line_number)+str('.')+str(1000))
                code_text.tag_config("start", background="black", foreground="yellow")
                code_text.config(state='disabled')
                ran_before=True
            if(reg_button.cget('bg')=='cyan'):
                display_registers()
            else:
                display_memory()

        except Exception as e:
            code_text.config(state=DISABLED)
            info_prompt("Error occurred", e)
    
# Buttons for code panel
code_panel_label = Button(code_panel_title, text="CODE TEXT", height=1, font=("Roboto", 14),bg='white')
code_panel_label.pack(side=LEFT)

clear_code_button = Button(code_panel_title, text="CLEAR CODE", height=1, font=("Roboto", 14),command=clear_all,activebackground='red')
clear_code_button.pack(side=LEFT)

run_code_at_once_button = Button(code_panel_title, text="RUN AT ONCE", height=1, font=("Roboto", 14),command=run_at_once,activebackground='red')
run_code_at_once_button.pack(side=LEFT)

run_code_step_button = Button(code_panel_title, text="RUN STEPWISE", height=1, font=("Roboto", 14),activebackground='red',command=run_step)
run_code_step_button.pack(side=LEFT)

# Body Panel of Register and Memory and User
reg_mem_body = PanedWindow(reg_mem_panel, bg="cyan")
code_body = PanedWindow(code_panel, bg="white")

reg_mem_panel.add(reg_mem_body)
code_panel.add(code_body)

# Scrollbars
scroll_reg = Scrollbar(reg_mem_body, orient="vertical")
scroll_code = Scrollbar(code_body, orient="vertical")

scroll_reg.pack(side=RIGHT, fill=Y)
scroll_code.pack(side=RIGHT, fill=Y)


# Console Panel
# console_panel = PanedWindow(code_panel, orient="vertical", relief="raised", bg="white")
# code_panel.add(console_panel)

# console_title = Label(console_panel, text="CONSOLE", relief="raised", height=1, font=("Arial", 10))
# console_panel.add(console_title)

# console = Label(console_panel, font=("Roboto", 14), fg="yellow")
# console_panel.add(console)
    
def display_status_messages():
    status_text.config(state='normal',fg='cyan',bg='black')
    status_text.delete("1.0","end")
    status_text.config(state="disabled")

def handle_forwarding():
    # global ran_before
    # print(ran_before)
    # if(ran_before == False):
    #     display_pipeline_forwarding_matrix(False)
    #     return
    display_pipeline_forwarding_matrix(True)
    return

def handle_non_forwarding():
    # global ran_before
    # if(ran_before == False):
    #     display_pipeline_non_forwarding_matrix(False)
    #     return
    display_pipeline_non_forwarding_matrix(True)
    return

# Status Panel -> Return status of program (whether it has finshed or there are some errors
status_panel = PanedWindow(simulator_body,orient=VERTICAL, relief="raised", bg="black",bd=0)
simulator_body.add(status_panel)

status_title = PanedWindow(status_panel, bd=1, relief="raised")
status_panel.add(status_title)

status_button = custom_button(status_title,"Status Bar","cyan","black",17, display_status_messages)
status_button.pack(side=LEFT, pady=1)

pipeline_forwarding_button = custom_button(status_title,"Pipeline Forwarding","cyan","black",17, handle_forwarding)
pipeline_forwarding_button.pack(side=LEFT,padx=10, pady=1)

pipeline_non_forwarding_button = custom_button(status_title,"Pipeline non-Forwarding","cyan","black",20, handle_non_forwarding)
pipeline_non_forwarding_button.pack(side=LEFT,padx=10, pady=1)

status_panel_body = PanedWindow(status_panel, bg="black")
status_panel.add(status_panel_body)

scroll_status = Scrollbar(status_panel_body, orient="vertical")
scroll_status.pack(side=LEFT,fill=Y)

# Handling gui data
code_text = Text(code_body, yscrollcommand = scroll_code.set,font=("Roboto", 14) )

reg_mem_text = Text(reg_mem_body,yscrollcommand=scroll_reg.set,font=("Roboto", 14),bg="cyan")

status_text = Text(status_panel_body,yscrollcommand=scroll_reg.set,font=("Roboto", 14),bg="black",fg='cyan')

def display_registers():
    reg_mem_text.configure(state='normal')
    reg_mem_text.delete("1.0", "end")
    for i in simul2.REGISTERS:
            reg_mem_text.insert(END, str(i) + " = " + str(simul2.REGISTERS[i])+ "\n")
    reg_mem_text.pack(side=TOP, fill=X)
    scroll_code.config(command=reg_mem_text.yview)
    reg_mem_text.configure(state='disabled')

def display_memory():
    reg_mem_text.configure(state='normal')
    reg_mem_text.delete("1.0", "end")
    j=268500992
    # reg_mem_text.insert(END, "The memory starts from the location 268500992 (which is 0x10010000 in hexadecimal) and ends at 268697599 (which is 0x1003ffff in hexadecimal). Each memory element is of four bytes.\n")
    for i in simul2.MEMORY:
            reg_mem_text.insert(END, str(j) + " = " + str(i)+ "\n")
            j+=4
    reg_mem_text.pack(side=TOP, fill=X)
    scroll_code.config(command=reg_mem_text.yview)
    reg_mem_text.configure(state='disabled')

def display_data():
    code_text.configure(state='normal')
    code_text.delete("1.0","end")
    j=0
    for i in simul2.PROCESSED_LINES:
            code_text.insert(END, str(j) + " : " + str(i)+"\n")
            j+=1
    code_text.pack(side=TOP, fill=X)
    scroll_code.config(command=code_text.yview)
    code_text.configure(state='disabled')

def display_pipeline_forwarding_matrix(status):
    status_text.config(state='normal',bg='white',fg='black')
    status_text.delete("1.0","end")
    # if(status == False):
    #     status_text.insert(END,"Please run the simulation")
    #     status_text.config(state='disabled')
    #     return

    for i in simul2.forwarding_pipeline_matrix:
        for j in i:
            status_text.insert(END, "  "+j)
        status_text.insert(END,'\n')
    status_text.config(state='disabled')

def display_pipeline_non_forwarding_matrix(status):
    status_text.config(state='normal',bg='white',fg='black')
    status_text.delete("1.0","end")
    # if(status == False):
    #     status_text.insert(END,"Please run the simulation")
    #     status_text.config(state='disabled')
    #     return

    for i in simul2.non_forwarding_pipeline_matrix:
        for j in i:
            status_text.insert(END, "  "+j)
        status_text.insert(END,'\n')
    status_text.config(state='disabled')


display_data()
display_registers()

root.mainloop()
