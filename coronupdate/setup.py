''' this file will show the country data and state wise data
by using webscraping  '''
import sqlite3 as sqll
import requests
import datetime
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

APP = Flask(__name__)

@APP.route('/data', methods=['GET', 'POST'])
def data():
    ''' when user search by state name  '''
    try:
        response = requests.get("https://www.worldometers.info/coronavirus/")
    except requests.exceptions.RequestException:
        name = request.form.get('cname')
        if name.find(" ") >= 1:
            name = name[0:(name.find(" ")):].title()
        connection = sqll.connect("coronadatabase.db")
        pointer = connection.cursor()
        pointer.execute("select * from district where sname == '{}'".format(name.title()))
        data1 = pointer.fetchall()

        if len(data1) >= 1:
            pointer.execute("select * from district where sname == '{}'".format(name.title()))
            data1 = pointer.fetchall()
            data = connectionnotfund()
            connection.commit()
            dicc = {
                "wc":data[0]['total'], "wr":data[0]['totalrecovered'], 'wd':data[0]['totaldeath'],
                "d0":data1[0][0], "d1":data1[0][1], "d2":data1[0][2], "d3":data1[0][3],
                "d4":data1[0][4],
            }
            return render_template("CoronaUpdate.html", dicc=dicc, coronadata=data)
        connection.commit()
        data = connectionnotfund()
        dicc = {"wc":data[0]['total'], "wr":data[0]['totalrecovered'], 'wd':data[0]['totaldeath']}
        error = "enter valid state name "
        return render_template("CoronaUpdate.html", dicc=dicc, coronadata=data, error=error)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        var = [va.text for va in soup.find_all('div', attrs={'class':'maincounter-number'})]
        name = request.form.get('cname')
        if name.find(" ") >= 1:
            name = name[0:(name.find(" ")):].title()
        connection = sqll.connect("coronadatabase.db")
        pointer = connection.cursor()
        data = pointer.execute("select * from district where sname == '{}'".format(name.title()))
        data1 = pointer.fetchall()

        if len(data1) >= 1:
            pointer.execute("select * from district where sname == '{}'".format(name.title()))
            data1 = pointer.fetchall()
            pointer.execute("select * from corona3")
            india = pointer.fetchall()
            new = []
            for i in india[0:len(india):]:
                dic = {"NO":i[0], "country":i[1], "total":i[2], "newcase":i[3], "totaldeath":i[4],
                       "newdeath":i[5], "totalrecovered":i[6], "activecase":i[7], "serious":i[8],
                       "totcase1MP":i[9], "death1mp":i[10], "totaltest":i[11], "test1m_pop":i[12],
                       "population":i[13]}
                new.append(dic)
            connection.commit()
            dicc = {
                "wc":var[0], "wr":var[2], 'wd':var[1],
                "d0":data1[0][0], "d1":data1[0][1], "d2":data1[0][2], "d3":data1[0][3],
                "d4":data1[0][4],
            }
            return render_template("CoronaUpdate.html", dicc=dicc, coronadata=new)
        pointer.execute("select * from corona3")
        india = pointer.fetchall()
        dicc = {"wc":var[0], "wr":var[2], 'wd':var[1]}
        connection.commit()
        new = []
        for rows in india[0:len(india):]:
            dic = {"NO":rows[0], "country":rows[1], "total":rows[2],
                   "newcase":rows[3], "totaldeath":rows[4], "newdeath":rows[5],
                   "totalrecovered":rows[6], "activecase":rows[7], "serious":rows[8],
                   "totcase1MP":rows[9], "death1mp":rows[10], "totaltest":rows[11],
                   "test1m_pop":rows[12], "population":rows[13]}
            new.append(dic)
        error = "enter valid state name "
        return render_template("CoronaUpdate.html", dicc=dicc, coronadata=new, error=error)
