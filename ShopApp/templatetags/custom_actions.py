from django import template

register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def str_to_list(val):
  return val.split(' ')

@register.filter
def transact(val):
  val = str(val)
  val.replace("transact","")
  return val