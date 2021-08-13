from flask import Flask, render_template, request ,  url_for 
import requests, bs4, json
import pickle

app = Flask(__name__)

# open a file , where you stored model data ; load model ; close file

file = open('coronamodel.pkl','rb')
lr = pickle.load(file)
file.close()

# for fetching case recover death values
def get_data(url):
    data=requests.get(url)
    return data

def get_covid_data():
    url= 'https://www.worldometers.info/coronavirus/'
    dataFetch = get_data(url)

    bs = bs4.BeautifulSoup(dataFetch.text,'html.parser')
    worldCount = bs.findAll('span')[4:7]    
    a=[]
    for d in worldCount:
        a.append(d.text)
    return a

def namePop():
    url = 'https://www.worldometers.info/coronavirus/#countries'
    r=get_data(url)

    bs = bs4.BeautifulSoup(r.text,'html.parser' )
    table1 = bs.findAll('table')[0]
    
    links_with_text = []
    for a in table1.find_all('a', href=True): 
        if a.contents[0]: 
            links_with_text.append(a.contents[0])

    links_with_text.remove('Hungary')
    links_with_text.remove('New Zealand')
    links_with_text.remove('Bosnia and Herzegovina')

    data=[]
    for i in links_with_text:
        data.append(i)

    data.pop()

    # print(data)

    sno=[]
    country=[]
    population=[]
    no=1
    for i in range(int(len(data)/2)):
        sno.append(no)
        no+=1

        country.append(data.pop(0))
        population.append(data.pop(0))

    # for checking purpose
    # c=zip(sno,country,population)
    # for x,y,z in c:
    #     print(x,' = ',y,':',z)
    return sno,country,population

def continentDetails():
    url = 'https://www.worldometers.info/coronavirus/#countries'
    r=get_data(url)
    bs = bs4.BeautifulSoup(r.text,'html.parser' )
    table = bs.findAll('table')[0]

    d=table.find_all('td')
    data=[]
        
    for a in d:  
        data.append(a.text)

    data = " ".join(data)
    data.replace('\n','')
    data=data.replace('North','North-America')
    data=data.replace('South','South-America')
    data=data.split()

    for i in data:
        if i=='America':
            data.remove('America')

    no=0
    custom=[]
    for i in range(59):
        no+=1
        if no%10==0:
            continue
        custom.append(data[i])

    continent=[]
    tcases=[]
    ncases=[]
    tdeath=[]
    ndeath=[]
    trecover=[]
    nrecover=[]
    acases=[]
    scritical=[]

    i=0
    while i<len(custom):
        continent.append(custom[i])
        i+=1
        tcases.append(custom[i])
        i+=1
        ncases.append(custom[i])
        i+=1
        tdeath.append(custom[i])
        i+=1
        ndeath.append(custom[i])
        i+=1
        trecover.append(custom[i])
        i+=1
        nrecover.append(custom[i])
        i+=1
        acases.append(custom[i])
        i+=1
        scritical.append(custom[i])
        i+=1

    
    scritical[4]='0'
    scritical[5]=acases[5]
    acases[5]=nrecover[5]
    nrecover[5]=trecover[5]
    trecover[5]=ndeath[5]
    ndeath[5]=tdeath[5]
    tdeath[5]=ncases[5]
    ncases[5]=tcases[5]
    tcases[5]=continent[5]
    continent[5]='Australia/Oceania'


    # for checking purpose 
    # for i in range(len(continent)):
    #     print(continent[i]+' '+tcases[i]+' '+ncases[i]+' '+tdeath[i]+' '+ndeath[i]+' '+trecover[i]+' '+nrecover[i]+' '+acases[i]+' '+scritical[i])

    return continent,tcases,ncases,tdeath,ndeath,trecover,nrecover,acases,scritical

def crct(X):
    X=X.replace('-',' ')
    return X

def countryDetail():
    url='https://api.apify.com/v2/key-value-stores/tVaYRsPHLjNdNBu7S/records/LATEST?disableRedirect=true'
    r=requests.get(url)

    a=json.loads(r.text)
    di={}
    di['vl']=a

    finalData=[]
    for a in di:
        for i in di[a]:
            no=1
            egData=[]
            for key,val in i.items():
                if no<=5:
                    egData.append(val)
                print(no,' ',key,'= ',val)
                no+=1

            finalData.append(egData)
    no=1
    for a in finalData:
        a.insert(0,a.pop())

    # for checking purpose
    # for a in finalData:
    #     print(no,'= ',a,'\n')
    #     no+=1

    return finalData


