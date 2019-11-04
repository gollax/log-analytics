# log-analytics
Generate user session stats out of log files
Log file format example
`10.10.6.90 - - 15/Aug/2016:23:59:29 -0500 "POST /ecf8427e/b443dc7f/489f3e87/72cd2995?85f13c6c HTTP/1.0" 200 - "-" "AHC/1.0i" 8889 "10.10.200.11, 10.10.6.90" -`

Any request coming with in 10 mins of previous user request is considered to be in the same session.
The report prints out number of unique users and the top 5 users with respect to page requests in a descending order

Usage:
    1. Put all of the log files in <project_root>/data/logs
    2. Run python3 log_analyse.py to view the report

Tests:
    1. Go to the test folder
    2. Run python3 test_analytics.py


