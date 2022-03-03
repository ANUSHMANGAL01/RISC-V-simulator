from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from ctypes import alignment, windll
from tkinter import filedialog
import os
from tkinter import messagebox
import simul1

# Defining root
root = Tk()
root.title("risc-v-simulator")

# Enabling dpi scaling
windll.shcore.SetProcessDpiAwareness(1)

# Simulator body panel
simulator_body= PanedWindow(orient = VERTICAL,width=1600, height=800,bg="black");
simulator_body.pack(fill=BOTH,expand=1)

# Top panel
top_panel = PanedWindow(simulator_body,bd=1,relief="raised",bg="white");
top_panel.pack(fill=BOTH,expand=1)
simulator_body.add(top_panel);

# Top panel functions
# Function to upload a file
def upload_file():
    root.filename=filedialog.askopenfilename(initialdir="../RISC-V-simulator/Phase1",title="Select a file",filetypes=(("assembly files",".s"),("assembly files",".asm")))
    simul1.new_file_name=root.filename
    clear_all()
    simul1.load_code()
    display_data()
    display_registers()

# Top panel buttons
file_upload_button=Button(top_panel, text="File upload",font=("Roboto", 14),command=upload_file)
file_upload_button.pack(side=LEFT, pady=2)

help_button=Button(top_panel, text="Help",font=("Roboto", 14))
help_button.pack(side=LEFT, padx=15, pady=2)

quit_button = Button(top_panel,text=" Exit ",font=("Roboto", 14),command =root.quit)
quit_button.pack(side=RIGHT, padx=15, pady=2)

# Title panel
title_panel=PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(title_panel);

title_label = Label(title_panel, text="RISC-V SIMULATOR", font=("Roboto", 20))
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
def toggle_button_colour(but_1,but_2):
    but_1_colour = but_1.cget('bg')
    but_1.configure(bg=but_2.cget('bg'))
    but_2.configure(bg=but_1_colour)
    if(but_1.cget('bg') == "cyan"):
        display_registers()
    else:
        display_memory()

# Buttons for register-memory panel
reg_button = Button(reg_mem_panel_title, text="REGISTERS", height=1, font=("Roboto", 14),bg="cyan",command =lambda: toggle_button_colour(reg_button,mem_button))
reg_button.pack(side=LEFT)

mem_button = Button(reg_mem_panel_title, text="MEMORY", height=1, font=("Roboto", 14), bg="white",command=lambda:toggle_button_colour(reg_button,mem_button))
mem_button.pack(side=LEFT)

# Functions for code panel
# Function to clear the code panel and reset the memory and register values
def clear_all():
    simul1.clear_all()
    code_text.delete("1.0","end")
    reg_mem_text.delete("1.0", "end")
    display_registers()

# Function to run the code at once
def run_at_once():
    if(simul1.PROCESSED_LINES == []):
         messagebox.showinfo("Blank File","Please upload an assembly file")
    else:
        simul1.run()
        display_registers()

# Function for step by step execution
def run_step():
    messagebox.showinfo("Work in progress","Sorry , we don't have that functionality yet .")
# Buttons for code panel
code_panel_label = Button(code_panel_title, text="CODE TEXT", height=1, font=("Roboto", 14),activebackground='red',bg='white',state=DISABLED)
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
scroll_user = Scrollbar(code_body, orient="vertical")
scroll_reg.pack(side=RIGHT, fill=Y)
scroll_user.pack(side=RIGHT, fill=Y)

# Console Panel
# console_panel = PanedWindow(code_panel, orient="vertical", relief="raised", bg="white")
# code_panel.add(console_panel)

# console_title = Label(console_panel, text="CONSOLE", relief="raised", height=1, font=("Arial", 10))
# console_panel.add(console_title)

# console = Label(console_panel, font=("Roboto", 14), fg="yellow")
# console_panel.add(console)

# Status Panel -> Return status of program (whether it has finshed or there are some errors
status_panel = PanedWindow(simulator_body,orient=VERTICAL, relief="raised", bg="white")
simulator_body.add(status_panel)

status = Label(status_panel, font=("Roboto", 14), fg="green")
status_panel.add(status)

# Hnadling gui data
code_text = Text(code_body, yscrollcommand = scroll_user.set,font=("Roboto", 14) )

reg_mem_text = Text(reg_mem_body,yscrollcommand=scroll_reg.set,font=("Roboto", 14),bg="cyan")


def display_registers():
    reg_mem_text.delete("1.0", "end")
    for i in simul1.REGISTERS:
            reg_mem_text.insert(END, str(i) + " = " + str(simul1.REGISTERS[i])+ "\n")
    reg_mem_text.pack(side=TOP, fill=X)
    scroll_user.config(command=reg_mem_text.yview)

def display_memory():
    reg_mem_text.delete("1.0", "end")
    j=0
    for i in simul1.MEMORY:
            reg_mem_text.insert(END, str(j) + " = " + str(i)+ "\n")
            j+=1
    reg_mem_text.pack(side=TOP, fill=X)
    scroll_user.config(command=reg_mem_text.yview)

def display_data():
    code_text.delete("1.0","end")
    j=1
    for i in simul1.PROCESSED_LINES:
            code_text.insert(END, str(j) + " : " + str(i)+"\n")
            j+=1
    code_text.pack(side=TOP, fill=X)
    scroll_user.config(command=code_text.yview)

display_data()
display_registers()

root.mainloop()
