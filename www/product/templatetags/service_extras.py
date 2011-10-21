# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def pln(value, arg='zł'):
    if value: return str(value) + arg
    else: return '-'

def comment_costs(obj, arg='zł'):
    to_join = []
    get_data = False
    for cost in [['sprzęt', obj.hardware], ['usługa', obj.software], ['dojazd', obj.transport]]:
        if cost[1] > 0: 
            to_join.append(cost[0] + ': ' + str(cost[1]) + 'zł')
            get_data = True
    if get_data: return "(" + ", ".join(to_join) + ")"
    else: return ''

register.filter('pln', pln)
register.filter('comment_costs', comment_costs)