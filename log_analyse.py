import glob
import re
import operator
from datetime import datetime
from dateutil.parser import parse
from tabulate import tabulate
from collections import OrderedDict


ts_pattern = '\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s(.)\d{4}'
user_pattern = '(?<=\s/\w{8}/\w{8}/)\w{8}'
top_user_count = 5

class User:
    def __init__(self,user_id,session_count,last_session_ts,total_pages,longest_session,shortest_session,last_page_request_ts):
        self.user_id = user_id
        self.session_count = session_count
        self.last_session_ts = last_session_ts
        self.total_pages = total_pages
        self.longest_session = longest_session
        self.shortest_session = shortest_session
        self.last_page_request_ts = last_page_request_ts
    
    def increment_total_pages(self):
        self.total_pages += 1
    
    def increment_session_count(self):
        self.session_count += 1
    
    def get_attributes(self):
        attributes = [self.user_id, self.total_pages,self.session_count,self.longest_session, self.shortest_session]
        return attributes

    
    



def print_stats(user_sessions):
    print('---------------------------------------------------------------')
    print('Here are the statistics from the logs: ')
    if(user_sessions is not None):
        unique_users = "Total unique users: {}"
        print(unique_users.format(len(user_sessions)))
        print('Top users:')
        print(tabulate((item.get_attributes() for item in user_sessions.values()), headers=['id', '# pages', '# sess', 'longest', 'shortest']))
    print('---------------------------------------------------------------')

def extract_entity(line, pattern):
    ts= None;
    match = re.search(pattern, line)
    if match is not None:
        ts = match.group()
    return ts


def get_stats(log_folder_path):
    users = dict()
    for file_name in glob.glob(log_folder_path):
        with open(file_name, 'r') as f:
            for line in f:
                user_id = extract_entity(line, user_pattern)
                current_datetime = parse(extract_entity(line, ts_pattern), fuzzy=True)
                if(user_id is not None and user_id.strip()):
                    if(user_id in  users):
                        userObj = users[user_id]
                        userObj.increment_total_pages()
                        if((current_datetime-userObj.last_page_request_ts).total_seconds() <= 600):
                                #Page request is with in the session. Update last page request_ts  
                                #Also update the session duration
                                if(userObj.last_session_ts is None):
                                    userObj.last_session_ts = current_datetime
                                userObj.last_page_request_ts = current_datetime
                                session_duration = (userObj.last_page_request_ts-userObj.last_session_ts).total_seconds()/60
                                #update longest and shortest duration for the user
                                if(userObj.session_count == 1):
                                    userObj.shortest_session = session_duration
                                if(session_duration< userObj.shortest_session):
                                    userObj.shortest_session = session_duration
                                if(session_duration>=userObj.longest_session):
                                    userObj.longest_session =  session_duration
                                
                        else:
                                #Must be new session 
                                userObj.increment_session_count()
                                #compute session duration
                                session_duration = (userObj.last_page_request_ts-userObj.last_session_ts).total_seconds()/60  
                                #update longest and shortest duration for the user
                                if(session_duration< userObj.shortest_session or userObj.shortest_session == 0):
                                    userObj.shortest_session = session_duration
                                if(session_duration>=userObj.longest_session):
                                    userObj.longest_session =  session_duration
                                userObj.last_session_ts = current_datetime
                                userObj.last_page_request_ts = current_datetime
                    else:
                        userObj = User(user_id,1,current_datetime,1,0,0,current_datetime)
                        users[user_id] = userObj
        f.close()
    return users

def analyze():
    #Sort the dictionary on top users in terms of page views and print the report
    users = get_stats('./data/logs/*')
    orderedUsers = OrderedDict(sorted(users.items(), key=lambda x: x[1].total_pages, reverse = True))
    while len(orderedUsers) > top_user_count:
        orderedUsers.popitem()
    print_stats(orderedUsers)

if __name__ == '__main__':
    analyze()

                    
            
            



