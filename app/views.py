from flask import render_template, flash, redirect, session
from app import app
from .forms import Districts,Issues,Vote,Matches

@app.route('/')
@app.route('/districts', methods=['GET', 'POST'])
def districts():
    form = Districts()
    session['issues'] = ()
    if form.validate_on_submit():
       zipcodeInput = form.zipcode.data

       #save in session for later
       session['zipcode'] = zipcodeInput

       import urllib, json
       url = "https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s&apikey=43b59706ee1641e3b709806527b9cd81" % zipcodeInput
       response = urllib.urlopen(url)
       data = json.loads(response.read())
       data = data["results"]

       return render_template('districts.html',
                           title='Display ZIP',
                           form=form,
                           zipcodeInput=zipcodeInput,
                           data=data)

    return render_template('districts.html',
                           title='Collect ZIP',
                           form=form,
                           zipcodeInput="")

@app.route('/issues', methods=['GET', 'POST'])
def issues():
    form = Issues()
    keywordsCount = len(session['issues'])
    keywordsInput = session['issues']
    if form.validate_on_submit():
       session['issues'] += (form.keywords.data,)
       keywordsInput = session['issues']

       #clear textbox for next entry
       form.keywords.data = ""
       
       return render_template('issues.html',
                           title='Collect Issues',
                           form=form,
                           keywordsInput=keywordsInput,
                           keywordsCount=keywordsCount)
    return render_template('issues.html',
                           title='Collect Issues',
                           form=form,
                           keywordsInput=keywordsInput,
                           keywordsCount=keywordsCount)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    form = Vote()

    import urllib, json
    url1 = "https://congress.api.sunlightfoundation.com/bills/search?query=%s&highlight=true&history.enacted=true&fields=summary_short&per_page=2&apikey=43b59706ee1641e3b709806527b9cd81" % session['issues'][0]
    url2 = "https://congress.api.sunlightfoundation.com/bills/search?query=%s&highlight=true&history.enacted=true&fields=summary_short&per_page=2&apikey=43b59706ee1641e3b709806527b9cd81" % session['issues'][1]
    url3 = "https://congress.api.sunlightfoundation.com/bills/search?query=%s&highlight=true&history.enacted=true&fields=summary_short&per_page=2&apikey=43b59706ee1641e3b709806527b9cd81" % session['issues'][2]
    url4 = "https://congress.api.sunlightfoundation.com/bills/search?query=%s&highlight=true&history.enacted=true&fields=summary_short&per_page=2&apikey=43b59706ee1641e3b709806527b9cd81" % session['issues'][3]
    url5 = "https://congress.api.sunlightfoundation.com/bills/search?query=%s&highlight=true&history.enacted=true&fields=summary_short&per_page=2&apikey=43b59706ee1641e3b709806527b9cd81" % session['issues'][4]

    response1 = urllib.urlopen(url1)
    response2 = urllib.urlopen(url2)
    response3 = urllib.urlopen(url3)
    response4 = urllib.urlopen(url4)
    response5 = urllib.urlopen(url5)

    votes1 = json.loads(response1.read())
    votes2 = json.loads(response2.read())
    votes3 = json.loads(response3.read())
    votes4 = json.loads(response4.read())
    votes5 = json.loads(response5.read())

    votes1 = votes1['results']
    votes2 = votes2['results']
    votes3 = votes3['results']
    votes4 = votes4['results']
    votes5 = votes5['results']

    if form.validate_on_submit():
       session['myVotesStr'] = form.myVotes

       return redirect('/matches')
    return render_template('vote.html',
                            title='Vote on issues',
                            form=form,
                            key1=session['issues'][0],
                            key2=session['issues'][1],
                            key3=session['issues'][2],
                            key4=session['issues'][3],
                            key5=session['issues'][4],
                            votes1=votes1,
                            votes2=votes2,
                            votes3=votes3,
                            votes4=votes4,
                            votes5=votes5)

@app.route('/matches', methods=['GET', 'POST'])
def matches():
    form = Matches()

    import urllib, json
    zipcodeInput = session['zipcode']
    url = "https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s&apikey=43b59706ee1641e3b709806527b9cd81" %zipcodeInput
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data = data["results"]

    matchesYea = []

    for reps in data:
      matchCount = 0
      #our repid is: reps["bioguide_id"]
      print reps["bioguide_id"]
      #hard code myVotes
      myVotes = session['myVotesStr']
      for personalVote in myVotes.split(","):
        billid = personalVote.split(":")[0]
        #our vote is: personalVote
        url = "https://congress.api.sunlightfoundation.com/votes?bill_id=%s&fields=roll_id,voters.%s.vote,bill_id&apikey=43b59706ee1641e3b709806527b9cd81" % (billid,reps["bioguide_id"])
        #print url
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        #print data['results']

        try:
           if personalVote.split(":")[1] == data['results'][0]['voters'][reps["bioguide_id"]]['vote']:
              matchCount += 1
        except: 
           pass
        
      print matchCount

      matchesYea.append({"name" : reps["first_name"] + ' ' + reps["last_name"],
                     "size" : matchCount})


    """
    requires:
    maybe zipcode
    definitely RepIds
    definitely BillsIds
    definitely myVotes

    foreach rep, make api call based on their pk, and BillId
      count matches between their vote and mine
      percentage match, save to var
      print to screen
      iterate by rep, show %

      "the tinder of politics, yo" #DollaBills

      """





    return render_template('matches.html',
                          title='Your matches',
                          form=form,
                          repMatches='',
                          matchesYea=matchesYea)