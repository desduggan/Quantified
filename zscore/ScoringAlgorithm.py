from score.models import Goal, GoalSnapshot, Priority, ZScoreSnapshot

def normalize(data):
    """
   	return a normalize array
    """
    total = float(sum(data))
    if total == 0.0: return
    normalizedList = []
    for item in data:
        normalizedList.append(item/total)
    return normalizedList

def getTotalZscore():
	""" 
	Zk_1 = Zk + Fk

	Zk = ZScore at discrete time k
	Zk_1 = ZScore at discrete time k+1
	Fk = state transition based on progress made on goals

	"""

	Zk = 

	# first, normalize all of the weights of the priorities
	priorities = Priority.objects.all()
	weights = [p.currentWeight for p in priorities]
	weights = normalize(weights)

	# get zscore for each goal in each priority
	for p in priorities:







