import force_connectivity
import thinkstats
import math


def Mean(t):
	return float(sum(t) / len(t))

def Var(t, mu=None):
	if mu is None:
		mu = Mean(t)

	dev2 = [(x-mu)**2 for x in t]
	var = Mean(dev2)
	return var

def std(variance):
	return math.sqrt(variance)

def PartitionRecords(table):

	accepted_sms = force_connectivity.Cases()
	others = force_connectivity.Cases()

	for case in table.records:
		if case.accepted_sms:
			accepted_sms.AddRecord(case)
		else:
			others.AddRecord(case)

	return accepted_sms, others

def Process(table):
	table.percent_outcomes = [c.percent_outcomes_submitted for c in table.records]
	table.n = len(table.percent_outcomes)
	table.mu = Mean(table.percent_outcomes)

def MakeTables(data_dir='.'):
	table = force_connectivity.Cases()
	table.ReadRecords(data_dir)

	accepted_sms, others = PartitionRecords(table)
	return table, accepted_sms, others

def ProcessTables(*tables):
	for table in tables:
		Process(table)

def Summarize(data_dir):

	table, accepted_sms, others = MakeTables(data_dir)
	ProcessTables(accepted_sms, others)

	print('Number accepted sms: %s'% accepted_sms.n)
	print('Number not accepted sms: %s'% others.n)

	mu1, mu2 = accepted_sms.mu, others.mu
	var1, var2 = Var(accepted_sms.percent_outcomes, mu1), Var(others.percent_outcomes, mu2)
	std1, std2 = std(var1), std(var2)

	print("mean outcomes submitted")
	print("accepted sms: %s"% mu1)
	print("others: %s"% mu2)

	print('Std Deviation:')
	print('accepted sms %s'% std1)
	print('others %s', std2)

	print('difference in std dev: %s'% (std1-std2))


def main(name, data_dir='.'):
    Summarize(data_dir)


if __name__ == '__main__':
    import sys
    main(*sys.argv)