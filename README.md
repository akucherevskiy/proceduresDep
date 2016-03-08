
There are a lot of stored procedures in databases, so we have to move that logic to php code. To do this, we have to know how to do it. I recommend migrate step-by-step, choosing one store procedure, that calls from php code, and migrate it to be sure that everything is fine. But, a lot of stored procedures use else stored procedures, so now we have the same dependencies in stored procedures like in php code. Scanner script will help you to find all dependencies that stored procedure has.
optional arguments:

  -h, --help        :    show this help message and exit\n
  -f FILENAME, --fileName FILENAME, required* : file name
  -count COUNT, --count COUNT :   Count of procedures and functions
  -pvsg PRETTYVIEWSORTEDGRAPH, --prettyViewSortedGraph PRETTYVIEWSORTEDGRAPH:  Pretty View Sorted Graph
  -p PROCEDURE, --procedure PROCEDURE:  Show Stored Procdure Dependencies
