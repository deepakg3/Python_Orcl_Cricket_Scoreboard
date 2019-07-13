import cx_Oracle
from random import randint
from collections import defaultdict
connection = cx_Oracle.connect('SYSTEM/gads2316')
cursor = connection.cursor()
cursor.execute('drop table team')
cursor.execute('drop table players')
cursor.execute('drop table batting')
def over(no):
    global team
    global teamstats
    global players
    global data
    global overs
    batting = team[no]
    notno = 0 if no ==1 else 1
    bowling = team[notno]
    st = players[no][int(input('Who is the striker?'))]
    nst = players[no][int(input('Who is the non striker?'))] 
    cursor.execute('update players set status = \'Not Out\' where team = \'{}\' and name = \'{}\''.format(batting,st))
    cursor.execute('update players set status = \'Not Out\' where team = \'{}\' and name = \'{}\''.format(batting,nst))
    cursor.execute('commit')
    for i in range(overs):
        bowler = players[notno][int(input('Who is going to bowl the current over'))]
        ball = 1
        while ball<8:
            if teamstats[batting]['target'] and teamstats[batting]['runs']>teamstats[batting]['target']:
                print('{} won by {} wickets'.format(batting,n-teamstats[batting]['wickets']))
                exit()
                return
            if ball == 7 :
                t = st
                st = nst
                nst = t
                break
            temp = input('BALL {}.{} {} to {}'.format(i,ball,bowler,st))
            if temp.isnumeric():
                data[batting][st]['runs'] += int(temp)
                cursor.execute('update players set runs = runs+{} where team=\'{}\' and name=\'{}\''.format(int(temp),batting,st))
                data[batting][st]['balls_faced'] += 1
                cursor.execute('update players set balls_faced = balls_faced+1 where team=\'{}\' and name = \'{}\''.format(batting,st))
                data[bowling][bowler]['balls_bowled'] += 1
                cursor.execute('update players set balls_bowled = balls_bowled+1 where team=\'{}\' and name = \'{}\''.format(bowling,bowler))
                teamstats[batting]['runs'] += int(temp)
                cursor.execute('update team set runs = runs+{} where name=\'{}\''.format(int(temp),batting))
                cursor.execute('commit')
                if int(temp)%2 != 0:
                    t = st
                    st = nst
                    nst =t
                else:
                    if int(temp) == 4:
                        data[batting][st]['fours'] += 1
                        cursor.execute('update players set fours = fours+1 where team=\'{}\' and name = \'{}\''.format(batting,st))
                    elif int(temp) == 6:
                        data[batting][st]['sixes'] += 1
                        cursor.execute('update players set sixes = sixes+1 where team=\'{}\' and name = \'{}\''.format(batting,st))
                        cursor.execute('commit')
                ball +=1
            else:
                if temp == 'wd' or temp == 'nb':
                    teamstats[batting]['runs'] += 1
                    cursor.execute('update team set runs = runs+1 where name=\'{}\''.format(batting))
                    data[bowling][bowler]['extras'] += 1
                    cursor.execute('update players set extras = extras+1 where team=\'{}\' and name = \'{}\''.format(bowling,bowler))
                    cursor.execute('commit')
                elif temp == 'W':
                    teamstats[batting]['wickets'] +=1
                    cursor.execute('update team set wickets = wickets+1 where name=\'{}\''.format(batting))
                    st,nst = wicket(st,nst,bowler,batting,bowling)
                    if teamstats[batting]['innings']:
                        return
