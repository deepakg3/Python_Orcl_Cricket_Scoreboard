from tkinter import *
from tkinter import font
import cx_Oracle
connection = cx_Oracle.connect('SYSTEM/gads2316')
cursor = connection.cursor()
def refresh():
    cursor.execute('select team from batting')
    for line in cursor:
        bemp  = line[0]
    label.config(text = '{}'.format(bemp[0:3:]))
    cursor.execute('select runs,wickets from team where name=(select team from batting)')
    for each in cursor:
        score = each[0]
        wickets = each[1]
    label2.config(text = '{}-{}'.format(score,wickets))
    cursor.execute('select name,runs,balls_faced from players where team =(select team from batting) and status=\'Not Out\'')
    players = []
    for each in cursor:
        players.append(each)
    label3.config(text = '{} {}({})'.format(players[0][0],players[0][1],players[0][2]))
    try:
        label4.config(text = '{} {}({})'.format(players[1][0],players[1][1],players[1][2]))
    except:
        print('')
    
#helv36 = font.Font(family='Helvetica', size=36, weight='bold')
root = Tk()
root.configure(background = 'yellow')
root.geometry('750x600')
frame = Frame(root,bg = 'blue',height =120,bd=120)
l = Label(frame,text = 'CRICKET SCORE LIVE')
l.configure(font = ('Cooper Black','30'))
l.pack()
a = Frame(frame,height = 10,bd=20)
cursor.execute('select team from batting')
for line in cursor:
    temp  = line[0]
label =Label(a,text = 'TEAM',bg = 'yellow')
label.config(font = ('Cooper Black','30'))
label2 = Label(a,text ='0 - 0',bg = 'red')
label2.config(font = ('Cooper Black','30'))
b = Frame(frame,bg = 'red',height=20,bd=40)
label3 = Label(b,text ='Random Player 0(0)',bg = 'red')
label4 = Label(b,text ='Random Player 0(0)',bg = 'red')
label3.config(font = ('Cooper Black','30'))
label4.config(font = ('Cooper Black','30'))
button = Button(b,text = 'Refresh',command = refresh,bg = 'blue',fg = 'white')
frame.pack(side = TOP)
a.pack()
b.pack()
label.pack(side = LEFT)
label2.pack(side = LEFT)
label3.pack(side = BOTTOM)
label4.pack(side = BOTTOM)
button.pack(side = BOTTOM)
root.mainloop()
