import sys, getopt, pprint, re, argparse, os

procedureMask = "` PROCEDURE `"
functionMask = "` FUNCTION `"
beginMask = "BEGIN"
endMask =  "END ;;"
functionCount = procedureCount = pos = 0
graph = newSort = {}
readLine = False
usages1 = usages2 = usages3 = stackOfNested = []
procedureName = ''
regMask = "(= [_]*[a-zA-Z]{1}[a-zA-Z_]+)[(]"
regMaskCall = "CALL ([_]*[a-zA-Z]{1}[a-zA-Z_]+)[(]"
regMask3 = "SELECT ([_]*[a-zA-Z]{1}[a-zA-Z_]+)[(]"
usage = ""
nest = -10 #mud
dictionary = {"CHAR" , "CONCAT", "LENGTH", "SUBSTRING", "IFNULL", "DATE_SUB", "IF", "FLOOR", "ELSEIF", "CURDATE", "VARCHAR", "NOW", "COUNT", "LAST_INSERT_ID", "GROUP_CONCAT", "COALESCE", "CAST", "TRIM", "DATE_ADD", "SUM", "INT", "WHILE", "SUBSTR", "MAX", "VALUES", "TRACE", "ENTER_MODULE", "ABS", "ROW_COUNT", "UNSUBSCRIBED", "MIN", "FROM", "ACTIVATION", "BADMAIL", "DISTINCT", "DATE", "ROUND", "TIME_TO_SEC", "TO_DAYS", "DATE_FORMAT", "CONCAT_WS", "YEARWEEK", "YEAR", "WEEK", "TINYINT", "TIMESTAMPDIFF", "MONTH", "DATEDIFF", "DECIMAL", "AVG", "IN", "UUID", "NOT", "UUID", "FLOAT", "REPLACE", "TIMESTAMP", "REPLACE", "SUBSTRING_INDEX", "ASCII", "ISNULL", "LOWER", "MID", "LOCATE", "XOCHIMILCO", "INSTR", "_ENCODE", "CURRENT_TIMESTAMP", "GREATEST", "UNIX_TIMESTAMP", "EXISTS", "CONVERT", "LEAST", "LPAD", "BIGINT", "INDEX", "UNIQUE", "DAYOFYEAR", "ON", "UPPER", "TIMEDIFF", "HAVING", "AND", ""}

class procedureScaner():
	def readFile(self, fileName):
		return open(fileName, 'r')

	def createGraphFromFile(self, _file, usages1, usages2, usages3):
		global procedureName
		global functionCount
		global procedureCount		
		for line in _file:
			if beginMask in line:
				usages1 =  usages2 = usages3 = []

			if procedureMask in line:
				line = line[len(procedureMask):]
				procedureName = line.split('`')[5]
				procedureCount = procedureCount + 1
			if functionMask in line:
				line = line[len(functionMask):]
				procedureName = line.split('`')[5]
				functionCount = functionCount + 1

			if re.search(regMask, line) <> None:
				if re.search( regMask, line).group(0)[0:-1] not in graph:
					usage = re.search(regMask, line).group(0)[2:-1]
					if usage.upper() not in dictionary and usage <> procedureName:
						usages1.append(usage)
			#cp-mud
			if re.search(regMaskCall, line) <> None:
				if re.search( regMaskCall, line).group(0)[0:-1] not in graph:
					usage = re.search(regMaskCall, line).group(0)[5:-1]
					if usage.upper() not in dictionary and usage <> procedureName:
						usages2.append(usage)
			#cp-mud
			if re.search(regMask3, line) <> None:
				if re.search( regMask3, line).group(0)[0:-1] not in graph:
					usage = re.search(regMask3, line).group(0)[7:-1]
					if usage.upper() not in dictionary and usage <> procedureName:
						usages3.append(usage)
			graph[procedureName] = set(usages1 + usages2 + usages3)
		
		return graph

	def getChilds(self, graph, origin, firstFlag):	
		global nest 
		global stackOfNested
		if len(graph) == 0 and nest>0:
			print '|' + nest *'-' + 'empty'
			nest = 0
		else:
			for item in graph:	
				if item not in stackOfNested:
					if not firstFlag:
						print "|"+nest*'-' + item
					nest = nest + 10 
					firstFlag = False 
			
					stackOfNested =stackOfNested + [item]
					tmp = origin[item]
					self.getChilds(tmp, origin, firstFlag)
	
	def getSortGraphByCount(self, graph):
		for key, value in graph.iteritems():
			newSort[key] = len(value)
		
		return newSort
	
	def prettyViewGraph(self, graph):
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(graph)
	
	def prettyViewSortedGraph(self, sortedGraph):
		from collections import OrderedDict
		from operator import itemgetter
		import json

		d = OrderedDict(sorted(newSort.items(), key=itemgetter(1)))
		print(json.dumps(d, indent=4))
	
	def printCount(self, graph):
		print "count of procedures: " + str(procedureCount)
		print "count of functions: " + str(functionCount)

def main(argv):
	parser = argparse.ArgumentParser(description = 'Stored Procedures Dependencies Scanner')
	parser.add_argument('-f','--fileName', help = 'Input file name', required = True)
	parser.add_argument('-count','--count', help = 'Count of procedures and functions', required = False)
	parser.add_argument('-pvsg','--prettyViewSortedGraph', help = 'Pretty View Sorted Graph', required = False)
	parser.add_argument('-p','--procedure', help = 'Show Stored Procdure Dependencies', required = False)
	args = parser.parse_args()
	
	scanner = procedureScaner()
	_file = scanner.readFile(args.fileName)
	graph = scanner.createGraphFromFile(_file, usages1, usages2, usages3)
	print "Creating gpraph ......................... done\n"

	if args.count:
		scanner.printCount(graph)
		return
	if args.prettyViewSortedGraph:
		sortedGraph = scanner.getSortGraphByCount(graph)
		scanner.prettyViewSortedGraph(sortedGraph)
		return
	if args.procedure:
		scanner.getChilds([args.procedure], graph, True)
		return
	if args.fileName :
		scanner.prettyViewGraph(graph)
		return
if __name__ == "__main__":
   main(sys.argv[1:])
   print "\nMagic is ................................ done"


