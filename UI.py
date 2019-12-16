# UI File
import tkinter as tk
import stocku as stocky
import webbrowser

if __name__ == "__main__":
    main = tk.Tk()
    main.title("IEX Quote")
    main.resizable(False,False)
    stFont = stocky.stFont

    q_lbl = tk.Label(text='stock quote',font=stFont,bg="white",width=5)
    q_ent = tk.Entry(font=stFont,borderwidth=0,width=50,bg="gray95")
    q_btn = tk.Button(text="quote",anchor='w',font=stFont,bg="white",borderwidth=0,width=10,command=lambda: stocky.getQuote(q_ent.get(),q_ent))
    e_btn = tk.Button(text="earnings",anchor='w',font=stFont,bg="white",borderwidth=0,width=10,command=lambda: stocky.getEarnings(q_ent.get(),q_ent))
    wl_btn = tk.Button(text="mark",anchor='w',font=stFont,bg="white",borderwidth=0,width=10,command=lambda: stocky.add_Quote(q_ent.get(),q_ent))
    ed_btn = tk.Button(text="edit",anchor='w',font=stFont,bg="white",borderwidth=0,width=10,command=lambda: webbrowser.open("wl.txt"))
    q_ent.bind('<Return>',lambda event = None: stocky.getQuote(q_ent.get(),q_ent))
    
    q_lbl.grid(row=0,column=0,sticky='nsew')
    q_ent.grid(row=0,columnspan=2,column=1,sticky='nsew',padx=3,pady=3)
    q_btn.grid(row=0,column=3,sticky='nsew',padx=3,pady=3)
    e_btn.grid(row=1,column=3,sticky='nsew',padx=3,pady=3)
    wl_btn.grid(row=2,column=3,sticky='nsew',padx=3,pady=3)
    ed_btn.grid(row=3,column=3,sticky='nsew',padx=3,pady=3)
    
    stocky.load_Quotes()
    q_ent.focus()
    
    width_Screen = main.winfo_screenwidth()
    height_Screen = main.winfo_screenheight()
    c_width = 624
    c_height = 224
    x = int((width_Screen//2)-(c_width//2))
    y = int((height_Screen//2)-(c_height//2))
    
    main.columnconfigure(0,weight=1)
    main.config(bg='white')
    main.geometry(f"{c_width}x{c_height}+{x}+{y}")
    main.mainloop()