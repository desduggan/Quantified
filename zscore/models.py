from django.db import models
import datetime, calendar

# Create your models here.

class Priority(models.Model):
    """ A priority class
    examples:
        Networking
        Fitness
        Programming Skills

     """
    # each priority has a name
    name = models.CharField(max_length=50)

    # each priority has a current value relative to other 
    # priorities
    currentWeight = models.FloatField('Current Weight')

    def __unicode__(self): 
        return self.name

class Goal(models.Model):
    """ a Goal class"""
    # each goal has an associated priority
    priority = models.ForeignKey(Priority)

    # the primitikve construction of a goal
    # think SMART
    verb = models.CharField(max_length=30)
    value = models.IntegerField('Goal Value')
    unit = models.CharField(max_length=30)
    FREQUENCY = (
        ('d', 'Day'),
        ('w', 'Week'),
        ('m', 'Month'),
        ('y', 'Year'),
    )
    frequency = models.CharField(max_length=10, choices=FREQUENCY)

    # every goal has a lifetime
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def getExpectedProgress(self):
        totalProgress = -1
        if self.frequency == 'Month':
            today = datetime.datetime.now()
            daysInMonth = float(calendar.monthrange(today.year,today.month)[1])
            return (float(today.day) / daysInMonth) * 100.0

        elif self.frequency == 'Week':
            today = datetime.datetime.now()
            weekday = today.weekday()+1
            return (weekday/7.0) * 100.0

        elif self.frequency == 'Day':
            today = datetime.datetime.now()
            firstHour = today.replace(minute=0, second=0, microsecond=0, hour=0)
            fiveAM = firstHour + datetime.timedelta(0.209)
            tenPM = firstHour + datetime.timedelta(0.921)

            if today < fiveAM:
                return 0.0
            elif today > tenPM:
                return 1.0
            else:
                return float((today.hour - fiveAM.hour)) / float((tenPM.hour - fiveAM.hour)) * self.value *100.0

    def getProgress(self):
        snaps = self.goalsnapshot_set.all()
        
        if len(snaps) == 0:
            return 0

        totalProgress = 0
        if self.frequency == 'Month':
            # get first day in the month
            today = datetime.datetime.now()
            firstDayOfMonth = today - datetime.timedelta(today.day-1)
            lastDayOfMonth = firstDayOfMonth + datetime.timedelta(calendar.monthrange(today.year,today.month)[1]-1)

            totalProgress = 0
            for snap in snaps:
                if snap.date >= firstDayOfMonth.date() and snap.date <= lastDayOfMonth.date():
                    totalProgress += snap.progress

        elif self.frequency == 'Week':

            mostRecentSunday = self.getNearestSunday()
            nextSunday = mostRecentSunday + datetime.timedelta(7)

            totalProgress = 0
            for snap in snaps:
                if snap.date < nextSunday.date() and snap.date >= mostRecentSunday.date(): #progress was made this week
                    totalProgress += snap.progress

        elif self.frequency == 'Day':
            today = datetime.datetime.now()
            firstHour = today.replace(minute=0, second=0, microsecond=0, hour=0)
            lastHour = firstHour + datetime.timedelta(1)

            for snap in snaps:
                if snap.date < lastHour.date() and snap.date >= firstHour.date():
                    totalProgress += snap.progress

        return (totalProgress/float(self.value))*100

    def getNearestSunday(self):
        today = datetime.datetime.now()
        weekday = today.weekday()
        lastSunday = today - datetime.timedelta(weekday + 1)
        return lastSunday

    def __unicode__(self): 
        return self.verb + " " + str(self.value) + " " + self.unit + " " + self.frequency


class GoalSnapshot(models.Model):
    """docstring for GoalSnapshot"""
    goal = models.ForeignKey(Goal)

    # the date of the snapshot
    date = models.DateField()

    # the progress made towards the goal for this snapshot
    progress = models.IntegerField('Progress')

    def __unicode__(self): 
        return str(self.progress) + " made on " + str(self.date)
        

class ZScoreSnapshot(models.Model):
    """docstring for ZScoreSnapshot"""
    value = models.IntegerField('ZScore')
    date = models.DateTimeField()

    def __unicode__(self): 
        return "ZScore from " + str(self.date) + ": " + str(self.value)
        





