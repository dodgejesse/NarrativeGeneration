
class GSREvent:

	def __init__(self, eid, country, state, city, event, population, date):

		self.eid=eid
		self.country=country
		self.state=state
		self.city=city
		self.event=event
		self.population=population
		self.date=date

	def __str__(self):
		return "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (self.event, self.country, self.state, self.city, self.date.year, self.date.month, self.date.day)
