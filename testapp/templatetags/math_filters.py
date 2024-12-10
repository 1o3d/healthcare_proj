from django import template

register = template.Library()

@register.filter
def multiply(value,arg):
    return value * arg

@register.simple_tag
def calccovcost(amt, price, cov):
    return float(amt) * float(price) * float(1 - (cov/100))