from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3 as sql
import math
import sys
import requests
from datetime import datetime
import time
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import os
import shutil




app = Flask(__name__)
'''
con = sql.connect("site.db")
con.row_factory = sql.Row

cur = con.cursor()
cur.execute('select * from v1 where "University of Divinity" <= "10"')
   
rows = cur.fetchall(); 

for i in rows:
    print(i[1])
'''
#app.config['GOOGLEMAPS_KEY'] = "AIzaSyBYkIz-pqehbEloeqad8C-JSvTgLruFdBg"
#GoogleMaps(app)
GoogleMaps(app, key="AIzaSyBYkIz-pqehbEloeqad8C-JSvTgLruFdBg")


@app.route("/",methods =["GET", "POST"])
@app.route("/search",methods =["GET", "POST"])
def mapview1():
    
    con = sql.connect("site.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    
    if request.method == "POST":
        list_sub = []
        suburb = request.form["suburb"]

        #show1='select "Suburb/Town Name",Postcode from v3 where "Suburb/Town Name" = "'+suburb+'"'
        show1='select "Suburb/Town Name",Postcode,"Median Rent","Number of Hospitals", "Number of Cinemas" from v3 where "Suburb/Town Name" like "%'+suburb+'%"'
        cur.execute(show1)
        rows = cur.fetchall(); 
        for i in rows:
            list_sub.append(i)

        
        return render_template('searchResult3.html',list_sub=list_sub)
        
    else:
        return render_template('home.html')







@app.route("/ad")
def abd():
    return render_template("searchOne.html")
@app.route("/rent")
def rent():
    return render_template("rent.html")


@app.route('/filter',methods =["GET", "POST"])
def your_view():
    
    your_list = []
    your_list5=[]
    con = sql.connect("site.db")
    con.row_factory = sql.Row
    cur = con.cursor()


    if request.method == "POST":
        counter = 0
        uni = request.form.get("uni")
        max_distance = request.form.get("max_distance")
        cinema = request.form.get("cinema")
        hospital = request.form.get("hospital")
        rent = request.form.get("rent")

        print(max_distance,flush=True)

        if cinema.lower() == 'yes':
            cinema = '>= 1'
        elif cinema.lower() == 'no':
            cinema = '<= 99'

        if hospital.lower() == 'yes':
            hospital = '>= 1'

        elif hospital.lower() == 'no':
            hospital = '<= 99'

        #based on user filter
        url = 'select * from v3 where "'+uni+'" <= ' + max_distance+' and "Number of Cinemas" '+cinema+' and "Number of Hospitals" '+hospital+' and "Median Rent" <= '+rent
        cur.execute(url)
        rows = cur.fetchall(); 
        for i in rows:
            counter += 1
            t = i[0]
            your_list.append(t)

        #based on all suburb
        url = 'select * from v3'
        cur.execute(url)
        rows = cur.fetchall(); 
        for i in rows:
            counter += 1
            t = i[0]
            your_list5.append(t)

        your_list3=[]
        your_list4=[]

        for k in range(2):
            for_temp=None

            if k ==0:
                for_temp = your_list
            else:
                for_temp = your_list5
                

            for i in range (len(for_temp)):
                wsm_rent = 'select "Median Rent" from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_rent)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_rent = j[0]

                wsm_numberhospital = 'select "Number of Hospitals" from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_numberhospital)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_numberhospital = j[0]

                wsm_numbercinemas = 'select "Number of Cinemas" from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_numbercinemas)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_numbercinemas = j[0]


                
                wsm_closesthospital = 'select "Closest Hospital" from suburb_distance_updated where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_closesthospital)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_closesthospital = j[0]


                wsm_closestcinema = 'select "Closest Cinema" from suburb_distance_updated where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_closestcinema)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_closestcinema = j[0]


                wsm_distancetocbd = 'select "Distance to CBD" from suburb_distance_updated where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_distancetocbd)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_distancetocbd = j[0]


                wsm_distancetouni = 'select "'+uni+'" from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_distancetouni)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_distancetouni = j[0]


                wsm_crime = 'select "Incidents Recorded" from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_crime)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_crime = j[0]

                wsm_population = 'select population from v3 where "Suburb/Town Name" = "'+for_temp[i]+'"'
                cur.execute(wsm_population)
                rows = cur.fetchall(); 
                for j in rows:
                    wsm_population = int(     str(j[0]).replace(",","")    )
                


                calculate = -1.3*float(wsm_distancetouni)-0.1*float(wsm_closestcinema)-0.1*float(wsm_closesthospital)-0.1*float(wsm_distancetocbd)-5*(int(wsm_crime)/int(wsm_population))-float(wsm_rent)/10
                #calculate = -0.7*float(wsm_distancetouni)-0.1*float(wsm_closestcinema)-0.1*float(wsm_closesthospital)-0.1*float(wsm_distancetocbd)-float(wsm_rent)/10
                if k == 0:
                    your_list3.append((round(100+calculate,2),for_temp[i],wsm_rent,round(wsm_closesthospital,2),round(wsm_closestcinema,2),wsm_numberhospital,wsm_numbercinemas,wsm_distancetouni))
                if k == 1:
                    your_list4.append((round(100+calculate,2),for_temp[i],wsm_rent,round(wsm_closesthospital,2),round(wsm_closestcinema,2),wsm_numberhospital,wsm_numbercinemas,wsm_distancetouni))









        if len(your_list3) >= 5:
            your_list3.sort(reverse=True)
            your_list = []
            for i in range(5):
                your_list.append(your_list3[i])
        else:

            user_len = len(your_list3)
            add_len = 5-len(your_list3)

            your_list4.sort(reverse=True)


            your_list3.sort(reverse=True)
            your_list = []
            for i in range(user_len):
                your_list.append(your_list3[i])

            j = 0
            while j < add_len:
                if your_list4[j] in your_list:
                    j+=1
                    add_len += 1
                else:
                    your_list.append(your_list4[j])
                    j += 1
        your_list10=[]

        
        for i in range(len(your_list)):
            your_list10.append(your_list[i][1])


        ##################################################################################################

        '''
        suburbs = your_list10

        import os
        if os.path.exists("templates/vhospital.html"):
            os.remove("templates/vhospital.html")
        if os.path.exists("templates/vcinema.html"):
            os.remove("templates/vcinema.html")
        if os.path.exists("templates/vdistancetoCBD.html"):
            os.remove("templates/vdistancetoCBD.html")
        if os.path.exists("templates/vrent.html"):
            os.remove("templates/vrent.html")
        if os.path.exists("templates/vcrime.html"):
            os.remove("templates/vcrime.html")



        import pandas as pd
        distance = pd.read_csv('closest_distance.csv')
        rentx = pd.read_csv('rent_one_bedroom.csv')
        rentx['Count']=rentx['Count'].str.replace(',','')

        
        #create df for visualisation
        selected_dist = pd.DataFrame()
        selected_rent = pd.DataFrame()

        for i in range(len(suburbs)):
            row1 = pd.DataFrame(distance.loc[distance['Suburb/Town Name']==suburbs[i],['Suburb/Town Name','Number of hospitals','Number of cinemas','Closest Hospital','Closest Cinema','Distance to CBD']])
            selected_dist = pd.concat([selected_dist,row1],verify_integrity=True)
            row2 = pd.DataFrame(rentx.loc[rentx['Suburb']==suburbs[i],['Suburb','Count','Median']])
            selected_rent = pd.concat([selected_rent,row2],verify_integrity=True)

        crime = pd.read_csv('Crime.csv')
        crime.columns =[column.replace(" ", "_") for column in crime.columns]
        crime['Incidents_Recorded'] = crime['Incidents_Recorded'].str.replace(',','')
        crime['Incidents_Recorded'] = pd.to_numeric(crime['Incidents_Recorded']) 

        fig = px.line(x=selected_dist['Suburb/Town Name'],y=selected_dist['Closest Hospital'],markers=True, labels={"x":"Suburb","y":"Shortest distance to hospital (km)"})

        fig.add_bar(x=selected_dist['Suburb/Town Name'],y=selected_dist['Number of hospitals']
                , name="hospitals")
        fig.update_layout(showlegend=False)
        fig.write_html("templates/vhospital.html",full_html=False,include_plotlyjs='cdn')    
        
        fig1 = px.line(x=selected_dist['Suburb/Town Name'],y=selected_dist['Closest Cinema'],
                        markers=True,
                    labels={"x":"Suburb","y":"Shortest distance to cinema (km)"})
        fig1.add_bar(x=selected_dist['Suburb/Town Name'],y=selected_dist['Number of cinemas'],
                    name="cinemas")
        fig1.update_layout(showlegend=False)
        fig1.write_html("templates/vcinema.html",full_html=False,include_plotlyjs='cdn')

            
        fig2 = px.bar(x=selected_dist['Distance to CBD'],y=selected_dist['Suburb/Town Name'], orientation="h",
                    labels={"x":"Distance to CBD (km)","y":"Suburb"})
        asdfgh=None
        fig2.write_html("templates/vdistancetoCBD.html",full_html=False,include_plotlyjs='cdn')


        selected_rent["Count"] = selected_rent["Count"].astype(str).replace(',','')
        selected_rent["Count"] = selected_rent["Count"].astype(float)
        fig3 = px.scatter(selected_rent,x="Suburb", y="Median",color="Count",custom_data=["Count"],
                        labels={"x":"Suburb","y":"Median rent ($)","color":"Number of properties"})
        fig3.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
        fig3.update_traces(mode="markers",hovertemplate="<br>".join([
                "Suburb: %{x}",
                "Median price: $%{y}",
                "Number of property: %{customdata[0]}"
            ])
        )
        fig3.write_html("templates/vrent.html",full_html=False, include_plotlyjs='cdn')

        dfg = crime.query('(Suburb in @suburbs) and (Year==2022)')
        dfg_1 = dfg.groupby('Suburb').count().reset_index()
        dfg_1 = dfg_1.rename(columns={"Year":"Number of crime recorded"})
        fig4 = px.bar(dfg_1,x="Number of crime recorded",y="Suburb", orientation="h",title='Number of crime in each suburb',
                    labels={"x":"Suburb","y":"Number of crime records"})
        fig4.write_html("templates/vcrime.html",full_html=False, include_plotlyjs='cdn')

        '''



        
        ##################################################################################################

        import os
        import shutil


        if hospital=='>= 1':
            hospital = 'include'
        else:
            hospital='exclude'
        if cinema == '>= 1':
            cinema = 'include'
        else:
            cinema = 'exclude'
        print(your_list,flush=True)
        return render_template('searchResult.html', your_list3=your_list,uni=uni, max_distance=max_distance, cinema = cinema, hospital=hospital, rent=rent)


    list_of_uni=[]
    con = sql.connect("site.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    url_uni = 'select University from uni_loc'
    cur.execute(url_uni)
    rows = cur.fetchall(); 
    for j in rows:
        list_of_uni.append(j[0])


    return render_template("perference.html",list_of_uni=list_of_uni)






@app.route("/search_all",methods =["GET", "POST"])
def mapview2():
    con = sql.connect("site.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    list_sub = []
    list_sub2 = []
    region_list = []
    
    
    show1='select Suburb, Region from rent_updated'
    region = "All Region"
    cur.execute(show1)
    rows = cur.fetchall(); 
    for i in rows:
        list_sub.append(i[0])

    #making a list into list of list 5 each
    temp_list, temp_list2 = [],[]
    for i in range(len(list_sub)):
        temp_list.append(list_sub[i])
        if len(temp_list) == 5 or i == len(list_sub)-1:
            temp_list2.append(temp_list)
            temp_list =[]     
    list_sub = temp_list2   



    reg='select distinct Region from rent_updated'
    cur.execute(reg)
    rows = cur.fetchall(); 
    for i in rows:
        region_list.append(i[0])

    
    if request.method == "POST":
        region = request.form.get("region")

        if region == "Select":
            list_sub2=[]
        else:
            if region == "All Region":
                show1='select Suburb, Region from rent_updated'
            else:
                show1='select Suburb, Region from rent_updated where Region = "'+region+'" '
            cur.execute(show1)
            rows = cur.fetchall(); 
            for i in rows:
                list_sub2.append(i[0])
                list_sub2.sort()

            #making a list into list of list 5 each
            temp_list, temp_list2 = [],[]
            for i in range(len(list_sub2)):
                temp_list.append(list_sub2[i])
                if len(temp_list) == 5 or i == len(list_sub2)-1:
                    temp_list2.append(temp_list)
                    temp_list =[]     
            list_sub2 = temp_list2           


        return render_template('searchResult2.html',list_sub=list_sub2,region_list=region_list,region=region)


        
    return render_template('searchResult2.html',list_sub=list_sub,region_list=region_list,region=region)


@app.route("/<suburb>",methods =["GET", "POST"])
def mapview(suburb):
    your_list = []
    your_list2 = []
    list_of_uni = []
    stop_list=[]
    suburb_coor = None
    dist_to_cbd = None
    dist_to_closest_hospital = None
    dist_to_closest_cinema = None
    dur3 = ""
    dist3= None
    arr3= None
    dep3 = None
    check_exist = None
    change_count = None
    con = sql.connect("site.db")
    con.row_factory = sql.Row
    cur = con.cursor()




    generator = []
    qwer = 'select "Suburb/Town Name" from v3'
    cur.execute(qwer)
    rows = cur.fetchall(); 
    for i in rows:
        generator.append(i[0])

    





    ################################################

    '''

    crime = pd.read_csv('Crime.csv')
    crime.columns =[column.replace(" ", "_") for column in crime.columns]
    crime['Incidents_Recorded'] = crime['Incidents_Recorded'].str.replace(',','')
    crime['Incidents_Recorded'] = pd.to_numeric(crime['Incidents_Recorded']) 


    chosen = suburb

    #crime.columns.tolist()
    dfg_chosen = pd.DataFrame(crime.loc[crime['Suburb']==chosen,crime.columns.tolist()]).reset_index(drop=True)
    dfg_chosen = dfg_chosen[dfg_chosen['Year']==2022]
    fig10 = px.sunburst(dfg_chosen, path=['Offence_Division', 'Offence_Subdivision', 'Offence_Subgroup'],values='Incidents_Recorded')

    fig10.update_layout(margin=dict(l=20, r=20,  b=20))
    fig10.update_traces(hovertemplate='Offence division: %{id} <br>Offence Subdivision: %{parent} <br>Offence Subgroup: %{label} <br>No of incidents: %{value}')
    fig10.update_layout(
        title="Incidents based on Offence Type in 2022",
        legend_title="Legend Title",
        font=dict(size=15)
    )
    
    fig10.write_html("templates/vcrime_3.html",full_html=False, include_plotlyjs='cdn')


    #line chart
    crime_1 = crime.query("Suburb == \'"+suburb+"\'")
    crime_11 = crime_1.groupby(['Year'])['Incidents_Recorded'].sum().reset_index()

    fig8 = go.Figure()
    fig8.add_trace(
        go.Scatter(x=crime_11.Year, y=crime_11.Incidents_Recorded))

    fig8.update_layout(
        xaxis=dict(rangeselector=dict(buttons=list([
                    dict(count=1,label="1y",step="year",stepmode="backward"),
                    dict(count=6,label="6y",step="year",stepmode="backward"),
                    dict(count=1,label="Now",step="year",stepmode="todate"),
                    dict(count=10,label="10y",step="year",stepmode="backward"),
                    dict(step="all")
                ])),rangeslider=dict(visible=True),type="date"))

    fig8.update_traces(hovertemplate="<br>".join(["Year: %{x}","Number of crime recorded: %{y}"]))
    fig8.update_layout(
        title="Total Incidents by Year",
        legend_title="Legend Title",
        font=dict(size=15)
    )
    fig8.write_html("templates/vcrime_1.html",full_html=False, include_plotlyjs='cdn')




    #y values being too big, not too sure how to minimise them down!
    crime_2 = crime_1.groupby(['Year','Offence_Division'])['Incidents_Recorded'].sum().reset_index()
    fig8_1= px.bar(crime_2,x="Year",y="Incidents_Recorded",color="Offence_Division",
                labels={"x":"Year","y":"Number of incidents records",
            "Offence_Division": "Offence division"})
    fig8_1.update_traces(hovertemplate="<br>".join([
            "Year: %{x}",
            "Number of crime records: %{y}"
        ])
    )
    fig8_1.write_html("templates/vcrime_2.html",full_html=False, include_plotlyjs='cdn')
    '''
    ##################################################
    
    '''
    crime = pd.read_csv('Crime.csv')
    crime.columns =[column.replace(" ", "_") for column in crime.columns]
    crime['Incidents_Recorded'] = crime['Incidents_Recorded'].str.replace(',','')
    crime['Incidents_Recorded'] = pd.to_numeric(crime['Incidents_Recorded']) 
    #Sunburs chart
    for i in range(len(generator)):
        chosen = generator[i]
        chosen1 = generator[i].replace(" ","_")

        #crime.columns.tolist()
        dfg_chosen = pd.DataFrame(crime.loc[crime['Suburb']==chosen,crime.columns.tolist()]).reset_index(drop=True)
        dfg_chosen = dfg_chosen[dfg_chosen['Year']==2022]
        fig10 = px.sunburst(dfg_chosen, path=['Offence_Division', 'Offence_Subdivision', 'Offence_Subgroup'],values='Incidents_Recorded')

        fig10.update_layout(margin=dict(l=20, r=20,  b=20))
        fig10.update_traces(hovertemplate='Offence division: %{id} <br>Offence Subdivision: %{parent} <br>Offence Subgroup: %{label} <br>No of incidents: %{value}')
        fig10.update_layout(
            title="Incidents based on Offence Type in 2022",
            legend_title="Legend Title",
            font=dict(size=15)
        )
        fig10.write_html("templates/vizu/"+chosen1+"_vcrime_3.html",full_html=False, include_plotlyjs='cdn')


        #line chart
        crime_1 = crime.query("Suburb == \'"+suburb+"\'")
        crime_11 = crime_1.groupby(['Year'])['Incidents_Recorded'].sum().reset_index()

        fig8 = go.Figure()
        fig8.add_trace(
            go.Scatter(x=crime_11.Year, y=crime_11.Incidents_Recorded))

        fig8.update_layout(
            xaxis=dict(rangeselector=dict(buttons=list([
                        dict(count=1,label="1y",step="year",stepmode="backward"),
                        dict(count=6,label="6y",step="year",stepmode="backward"),
                        dict(count=1,label="Now",step="year",stepmode="todate"),
                        dict(count=10,label="10y",step="year",stepmode="backward"),
                        dict(step="all")
                    ])),rangeslider=dict(visible=True),type="date"))

        fig8.update_traces(hovertemplate="<br>".join(["Year: %{x}","Number of crime recorded: %{y}"]))
        fig8.update_layout(
            title="Total Incidents by Year",
            legend_title="Legend Title",
            font=dict(size=15)
        )
        fig8.write_html("templates/vizu/"+chosen1+"_vcrime_1.html",full_html=False, include_plotlyjs='cdn')




        #y values being too big, not too sure how to minimise them down!
        crime_2 = crime_1.groupby(['Year','Offence_Division'])['Incidents_Recorded'].sum().reset_index()
        fig8_1= px.bar(crime_2,x="Year",y="Incidents_Recorded",color="Offence_Division",
                    labels={"x":"Year","y":"Number of incidents records",
                "Offence_Division": "Offence division"})
        fig8_1.update_traces(hovertemplate="<br>".join([
                "Year: %{x}",
                "Number of crime records: %{y}"
            ])
        )
        fig8_1.update_layout(
            title="Annual Incidents based on Offence Division from 2013",
            legend_title="Legend Title",
            font=dict(size=15)
        )
        fig8_1.write_html("templates/vizu/"+chosen1+"_vcrime_2.html",full_html=False, include_plotlyjs='cdn')

    '''
        
    ###################################################








    #Checking if suburb exists
    checker = 'select "Suburb/Town Name" from v3 where "Suburb/Town Name" = "'+suburb+'"'
    cur.execute(checker)
    rows = cur.fetchall(); 
    for i in rows:
        check_exist = i
    if check_exist == None:
        return render_template('notavailable.html')


    show = 'select "Median Rent","Incidents Recorded", Postcode, population, "Number of Hospitals","Number of Cinemas" from v3 where "Suburb/Town Name" = "'+suburb+'"'
    cur.execute(show)
    rows = cur.fetchall(); 
    for j in rows:
        show = [j[0],math.ceil(j[1]/9),j[2],j[3],j[4],j[5]]
  
    url_uni = 'select University from uni_loc'
    cur.execute(url_uni)
    rows = cur.fetchall(); 
    for j in rows:
        list_of_uni.append(j[0])


    url_cinema = 'select lat, long, name, rating, user_ratings_total, Suburb from cinema where Suburb = "'+suburb+'"'
    cur.execute(url_cinema)
    rows = cur.fetchall(); 
    for i in rows:
        t = (i[0],i[1],i[2])
        your_list.append(t)
    
    url_suburb = 'select lat,lng from v1 where "Suburb/Town Name" =  "'+suburb+'"'
    cur.execute(url_suburb)
    rows = cur.fetchall(); 
    for i in rows:
        suburb_coor = (i[0],i[1])

    url_hospital = 'select "Formal Name", Suburb, lat, lng from hospital where Suburb = "'+suburb+'"'
    cur.execute(url_hospital)
    rows = cur.fetchall(); 
    for i in rows:
        t = (i[0],i[1],i[2],i[3])
        your_list2.append(t)

    url_distance = 'select "Distance to CBD","Closest Hospital","Closest Cinema" from suburb_distance_updated where "Suburb/Town Name" = "'+suburb+'"'
    cur.execute(url_distance)
    rows = cur.fetchall(); 
    for i in rows:
        dist_to_cbd = math.ceil(float(i[0]))
        dist_to_closest_cinema = round(i[2],2)
        dist_to_closest_hospital = round(i[1],2)

    currtime = datetime.now().strftime("%Y-%m-%dT%H:%M")

    latlng = 'select lat,lng from v3 where "Suburb/Town Name" = "'+suburb+'"'
    cur.execute(latlng)
    rows = cur.fetchall(); 
    for j in rows:
        latlng = [str(j[0]),str(j[1])]


    restaurant_list=[]
    url33="https://maps.googleapis.com/maps/api/place/nearbysearch/json?keyword=restaurant&location="+latlng[0]+"%2C"+latlng[1]+"&radius=1500&type=restaurant&key=AIzaSyBYkIz-pqehbEloeqad8C-JSvTgLruFdBg"
    url33 = requests.get(url33).json()
    for i in range(len(url33['results'])):
        restaurant_list.append([
            url33['results'][i]['geometry']['location']['lat'],
            url33['results'][i]['geometry']['location']['lng']
            ]
            )




    if request.method == "POST":
        uni = request.form["uni"]
        dest_uni = uni
        departuretime = request.form['departuretime']
        departuretime = departuretime.replace('T','-')
        departuretime = departuretime.replace(':','-')
        departuretime = departuretime.split('-')
        departuretime = datetime(int(departuretime[0]),int(departuretime[1]),int(departuretime[2]),int(departuretime[3]),int(departuretime[4])).timestamp()
        departuretime = str(int(departuretime))


        uni = uni.replace(' ','%20')



        ######## JOURNEY PLANNER
        url = "https://maps.googleapis.com/maps/api/directions/json?origin="+suburb+"%2CVIC&destination="+uni+"&mode=transit&departure_time="+departuretime+"&key=AIzaSyBYkIz-pqehbEloeqad8C-JSvTgLruFdBg"
        dist3 = requests.get(url).json()
        
        
        dur3_value = dist3['routes'][0]['legs'][0]['duration']['value']
        
        try:
            dep3 = dist3['routes'][0]['legs'][0]['departure_time']['text']
            arr3 = dist3['routes'][0]['legs'][0]['arrival_time']['text']
        except KeyError:
            dep3 = int(departuretime)

            arr3 = dep3+int(dur3_value)


            dep3 = time.strftime('%H:%M', time.localtime(dep3))
            dep3 = str(datetime.strptime(dep3, '%H:%M').strftime("%#I:%M%p").replace('AM', 'am').replace('PM', 'pm'))
            arr3 = time.strftime('%H:%M', time.localtime(arr3))
            arr3 = str(datetime.strptime(arr3, '%H:%M').strftime("%#I:%M%p").replace('AM', 'am').replace('PM', 'pm'))


        dur3 = dist3['routes'][0]['legs'][0]['duration']['text']
        dist3 = dist3['routes'][0]['legs'][0]['distance']['text']
        
        response = requests.get(url).json()
        response = response['routes'][0]['legs'][0]['steps']
        change_count = -1
        
        temp2=None
        for i in range(len(response)):
            try:
                temp = response[i]['transit_details']['line']['vehicle']['type']
                if temp == "BUS" or temp =="TRAM":
                    temp2 = temp+' ( '+response[i]['transit_details']['line']['name']+' ('+ response[i]['transit_details']['line']['short_name'] +')'+  '), '+ response[i]['distance']['text']+', '+response[i]['duration']['text']+', from ('+response[i]['transit_details']['departure_stop']['name']+') to ('+response[i]['transit_details']['arrival_stop']['name']+')'
                else:
            
                    temp2 = response[i]['html_instructions']+', '+response[i]['distance']['text']+', '+response[i]['duration']['text']+', '+'from '+response[i]['transit_details']['departure_stop']['name']+' to '+response[i]['transit_details']['arrival_stop']['name']
            
                change_count += 1
            except KeyError:
                temp2 = response[i]['html_instructions'],response[i]['distance']['text'],response[i]['duration']['text']
        
            stop_list.append(temp2)
        if change_count == -1:
            change_count = 0







        suburb_underline = suburb.replace(' ','_')

        return render_template('searchOne.html', suburb_underline=suburb_underline,dest_uni=dest_uni,dist_to_closest_cinema=dist_to_closest_cinema,dist_to_closest_hospital=dist_to_closest_hospital,list_of_uni=list_of_uni,restaurant_list=restaurant_list,change_count=change_count,dep3=dep3,arr3=arr3,departuretime=departuretime,currtime = currtime, show=show, your_list=your_list, dur3=dur3, suburb_coor=suburb_coor, your_list2=your_list2, dist_to_cbd=dist_to_cbd,dist3=dist3,suburb=suburb,stop_list=stop_list)

    else:
        suburb_underline = suburb.replace(' ','_')


        


        return render_template('searchOne.html', suburb_underline=suburb_underline,dist_to_closest_cinema=dist_to_closest_cinema,dist_to_closest_hospital=dist_to_closest_hospital,list_of_uni=list_of_uni,restaurant_list=restaurant_list,currtime=currtime,show=show, your_list=your_list, dur3 = dur3,suburb_coor=suburb_coor, your_list2=your_list2, dist_to_cbd=dist_to_cbd,suburb=suburb,stop_list=stop_list)




'''
    cur.execute('select * from v1 where "University of Divinity" <= "10"')
    rows = cur.fetchall(); 
    for i in rows:
        your_list.append(i[1])

    return render_template('v2.html', your_list=your_list)
 '''   

'''
@app.route("/myproject/templates/vcinema.html")
def vcinemaplot():
    return render_template("vcinema.html",data='x')
@app.route("/myproject/templates/vcrime.html")
def vcrimeplot():
    return render_template("vcrime.html",data='x')
@app.route("/myproject/templates/vrent.html")
def vrentplot():
    return render_template("vrent.html",data='x')
@app.route("/myproject/templates/vhospital.html")
def vhospitalplot():
    return render_template("vhospital.html",data='x')
@app.route("/myproject/templates/vdistancetoCBD.html")
def vdistanceplot():
    return render_template("vdistancetoCBD.html",data='x')
'''
@app.route("/myproject/templates/vizu/<suburb>_vcrime_1.html")
def vcrime1plot(suburb):
    return render_template("vizu/"+suburb+"_vcrime_1.html",data='x')


@app.route("/myproject/templates/vizu/<suburb>_vcrime_2.html")
def vcrime2plot(suburb):
    return render_template("vizu/"+suburb+"_vcrime_2.html",data='x')


@app.route("/myproject/templates/vizu/<suburb>_vcrime_3.html")
def vcrime3plot(suburb):
    return render_template("vizu/"+suburb+"_vcrime_3.html",data='x')

@app.route("/myproject/templates/rent_vic.html")
def rent_all():
    return render_template("rent_vic.html")
if __name__ == '__main__':
   #app.run(debug = True)
   def generate_html(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table")
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                // paging: false,    
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html
   
   