def wicket(s,ns,b,batting,bowling):
    global team
    global n
    ch = int(input('\n1.bowled\n2.lbw\n3.caught\n4.Runout'))
    if ch == 1 or ch == 2:
        bl = 'b' if ch ==1 else 'lbw'
        print('{:>10}\n4s: {} 6s: {}\n{} {:>15}'.format(s,data[batting][s]['fours'],data[batting][s]['sixes'],bl,b))
        temp = '{} {}'.format(bl,b)
        cursor.execute('update players set status = \'{}\' where team = \'{}\' and name = \'{}\''.format(temp,batting,s))
        cursor.execute('update players set wickets = wickets+1 where team = \'{}\' and name = \'{}\''.format(bowling,b))
        cursor.execute('commit')
        s = ''
    elif ch == 3 :
        cby = players[team.index(bowling)][int(input('CAUGHT BY?'))]
        print('{:>10}\n4s: {} 6s: {}\nb {:>15} c {:<10}'.format(s,data[batting][s]['fours'],data[batting][s]['sixes'],b,cby))
        temp = 'b {} c {}'.format(b,cby)
        cursor.execute('update players set status = \'{}\' where team = \'{}\' and name = \'{}\''.format(temp,batting,s))
        cursor.execute('update players set wickets = wickets+1 where team = \'{}\' and name = \'{}\''.format(bowling,b))
        cursor.execute('commit')
        s = ''
    else:
        ch = int(input('1.{} or 2.{}'.format(s,ns)))
        rby = players[team.index(bowling)][int(input('Run out by?'))]
        if ch == 1:
            print('{:>10}\n4s: {} 6s: {}\n {:>15}  (Run Out)'.format(s,data[batting][s]['fours'],data[batting][s]['sixes'],rby))
            temp = '{}  (Run Out)'.format(rby)
            cursor.execute('update players set status = \'{}\' where team = \'{}\' and name = \'{}\''.format(temp,batting,s))
            cursor.execute('commit')
            s = ''
        else:
            print('{:>10}\n4s: {} 6s: {}\n {:>15}  (Run Out)'.format(s,data[batting][s]['fours'],data[batting][s]['sixes'],rby))
            temp = '{}  (Run Out)'.format(rby)
            cursor.execute('update players set status = \'{}\' where team = \'{}\' and name = \'{}\''.format(temp,batting,s))
            cursor.execute('commit')
            ns = ''
    if teamstats[batting]['wickets'] == n-2:
        innings(batting,bowling)
        return ('','')
    nb = players[team.index(batting)][int(input('Who is the new batsman in?'))]
    cursor.execute('update players set status = \'Not Out\' where team = \'{}\' and name = \'{}\''.format(batting,nb))
    if s:
        ns = nb
    else:
        s = nb
    return (s,ns)
def innings(batting,bowling):
    global overs
    global teamstats
    if teamstats[bowling]['innings'] and teamstats[batting]['wickets'] == n-2:
        print('{} won by {} runs'.format(bowling,teamstats[batting]['target']-teamstats[batting]['runs']))
        exit()
        return
    teamstats[batting]['innings'] = 1
    print('INNINGS OVER' )
    cursor.execute('update team set target = {}'.format(teamstats[batting]['runs']+1))
    teamstats[bowling]['target'] = teamstats[batting]['runs']+1
    print('{} needs to get {} runs from {} overs at {} per over'.format(bowling,teamstats[bowling]['target'],overs,teamstats[bowling]['target']/overs,))
    return
team = [input('Enter the team 1\'s name'),input('Enter the team 2\'s name')]
cursor.execute('create table team(name varchar2(20) primary key,runs number(3),wickets number(2), target number(3))')
cursor.execute('create table batting(team varchar2(20))')
teamstats = defaultdict(dict)
for each in team:
    teamstats[each] = defaultdict(int)
    cursor.execute('insert into team values(\'{}\',0,0,null)'.format(each))
    cursor.execute('commit')
n = int(input('Enter the number of players'))+1
print('Enter the squad of {} and {}'.format(team[0],team[1]))
players = [[input(str(_)) for _ in range(1,n)],[input(_) for _ in range(1,n)]]
players[0].insert(0,'')
players[1].insert(0,'')
overs = int(input('Enter the number of overs'))
toss = randint(0,1)
bat = toss
print('{} bats first'.format(team[bat]))
cursor.execute('insert into batting values(\'{}\')'.format(team[bat]))
data = defaultdict(dict)
vals = ['runs','balls_faced','fours','sixes','wickets','extras','balls_bowled']
cursor.execute('create table players(team varchar2(20),name varchar2(20),runs number(3),balls_faced number(3),status varchar2(20),fours number(3),sixes number(3),wickets number(2),extras number(3),balls_bowled number(3))')
for i in range(2):
    data[team[i]] = defaultdict(dict)
    for each in players[i][1::]:
        data[team[i]][each] = defaultdict(int)
        cursor.execute('insert into players values(\'{}\',\'{}\',0,0,null,0,0,0,0,0)'.format(team[i],each))
        cursor.execute('commit')
bowl = 0 if toss == 1 else 1
over(bat)
if not teamstats[team[bat]]['innings']:
    innings(team[bat],team[bowl])
cursor.execute('update batting set team=\'{}\''.format(team[bowl]))
over(bowl)
