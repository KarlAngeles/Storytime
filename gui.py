import tkinter as tk
from tkintertable import TableCanvas
from tkinter import scrolledtext
from PIL import ImageTk, Image
import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
from helpers import desc, predict_set_dict

window = tk.Tk()
window.configure(background="#EFEFEF")
window.title("Storytime Compiler")

class StorytimeTable(TableCanvas):
    """ Override a function in the parent class """
    def __init__(self, parent=None, model=None, width=None, height=None, rows=1, cols=2, data=None, read_only=True, cellwidth=150, **kwargs):
        TableCanvas.__init__(self, parent, model, data, read_only,
                             width, height, cellwidth, background='#EFEFEF', thefont=('monospace', 10))

    def deleteRow(self):
        row = self.getSelectedRow()
        self.model.deleteRow(row)
        self.setSelectedRow(row-1)
        self.clearSelected()
        self.redrawTable()

data = {1: {'lexeme': '', 'token': '', 'description': ''}}

top = tk.Frame(window, height=50, width=50)
mid = tk.Frame(window, height=50, width=150, background="#EFEFEF")
table_frame = tk.Frame(mid, background="#EFEFEF")
table_frame.grid(column=1, row=0)
table = StorytimeTable(table_frame, data=data,
                       read_only=True, height=530, thefont=('monospace', 15))
table.show()
bot = tk.Frame(window, height=25, width=50, background="#EFEFEF")

top.grid(row=0)
top.grid_propagate(1)
mid.grid(row=1, pady=10, padx=10)
bot.grid(row=2, sticky="s", pady=30)
bot.grid_propagate(1)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

# make sure the image is in the same directory as the script
logo = Image.open("logo.png")
pic = ImageTk.PhotoImage(logo)
logo_label = tk.Label(top, image=pic, borderwidth=0, background="#EFEFEF")
logo_label.grid(row=0, column=0)

code = tk.scrolledtext.ScrolledText(
    mid, height=25, width=60, font=('monospace', 13))
code.grid(row=0, column=0)

output = tk.scrolledtext.ScrolledText(
    bot, state="disabled", height=10, width=70, font=('monospace', 10), borderwidth=0)
output.grid(row=0, column=0, padx=15)


def lex_show():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    data = code.get("1.0", tk.END)
    l = lex.lex(module=lexer)
    l.input(data)
    rows = len(table.model.data)
    if rows >= 1:
        for i in range(1, rows):
            table.deleteRow()
    toks = []
    previousToken = ''
    while True:
        try:
            tok = l.token()
            table_data = table.model.data
            if not tok:
                output.insert(tk.END, "No lexing error")
                return
            row = len(table_data)
            table_data[row]['lexeme'] = tok.value

            if (tok.type == 'SNUM' or tok.type == 'ID' or tok.type == 'STRING'):
                if (tok.type == 'STRING'):
                    table_data[row]['token'] = 'stringterm'
                else:
                    table_data[row]['token'] = tok.type.lower()
            else:
                table_data[row]['token'] = tok.value

            table_data[row]['description'] = desc[tok.type]
            table.addRow()
            listVal = lexer.delimDict[previousToken]

            if (tok.value in listVal):
                toks.pop()
                raise lexer.StorytimeLexingError(
                    'Lexical error: Invalid delimiter for "{}" token: [{} {} {} {}]'
                    .format(previousToken, tok.type, tok.value, tok.lineno, tok.lexpos))

            previousToken = tok.value
            toks.append(tok)
        except KeyError:
            previousToken = tok.value
            toks.append(tok)
        except lexer.StorytimeLexingError as lexing_error:
            output.configure(state="normal")
            output.insert(tk.END, "{}".format(lexing_error))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
            break

    output.configure(state="disabled")


last_token = None
second_last_token = None

def get_token():
    global last_token
    global second_last_token
    second_last_token = last_token
    last_token = lexer.lexer.token()
    print('first: ', last_token)
    print('second: ', second_last_token)
    return last_token

def parse_show():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    data = code.get("1.0", tk.END)
    try:
        p = yacc.yacc(module=parser)
        res = p.parse(data, tokenfunc=get_token, debug=0)
        output.configure(state="normal")
        output.insert(tk.END, "great success!")
        output.configure(state="disabled")
        return
    except parser.StorytimeParsingError as parsing_error:
        try:
            message = ' '.join(predict_set_dict[second_last_token.type])
            output.configure(state="normal")
            output.insert(tk.END, "Unexpected {} Expected {}".format(last_token.value, message))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
        except:
            output.configure(state="normal")
            output.insert(tk.END, "{}".format(parsing_error))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
    except lexer.StorytimeLexingError as lexing_error:
        output.configure(state="normal")
        output.insert(tk.END, "{}".format(lexing_error))
        output.insert(tk.END, "\nCannot proceed to parse")
        output.insert(tk.END, "\n")
        output.configure(state="disabled")

lex_button = tk.Button(
    bot,
    font=('monospace', 15),
    text="Tokenize",
    width=15,
    height=2,
    padx=10,
    command=lex_show
)
parse_button = tk.Button(
    bot,
    font=('monospace', 15),
    text="Parse",
    width=15,
    height=2,
    padx=10,
    command=parse_show
)

lex_button.grid(column=1, row=0)
parse_button.grid(column=2, row=0)
code.insert(tk.END, "# insert code here")
window.mainloop()
