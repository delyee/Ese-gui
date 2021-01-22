import tkinter
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile, askdirectory
from tkinter.messagebox import showerror
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from collections import Counter
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
from jinja2 import Template


FILE_NAME = tkinter.NONE

def open_folder():
    global FOLDER_NAME
    FOLDER_NAME = askdirectory()
    print(dir(FOLDER_NAME))
    print(FOLDER_NAME)

def save_as():
    out = asksaveasfile(mode='w', defaultextension='yar')
    data = text_rule.get('1.0', tkinter.END)
    try:
        out.write(data)
    except Exception:
        showerror(title="Error", message="Saving file error")

def open_file():
    global FILE_NAME
    inp = askopenfile(mode="r")
    if inp is None:
        return
    FILE_NAME = inp.name
    data = inp.read()
    text_src.delete('1.0', tkinter.END)
    text_src.insert('1.0', data)
    getMostCommon()


root = tkinter.Tk()
root.title("test")

f_src_text = LabelFrame(root, text="src text")
f_most_common = LabelFrame(root, text="most common patterns")
f_rule = LabelFrame(root, text="rule")

f_src_text.pack(side=TOP, padx=10, pady=10, ipadx=10, ipady=10)
f_most_common.pack(side=LEFT, padx=10, pady=10, ipadx=10, ipady=10)
f_rule.pack(side=LEFT, padx=10, pady=10, ipadx=10, ipady=10)

#root.minsize(width=1000, height=1000)
#root.maxsize(width=1200, height=1000)

text_src = scrolledtext.ScrolledText(f_src_text, undo=True, width=200, height=20) #tkinter.Text(f_src_text, width=500, height=20)
#text_common = scrolledtext.ScrolledText(f_most_common, undo=True, width=100, height=20) #tkinter.Text(f_most_common, width=100, height=20)
listbox_patterns = Listbox(f_most_common, selectmode=MULTIPLE, width=70, height=20) #tkinter.Text(f_most_common, width=100, height=20)
text_rule = scrolledtext.ScrolledText(f_rule, undo=True, width=100, height=24) #tkinter.Text(f_rule, width=100, height=20)

text_src.pack(side=LEFT, expand=2, ipadx=10, ipady=10)
listbox_patterns.pack(side=LEFT, expand=2) # ipadx=10, ipady=10
text_rule.pack(side=LEFT, expand=2, ipadx=10, ipady=10)

def otherSplit(s):
    _chars = ['\n', ' ', ';', '+', '%', '//', '*/', '/*', '=', '&&', '(', ')']
    _ = []
    for _char in _chars:
        for iter1 in s.split(_char):
            if len(iter1) <= 128:
                _.append(iter1.strip())
    return _

def getMostCommon():
    s = text_src.get(1.0, END)
    all_lines = []

    # splitlines != split, read docs
    for line in s.splitlines():
        for split_line in otherSplit(line):
            all_lines.append(split_line)

    listbox_patterns.delete('0', tkinter.END)
    all_lines = sorted(set(all_lines), key=len)
    all_lines.sort()
    #for line in sorted(set(all_lines), key=len):
    for line in all_lines:
        #_tmp = '{}\n'.format(i)
        listbox_patterns.insert(END, line)
 

def genRule():
    text_rule.delete('1.0', tkinter.END)
    if FILE_NAME == tkinter.NONE:
        _sha256sum = sha256(text_src.get(1.0, END).encode()).hexdigest()
    else:
        _sha256sum = sha256(open(FILE_NAME, 'rb').read()).hexdigest()
    _strings = []
    selected_text_list = [listbox_patterns.get(i) for i in listbox_patterns.curselection()]
    for line in selected_text_list:
        _mda = " ".join("{:02x}".format(ord(c)) for c in line)
        _strings.append(_mda)
    
    with open('template.jinja2') as f_template:
        template = Template(f_template.read())

    _tmp = template.render(rulename=uuid4().hex, date=datetime.now().strftime("%d.%m.%Y"), sha256sum=_sha256sum, strings=_strings)
    text_rule.insert('1.0', _tmp)


menuBar = tkinter.Menu(root)
fileMenu = tkinter.Menu(menuBar)
fileMenu.add_command(label="Open Folder", command=open_folder)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save as", command=save_as)
fileMenu.add_command(label="getMostCommon", command=getMostCommon)
fileMenu.add_command(label="genRule", command=genRule)

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Exit", command=root.quit)
root.config(menu=menuBar)


root.mainloop()
