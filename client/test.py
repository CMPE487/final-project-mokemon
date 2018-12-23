from tkinter import *
from tkinter import simpledialog
from collections import OrderedDict
a = [False,True]
print(any(a))
exit()
# a = OrderedDict()
# a["asd"] = (1,23)
# a["dsa"] = (0,24)
# print(dir(a))
# a.pop()
# print(a[list(a.keys())[0]])
# exit()
def inp():
    global inpt
    number=inpt.get()
    try:
        int(number)
        info.configure(text=number)
    except ValueError:
        info.configure(text="Please enter an integer")
    root.update()
root=Tk()
# root.geometry("300x100-0+0")
# Label(root,text="Input ", height=1, width=7).grid(row=0)
# inpt=Entry(root, width=35)
# inpt.grid(row=0, column=1)
# info=Label(root,text="", height=1)
# info.grid(row=3, column=1)
# get=Button(root, text="Input", command=inp)
# get.grid(row=2, column=1)

# listbox = Listbox(root)
# listbox.pack()

# listbox.insert(END, "a list entry")

# for item in ["one", "two", "three", "four"]:
    # listbox.insert(END, item)

def onselect(evt):
    global lb
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print('You selected item %d: "%s"' % (index, value))
    lb.delete(0)

lb = Listbox(root, name='lb')
lb.pack()
lb.bind('<<ListboxSelect>>', onselect)
for item in ["one", "two", "three", "four"]:
    lb.insert(END, item)

mainloop()