def indiaDetail():
    url = 'https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true'
    r=requests.get(url)

    # overall detail of india
    tcases2 = r.json()['totalCases']
    acase2 = r.json()["activeCases"] 
    nacase2 = r.json()['activeCasesNew']
    death2 = r.json()['deaths']
    ndeath2 = r.json()["deathsNew"]
    lastUpdatedAtApify2 = r.json()['lastUpdatedAtApify']
    previousDayTests2 = r.json()["previousDayTests"]
    recovered2 = r.json()["recovered"]
    nRecovered2 = r.json()["recoveredNew"]

    lastUpdatedAtApify2=lastUpdatedAtApify2.replace('T',' ')
    lastUpdatedAtApify2=lastUpdatedAtApify2[0:19]

    # detail of every state in india
    ans=r.json()['regionData']
    region1=[]
    acase1 =[]
    deceased1=[]
    newDeceased1=[]
    newRecovered1=[]
    recovered1=[]
    totalInfected1=[]
    for a in ans:
        region1.append(a['region'])
        acase1.append( a['activeCases'])
        deceased1.append( a['deceased'])
        newDeceased1.append( a['newDeceased'])
        newRecovered1.append( a['newRecovered'])
        recovered1.append( a['recovered'])
        totalInfected1.append( a['totalInfected'])

    # for checking purpose
    # print(len(region1))
    # print(len(acase1))
    # print(len(deceased1))
    # print(len(newDeceased1))
    # print(len(newRecovered1))
    # print(len(recovered1))
    # print(len(totalInfected1))

    return (region1,acase1,deceased1,newDeceased1,newRecovered1,recovered1,totalInfected1,
    tcases2,acase2 ,nacase2 ,death2 ,ndeath2 ,lastUpdatedAtApify2 ,previousDayTests2 ,recovered2 ,nRecovered2) 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/covidDetect', methods=["GET","POST"])
def covidDetect():
    if request.method == "POST":
        myDict = request.form
        print(myDict)

        fever = float(myDict['fever'])
        age = int(myDict['age'])
        bodyPain = int(myDict['pain'])
        runnyNose = int(myDict['runnyNose'])
        diffBreath = int(myDict['diffBreath'])
        # print(fever)
        # Code for inference
        givenFeatures=[[fever,bodyPain,age,runnyNose,diffBreath]]
        infProb1=lr.predict_proba(givenFeatures)
        ans=infProb1[0][1]
        print("No yes event Prob : ",infProb1)
        print("YEs Prob : " , ans)
        
        # yes or no 
        # infProb=lr.predict_proba(givenFeatures)[0][1]
        return render_template('show.html',inf=round(ans*100))
    return render_template('index.html')


@app.route('/globalAffect')
def globalAffect():
    worldCount = get_covid_data() 
    case = worldCount[0]
    recover = worldCount[2] 
    death = worldCount[1]
    print (case,recover,death) 
    return render_template('tracker.html',case=case,recover=recover,death=death)


@app.route('/overallDetails')
def overallDetails():
    continent,tcases,ncases,tdeath,ndeath,trecover,nrecover,acases,scritical=continentDetails()
    a,b,c=namePop()
    
    region1,acase1,deceased1,newDeceased1,newRecovered1,recovered1,totalInfected1,tcases2,acase2,nacase2 ,death2 ,ndeath2 ,lastUpdatedAtApify2 ,previousDayTests2 ,recovered2 ,nRecovered2=indiaDetail()
    
    continent=list(map(crct,continent))
    
    finalData=countryDetail()
    # print(finalData)

    return render_template('casesWorld.html',a=a,b=b,c=c,len=len(a)
    ,continent=continent,tcases=tcases,ncases=ncases,tdeath=tdeath,ndeath=ndeath,trecover=trecover,nrecover=nrecover,acases=acases,scritical=scritical
    ,len1=len(continent)
    ,finalData=finalData,len3=len(finalData)
    )

@app.route('/about')
def about():
    return render_template('aboutUs.html')


@app.route('/indiaReport')
def indiaReport():
    
    region1,acase1,deceased1,newDeceased1,newRecovered1,recovered1,totalInfected1,tcases2,acase2,nacase2 ,death2 ,ndeath2 ,lastUpdatedAtApify2 ,previousDayTests2 ,recovered2 ,nRecovered2=indiaDetail()

    return render_template('india.html'
    ,tcase2=tcases2,acase2=acase2,nacase2=nacase2 ,death2=death2 ,ndeath2=ndeath2 ,lastUpdatedAtApify2=lastUpdatedAtApify2 ,previousDayTests2=previousDayTests2 ,recovered2=recovered2 ,nRecovered2=nRecovered2
    ,region1=region1,acase1=acase1,deceased1=deceased1,newDeceased1=newDeceased1,newRecovered1=newRecovered1,recovered1=recovered1,totalInfected1=totalInfected1
    ,len2=len(region1))


if __name__== "__main__":
    # For develop use true for end user make it false
    # app.run(debug=True)
    app.run(debug=False) 
    