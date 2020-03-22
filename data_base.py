import sqlite3


def save_to_db(position, link_id, salary, company, people_count, address, requirements, description):
    conn = sqlite3.connect('vacancies.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE vacancies
    #              (Position text, Link_id text, Salary text, Company text, People_count text,
    #               Address text, Requirements text, Description text)''')
    c.execute('INSERT INTO vacancies VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (position, link_id, salary, company, people_count, address, requirements, description))
    conn.commit()
    conn.close()
