#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 15:58:18 2023

@author: ahorpeda
"""
import mysql.connector

def connect_to_db():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='ahorpeda',
        database='snake_highscore'
        )
    return db

def registrer_new_record(db, name, score):
    cursor = db.cursor()
    cursor.execute("INSERT INTO  Highscore (name, score) VALUES (%s,%s)", (name, score))
    db.commit()
    
def retrive_top_3_records(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Highscore")
    results = cursor.fetchall()
    results_sorted = sorted(results, key=lambda tup: tup[1], reverse=True)
    results_sorted_top_3 = results_sorted[:3]
    return results_sorted_top_3
    
def get_char_from_int(integer):
    char_dict = {97: 'a',
                 98: 'b',
                 99: 'c',
                 100: 'd',
                 101: 'e',
                 102: 'f',
                 103: 'g',
                 104: 'h',
                 105: 'i',
                 106: 'j',
                 107: 'k',
                 108: 'l',
                 109: 'm',
                 110: 'n',
                 111: 'o',
                 112: 'p',
                 113: 'q',
                 114: 'r',
                 115: 's',
                 116: 't',
                 117: 'u',
                 118: 'v',
                 119: 'w',
                 120: 'x',
                 121: 'y',
                 122: 'z',}
    return char_dict[integer]
