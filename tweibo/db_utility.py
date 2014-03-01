#!/usr/bin/env python
#coding=utf-8

import sqlite3

def move_to_namenumber(cu, namenumber):
    i = 1
    cu.execute("select * from queue")
    row = cu.fetchone()
    while i < namenumber:
        i = i + 1
        row = cu.fetchone()

def check_queue(cu, tname):
    cu.execute('select * from queue where name=?',tname)
    if cu.fetchone():
        return True
    else:
        return False

def insert_to_fntable(cu, canshu):
    cu.executemany('insert into fntable values(?,?,?)',canshu)
    cx.commit()

def insert_to_queue(cu, canshu):
    cu.executemany('insert into queue values(?,?)',canshu)
    cx.commit()