def districtdata():
    ''' this function will show live state corona updates  '''
    list1 = []
    new = []
    data1 = requests.get('https://www.ndtv.com/coronavirus/india-covid-19-tracker')
    soup1 = BeautifulSoup(data1.text, 'lxml')
    table_rows = soup1.find_all('trow')
    for trow in table_rows:
        tcolumn = trow.find_all('tcolumn')
        row = [rows.text[0:rows.text.find(" ")]  for rows in tcolumn[0:]]
        row = [row[j][0:row[j].find('District')] if 'District' in row[j] else row[j] for j in range(len(row))]
        list1.append(row)
    for i in range(1, (len(list1)-1), 1):
        for  j in range(1, len(list1)-1):
            if int(list1[i][1]) >= int(list1[j][1]):
                list1[i], list1[j] = list1[j], list1[i]
    for i in list1[1::]:
        dic = {"state/name":i[0], "TotalCase":i[1], "Activecase":i[2],
               "Recoverd":i[3], "TotalDeath":i[4]}
        name = i[0]
        totcase = i[1]
        activecase = i[2]
        recovered = i[3]
        totaldeath = i[4]
        new.append(dic)
        connection = sqll.connect("coronadatabase.db")
        pointer = connection.cursor()
        pointer.execute("update  district set sname ='{}', totalcase='{}', activecase='{}', recovered='{}', totaldeath='{}' where sname ='{}'".format(name, totcase, activecase, recovered, totaldeath, name))
        connection.commit()
    return new
@APP.route('/', methods=['GET', 'POST'])
def cronalive():
    ''' this function will show live country corona updates '''
    list1 = []
    new = []
    try:
        data = requests.get("https://www.worldometers.info/coronavirus/")
    except requests.exceptions.RequestException:
        data1 = connectionnotfund()
        dicc = {"wc":data1[0]['total'], "wr":data1[0]['totalrecovered'], 'wd':data1[0]['totaldeath']}
        return render_template("CoronaUpdate.html", coronadata=data1, dicc=dicc)
    else:
        if data.status_code == 200:
            # district = districtdata()
            soup = BeautifulSoup(data.text, 'lxml')
            var = [va.text for va in soup.find_all('div', attrs={'class':'maincounter-number'})]
            table_rows = soup.find_all('tr')
            now = datetime.datetime.now()
            dtime = now.strftime('%Y/%m/%d')
            for trow in table_rows:
                tcolumn = trow.find_all('td')
                row = [i.text for i in tcolumn[0:15]]
                list1.append(row)
            for i in list1[8:215:]:
                dic = {"NO":i[0], "country":i[1], "total":i[2], "newcase":i[3],
                       "totaldeath":i[4], "newdeath":i[5], "totalrecovered":i[6], "activecase":i[8],
                       "serious":i[9], "totcase1MP":i[10], "death1mp":i[11], "totaltest":i[12],
                       "test1m_pop":i[13], "population":i[14]}
                new.append(dic)
                num1 = i[0]
                country = i[1]
                totalcase = i[2]
                newcase = i[3]
                totaldeath = i[4]
                newdeath = i[5]
                totalrecovered = i[6]
                activecase = i[8]
                serious = i[9]
                totcase1mp = i[10]
                death1mp = i[11]
                totaltest = i[12]
                test1m_pop = i[13]
                population = i[14]
                day = dtime
                if num1 == " ":
                    num1 = 0
                # connection = sqll.connect("coronadatabase.db")
                # pointer = connection.cursor()
                # num = num1
                # pointer.execute("update  corona3 set id='{}', country='{}', totalcase='{}', newcase='{}', totaldeath='{}', newdeath='{}', recoverdcase='{}', activecase='{}', criticalcase='{}', totcase1mp='{}', totdeath1Mp='{}', totaltest='{}', m1_poptest='{}', population='{}', day='{}' where id ='{}'".format(num1, country, totalcase, newcase, totaldeath, newdeath, totalrecovered, activecase, serious, totcase1mp, death1mp, totaltest, test1m_pop, population, day, num))
                dicc = {"wc":var[0], "wr":var[2], 'wd':var[1]}
                # connection.commit()
            return render_template("CoronaUpdate.html", coronadata=new, dicc=dicc)
def connectionnotfund():
    ''' when connection not fund then it will run  '''
    connection = sqll.connect("coronadatabase.db")
    pointer = connection.cursor()
    pointer.execute("select * from corona3")
    india = pointer.fetchall()
    new = []
    for i in india[0:len(india):]:
        dic = {"NO":i[0], "country":i[1], "total":i[2], "newcase":i[3],
               "totaldeath":i[4], "newdeath":i[5], "totalrecovered":i[6],
               "activecase":i[7], "serious":i[8], "totcase1MP":i[9], "death1mp":i[10],
               "totaltest":i[11], "test1m_pop":i[12], "population":i[13]}
        new.append(dic)
    connection.commit()
    return new
APP.run(debug=True)
