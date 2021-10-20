import os
import sqlite3


# Create a database
conn = sqlite3.connect('example.db')


##conn.execute('CREATE TABLE IF NOT EXISTS projects (id integer PRIMARY KEY,name text NOT NULL,begin_date text,end_date text)')
##print ("projects Country created successfully");
##                                    
##
##conn.execute('CREATE TABLE IF NOT EXISTS students ( name Text ,addr TEXT, city TEXT, pin TEXT)')
##print (" students Table created successfully");
##
##conn.execute('CREATE TABLE IF NOT EXISTS tasks ( id integer PRIMARY KEY, name text NOT NULL,priority integer ,status_id integer NOT NULL,project_id integer NOT NULL, begin_date text,end_date text NOT NULL )')
##print (" tasks Table created successfully");
##
##conn.execute('CREATE TABLE IF NOT EXISTS upload_tb ( id integer PRIMARY KEY, filename text NOT NULL)')
##print (" upload_tb Table created successfully");

                                
                                                

conn.row_factory = sqlite3.Row
# Make a convenience function for running SQL queries
def sql_query(query):
    conn = sqlite3.connect('example.db')#otherwise error SQLite objects created in a thread can only be used in that same thread
    conn.row_factory = sqlite3.Row#will not get displayed 
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def sql_edit_insert(query,var):
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()
    return cur.rowcount
  

def sql_delete(query,var):
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()
    return cur.rowcount

def sql_query2(query,var):
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    return rows
