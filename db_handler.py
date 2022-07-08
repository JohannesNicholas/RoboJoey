#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import sqlite3


#executes an sql query on the database and returns the result
def execute(query, args=()):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(query, args)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result



#ensures the database is setup
def setup():
    execute("""CREATE TABLE IF NOT EXISTS polls (
        id INTEGER,
        results_id INTEGER
        PRIMARY KEY id
    )""")
    execute("""CREATE TABLE IF NOT EXISTS poll_results (
        poll_id INTEGER,
        user_id INTEGER,
        selection INTEGER,
        FOREIGN KEY poll_id REFERENCES polls(id)
        PRIMARY KEY (poll_id, user_id)
    )""")



#gets the poll results for a poll
#returns result_id, counts. Where result_id is the id of the message that contains the results, and counts is a list of the number of votes for each option
def get_poll_results(poll_id):
    query_result = execute("SELECT selection FROM poll_results WHERE poll_id = ?", (poll_id))
    counts = []
    for row in query_result:
        s = row[0] #the selection

        #if needed, expand counts to fit the selected option
        while len(counts) < s + 1:
            counts.append(0)

        counts[s] += 1

    #get the message id of the results message
    results_id = execute("SELECT results_id FROM polls WHERE id = ?", (poll_id))[0][0]

    return results_id, counts
        
