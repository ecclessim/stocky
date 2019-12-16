# Author : Eccles Sim
# Uses API provided by IEX and a scrape from earningswhispers
# Functions file
import tkinter as tk
import requests
import json
import os
from collections import OrderedDict
from tkinter import messagebox
from tkinter import ttk
from bs4 import BeautifulSoup, SoupStrainer

# Combobox widget
global oro_ddl
oro_ddl = None

stFont = ("calibri",12)
# Token is given to each unique IEX API registered user.
token = ""

q_url = "https://cloud.iexapis.com"
e_url = "https://earningswhispers.com"

def load_Quotes():
    global oro_ddl
    # Simple local storage through text file of saved quotes :^)
    if os.stat("wl.txt").st_size != 0:
        with open("wl.txt","r") as f:
            quotes = f.read().strip().split("\n")
        for i,q in enumerate(quotes):
            quotes[i] = q.upper()
        quoteVar = tk.StringVar()
        # Global declaration of this widget so that when it updates, the program can recognise that since this widget already exist, we will just update the values
        if oro_ddl == None:
            oro_ddl = ttk.Combobox(state='readonly',textvariable=quoteVar,values=quotes)
            oro_ddl.bind("<<ComboboxSelected>>",lambda x = i: getQuote(oro_ddl.get()))
            oro_ddl.grid(row=1,column=0,sticky='nsew',padx=3,pady=3)
        else:
            oro_ddl.config(values=quotes)

# For these functions, you see that there is the optional argument ent, this argument is used to clear the entry widget if declared.
def add_Quote(quote,ent=0):
    # I was thinking of adding a check to see if the quote entered is a valid quote (response 200), but i don't know if the additional processing is worth it :^)
    data = []
    if len(quote.strip())!= 0:
        with open("wl.txt","r+") as f:
            if quote in f.read().split("\n"):
                messagebox.showerror("Error",f"{quote} is already marked!")
                if ent != 0:
                    ent.delete(0,'end')
            else:
                f.write(f"{quote}\n")
                messagebox.showinfo("Success",f"{quote.upper()} marked!")
                if ent != 0:
                    ent.delete(0,'end')
        # Refreshes the values in the dropdown list (or combobox in tkinter)
        load_Quotes()
    else:
        messagebox.showerror("Error","Uh oh, its empty!")
        if ent != 0:
            ent.delete(0,'end')
def getEarnings(quote,ent=0):
    # Kinda hacky way of getting earning dates from a website without the use of API, might break apart if website code changes :^)
    if len(quote.strip()) != 0:
        with requests.Session() as f:
            response = f.get(f"{e_url}/stocks/{quote}",allow_redirects=False)
        if response.status_code == 200:
            strainer = SoupStrainer(id='datebox')
            soup = BeautifulSoup(response.content,'lxml',parse_only=strainer)
            result = str(soup.get_text(" ",strip=True))
            messagebox.showinfo(quote,f"Earnings date for {quote.upper()}\n\n{result}")
            if ent != 0:
                ent.delete(0,'end')
        else:
            messagebox.showerror("Error",f"Couldn't find {quote}")
            if ent != 0:
                ent.delete(0,'end')
    else:
        messagebox.showerror("Error","Uh oh, its empty!")
def getQuote(quote,ent=0):
    # com_lbl is the first label created once results are returned, so if this label is instantiated (not None), implies the subsequent widgets are as well.
    com_lbl = None
    # These list hold similar stuff, naming convention could be better :^)
    # widget_list holds the widgets with the values taken from the IEX API JSON values
    # fabList holds the widgets beside the values, like titles of the values??
    widget_list = []
    fabList = []
    if len(quote.strip())!= 0:
        with requests.Session() as f:
            response = f.get(f"{q_url}/stable/stock/{quote}/quote?token={token}")
        if response.status_code != 200:
            messagebox.showerror("Error",f"Couldn't find {quote}")
            if ent!= 0:
                ent.delete(0,'end')
        else:
            info = json.loads(response.text)
            o_Info = OrderedDict(info)
            company_name = str(o_Info['companyName'])
            price_close = float(o_Info['latestPrice'])
            price_close = "${0:,.2f}".format(price_close)
            prev_close = float(o_Info['previousClose'])
            prev_close = "${0:,.2f}".format(prev_close)
            dollar_change = float("{0:.2f}".format(o_Info['change']))
            percent_change = float("{0:.2f}".format(100 * o_Info['changePercent']))
            date = str(o_Info['latestTime'])
            if dollar_change > 0:
                color_Indi = "limegreen"
            else:
                color_Indi = "red"
            if com_lbl == None:
                lbl_tit = tk.Label(text="company:",font=stFont,anchor='w',bg='white')
                lbl_tit0 = tk.Label(text="price:",font=stFont,anchor='w',bg='white')
                lbl_tit2 = tk.Label(text="change:",font=stFont,anchor='w',bg='white')
                lbl_tit3 = tk.Label(text="change(%):",font=stFont,anchor='w',bg='white')
                lbl_tit4 = tk.Label(text="last updated:",font=stFont,anchor='w',bg='white')
                com_lbl = tk.Label(text=company_name,font=stFont,anchor='w',bg='white',width=30)
                pri_lbl = tk.Label(text=f"{prev_close} → {price_close}",fg=color_Indi,font=stFont,anchor='w',bg='white')
                doc_lbl = tk.Label(text=f"${dollar_change}",fg=color_Indi,font=stFont,anchor='w',bg='white')
                per_lbl = tk.Label(text=f"{percent_change}%",fg=color_Indi,font=stFont,anchor='w',bg='white')
                date_lbl = tk.Label(text=date,font=stFont,anchor='w',bg='white')
                widget_list.append(com_lbl)
                widget_list.append(pri_lbl)
                widget_list.append(doc_lbl)
                widget_list.append(per_lbl)
                widget_list.append(date_lbl)
                fabList.append(lbl_tit)
                fabList.append(lbl_tit0)
                fabList.append(lbl_tit2)
                fabList.append(lbl_tit3)
                fabList.append(lbl_tit4)
                for i,widget in enumerate(fabList):
                    widget.grid(row=i+1,column=1,sticky='nsew',padx=3,pady=3)
                for i,widget in enumerate(widget_list):
                    widget.grid(row=i+1,column=2,sticky='nsew')
                if ent != 0:
                    ent.delete(0,'end')
            else:
                com_lbl.update(text=company_name)
                pri_lbl.update(text=price_close,fg=color_Indi)
                doc_lbl.update(text=str(dollar_change),fg=color_Indi)
                per_lbl.update(text=str(percent_change),fg=color_Indi)
                date_lbl.update(text=date)
                if ent != 0:
                    ent.delete(0,'end')
    else:
        messagebox.showerror("Error","Uh oh, its empty!")