import tkinter
import file_extractor
import os
import re
import lxml
import lxml.html
from lxml.html.clean import clean_html

def maingui(index,matrix,translator):
    m = tkinter.Tk()
    
    #m.geometry("{0}x{1}+0+0".format(m.winfo_screenwidth(), m.winfo_screenheight()))
    m.geometry("1000x500")
    m.title("ICS Search Engine")
    tkinter.Label(m, text='Enter Query').grid(row=0,column =0)
    e1 = tkinter.Entry(m, width=100)#where people enter their search

    def search(text):
        ranked = file_extractor.rank(e1.get().lower(),index,matrix)
        output = f"{len(ranked)} results found \n\n"
        #print(ranked)
        for posting in ranked[:20]:
            title, intro = get_info(posting)#gets the title of the result and a little bit of the page
            output += title.strip() +"\n"+translator[posting]+"\n"+intro+"\n\n\n"
        scroll = tkinter.Scrollbar(m)#creates the scrollbar
        scroll.grid(row = 1, column = 5, sticky = "ns")
        T = tkinter.Text(m,height = 30,width = 120, yscrollcommand = scroll.set, background="gray")
        T.grid(row = 1, column = 1, columnspan = 4)
        T.insert(tkinter.END,output)
        scroll.config(command=T.yview)
    m.bind("<Return>",search)#bind enter to searching
    e1.grid(row = 0, column = 1, columnspan = 4, sticky = "nesw") 
    m.mainloop() 

def get_info(file):
    with open(os.getcwd()+"/WEBPAGES_RAW/"+file,encoding = 'utf-8') as file:
        textcont = file.read()
        html = lxml.html.fromstring(textcont)#gets the title of the page and a little bit of the content
    title = ""
    for tag in html.xpath("//title"):
        title += tag.text_content()
        title += ""
#    body = html.xpath("//body").text_content()
    intro = " ".join([w for w in re.split(r"[^a-zA-Z0-9]",html.text_content()[:400]) if len(w) > 0])
    return (title, intro.lower())
