from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from zscore.models import Priority, Goal, GoalSnapshot

import datetime

def index(request):
    goals = Goal.objects.all()


    
    
    dictionary = {
        'empty' : "nothin",
        'priorityList' : Priority.objects.all(),
        'zscore' : 85,
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
    post = request.POST
    g = Goal.objects.all().filter(id=int(post["id"])).get()

    p = int(post["progress"])

    newSnap = GoalSnapshot(goal=g, date=datetime.datetime.now(), progress=p)

    newSnap.save()
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


    













