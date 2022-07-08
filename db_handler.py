#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import sqlite3


#executes an sql query on the database and returns the result
def execute(query, args=()):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(query, args)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result



#ensures the database is setup
def setup():
    execute("""CREATE TABLE IF NOT EXISTS polls ( 
        id INTEGER NOT NULL,
        results_id INTEGER NOT NULL,
        PRIMARY KEY (id)
    );""")
    execute("""CREATE TABLE IF NOT EXISTS poll_results (
        poll_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        selection INTEGER,
        FOREIGN KEY (poll_id) REFERENCES polls(id),
        PRIMARY KEY (poll_id, user_id)
    );""")


#saves a poll into the database
def save_poll(poll_id:int, results_id:int):
    execute("INSERT INTO polls VALUES (?, ?)", (poll_id, results_id))

#saves a poll result into the database
def save_poll_result(poll_id:int, user_id:int, selection:int):
    #if the user has not already voted, insert their selection
    if execute("SELECT * FROM poll_results WHERE poll_id = ? AND user_id = ?", (poll_id, user_id)) == []:
        execute("INSERT INTO poll_results VALUES (?, ?, ?)", (poll_id, user_id, selection))
    else:
        #if the user has already voted, update their selection
        execute("UPDATE poll_results SET selection = ? WHERE poll_id = ? AND user_id = ?", (selection, poll_id, user_id))


#gets the poll results for a poll
#returns result_id, counts. Where result_id is the id of the message that contains the results, and counts is a list of the number of votes for each option
def get_poll_results(poll_id:int):
    query_result = execute("SELECT selection FROM poll_results WHERE poll_id = ?", (poll_id,))
    counts = []
    for row in query_result:
        s = row[0] #the selection

        #if needed, expand counts to fit the selected option
        while len(counts) < s + 1:
            counts.append(0)

        counts[s] += 1

    #get the message id of the results message
    results_id = execute("SELECT results_id FROM polls WHERE id = ?", (poll_id,))[0][0]

    return results_id, counts
        
