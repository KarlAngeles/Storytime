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


top = tk.Frame(window, height=50, width=50)
mid = tk.Frame(window, height=50, width=150, background="#EFEFEF")
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

lexemes = tk.scrolledtext.ScrolledText(
        mid, height=25, width=25, font=('monospace', 13))
lexemes.grid(row=0, column=1)
tokens = tk.scrolledtext.ScrolledText(
        mid, height=25, width=25, font=('monospace', 13))
tokens.grid(row=0, column=2)

output = tk.scrolledtext.ScrolledText(
    bot, state="disabled", height=10, width=70, font=('monospace', 10), borderwidth=0)
output.grid(row=0, column=0, padx=15)


toks = []
errors = []

def lex_show():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    lexemes.delete("1.0", tk.END)
    tokens.delete("1.0", tk.END)
    data = code.get("1.0", tk.END)
    l = lex.lex(module=lexer)
    l.input(data)

    global toks
    global errors

    toks = []
    errors = []
    previousToken = ''
    lexemes.insert(tk.END, 'Lexemes\n')
    tokens.insert(tk.END, 'Tokens\n')

    while True:
        try:
            tok = l.token()
            if not tok:
                break

            try:
                if (previousToken.type in ['SNUM', 'STRING', 'ID']):
                    typeval = lexer.delimDict[previousToken.type]
                    if (tok.value in typeval or (tok.type == 'SNUM' and 'NUMBERS' in typeval)):
                        toks.pop()
                        errors.append('Lexical Error: invalid delimiter for "{}" token: [{} {} {} {}]'.format(previousToken, tok.type, tok.value, tok.lineno, tok.lexpos))

                # checks if current token is valid or invalid 
                elif (tok.value in lexer.delimDict[previousToken.value] or (tok.type == 'SNUM' and 'NUMBERS' in lexer.delimdict[previousToken.value])):
                    toks.pop()
                    errors.append('Lexical Error: invalid delimiter for "{}" token: [{} {} {} {}]'.format(previousToken, tok.type, tok.value, tok.lineno, tok.lexpos))

                previousToken = tok
                toks.append(tok)
            except:
                previousToken = tok
                toks.append(tok)

        except lexer.StorytimeLexingError as lexing_error:
            output.configure(state="normal")
            output.insert(tk.END, "{}".format(lexing_error))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
            return


    for idx, tok in enumerate(toks):
        lexemes.insert(tk.END, "\n" + tok.value)
        if (tok.type == 'SNUM' or tok.type == 'ID' or tok.type == 'STRING'):
            if (tok.type == 'STRING'):
                tokens.insert(tk.END, "\n" + 'stringterm')
            else:
                tokens.insert(tk.END, "\n" + tok.type.lower())
        else:
            tokens.insert(tk.END, "\n" + tok.value)

    for error in errors:
        output.configure(state="normal")
        output.insert(tk.END, error)
        output.insert(tk.END, "\n")
        output.configure(state="disabled")

    output.insert(tk.END, "No lexing error")
    output.configure(state="disabled")

# last_token = None
# second_last_token = None
# # After clicking lex, then parse, what happens is that the lexer finishes evaluation
# def get_token():
    # global last_token
    # global second_last_token
    # second_last_token = last_token
    # last_token = lexer.lexer.token()

    # print('second: ', second_last_token)
    # print('last: ', last_token)
    # return last_token

def parse_show():
    output.configure(state="normal")
    output.delete("1.0", tk.END)
    data = code.get("1.0", tk.END)
    l = lex.lex(module=lexer)
    l.input(data)

    try:
        if len(errors) != 0:
            for error in errors:
                output.configure(state="normal")
                output.insert(tk.END, error)
                output.insert(tk.END, "\n")
                output.configure(state="disabled")
                return

        p = yacc.yacc(module=parser)
        # p.parse(data, lexer=l, tokenfunc=get_token)
        p.parse(data, lexer=l)
        output.configure(state="normal")
        output.insert(tk.END, "great success!")
        output.configure(state="disabled")
        return
    except lexer.StorytimeLexingError as lexing_error:
        print('lexical error')
        output.configure(state="normal")
        output.insert(tk.END, "{}".format(lexing_error))
        output.insert(tk.END, "\n")
        output.configure(state="disabled")
        return
    except parser.StorytimeParsingError as parsing_error:
        if len(errors) != 0:
            for error in errors:
                output.configure(state="normal")
                output.insert(tk.END, error)
                output.insert(tk.END, "\n")
                output.configure(state="disabled")
                return
        try:
            for idx, tok in enumerate(toks):
                if (str(tok) == str(parsing_error)):
                    # print(toks)
                    # print(toks[idx-1])
                    message = ' '.join(predict_set_dict[toks[idx - 1].type]) # second last token type
                    output.configure(state="normal")
                    output.insert(tk.END, "Unexpected {} Expected {}".format(tok.value, message))
                    output.insert(tk.END, "\n")
                    output.configure(state="disabled")
                    return

            output.configure(state="normal")
            output.insert(tk.END, "Syntax Error: {}".format(parsing_error))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
            return
        except:
            output.configure(state="normal")
            output.insert(tk.END, "Syntax Error: {}".format(parsing_error))
            output.insert(tk.END, "\n")
            output.configure(state="disabled")
            return
    # except:
        # try:
            # maybe find matching token from tok list then second last token type is index before that
            # message = ' '.join(predict_set_dict[second_last_token.type])
            # output.configure(state="normal")
            # output.insert(tk.END, "Unexpected {} Expected {}".format(last_token.value, message))
            # output.insert(tk.END, "\n")
            # output.configure(state="disabled")
            # return
        # except parser.StorytimeParsingError as parsing_error:
            # output.configure(state="normal")
            # output.insert(tk.END, "{}".format(parsing_error))
            # output.insert(tk.END, "\n")
            # output.configure(state="disabled")
            # return

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
