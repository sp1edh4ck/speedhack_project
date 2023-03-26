from datetime import datetime as dt


def year(request):
	year = dt.today()
	return {
		'year': year.year,
	}
