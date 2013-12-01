from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from zscore.models import Priority, Goal, GoalSnapshot, ZScoreSnapshot

import datetime

from django.utils import timezone

def index(request):
    goals = Goal.objects.all()

    scores = ZScoreSnapshot.objects.all().order_by("-date")

    presentZScore = None
    if len(scores) == 0:
        presentZScore = 85
    else:
        presentZScore = scores[0].value
    
    dictionary = {
        'empty' : "nothin",
        'priorityList' : Priority.objects.all(),
        'zscore' : presentZScore,
    }
    c = Context(dictionary)
    c.update(csrf(request))
    return render_to_response('zscore/index_2.html', c, context_instance=RequestContext(request))


def goalAdd(request):
    post = request.POST
    priority = get_object_or_404(Priority, name=post["priority"])
    verb = post["verb"]
    value = float(post["value"])
    unit = post["unit"]
    frequency = post["frequency"]

    startDate = datetime.datetime.now()

    g = Goal(priority = priority, verb = verb, value = value, unit = unit, frequency = frequency, startDate = startDate, endDate=startDate)
    g.save()

    return redirect("/")

def goalDelete(request):
    post = request.POST
    goalId = int(post["id"])

    g = Goal.objects.all().filter(id=goalId).get()
    g.delete()

    return redirect("/")

def priorityAdd(request):
    post = request.POST
    weight = float(post["weight"])
    name = post["name"]

    p = Priority(name=name, currentWeight=weight)
    p.save()
    return redirect("/")

def priorityDelete(request):
    post = request.POST
    pId = int(post["id"])

    # delete the priority
    p = Priority.objects.all().filter(id=pId).get()
    p.delete()

    return redirect("/")

def snapshotAdd(request):
    # initial Values
    dailyCost = -1.0
    maxGain = 5.0


    # Save a new snapshot for this goal
    post = request.POST
    g = Goal.objects.all().filter(id=int(post["id"])).get()
    progress = int(post["progress"])
    newSnap = GoalSnapshot(goal=g, date=datetime.datetime.now(), progress=progress)
    newSnap.save()

    # get weight of priority
    priority = g.priority
    weight = float(priority.currentWeight)
    totWeights = sum([pIter.currentWeight for pIter in Priority.objects.all()])
    normalizedWeight = weight / totWeights

    # Get update amount
    # first, find percent progress made towards goal
    goalObjective = float(g.value)
    percentProgress = progress / goalObjective

    # Progress is based on percent towards maxGain
    Fk = int(percentProgress * maxGain)

    # weight based on priority
    Fk = Fk * normalizedWeight

    # get old Z Value
    scores = ZScoreSnapshot.objects.all().order_by("-date")
    
    Zk = None
    delta = None
    if len(scores) == 0:
        Zk = 85
        delta = 0
    else:
        ZScoreSnap = scores[0]
        ZScoreSnapDate = ZScoreSnap.date
        Zk = ZScoreSnap.value

        delta = abs((ZScoreSnapDate - timezone.now() + datetime.timedelta(1)).days)

    # Lose 'dailycost' per day
    # get number of days between updates
    totalLoss = delta * dailyCost
        
    # update ZScore
    Zk_1 = Zk + totalLoss + Fk

    # save the new snapshot
    ZSnap = ZScoreSnapshot(value=Zk_1, date=datetime.datetime.now())
    ZSnap.save()

    return redirect("/")

def snapshotDelete(request):
    post = request.POST
    g = Goal.objects.all().filter(id=int(post["id"])).get()

    p = int(post["progress"])

    p = -1*p

    newSnap = GoalSnapshot(goal=g, date=datetime.datetime.now(), progress=p)

    newSnap.save()
    return redirect("/")

    
    # dateComponents = request.POST['date'].split('/')
    # year = int(dateComponents[2])
    # month = int(dateComponents[0])
    # day = int(dateComponents[1])
    # workout_date = datetime.date(year, month, day)


    













