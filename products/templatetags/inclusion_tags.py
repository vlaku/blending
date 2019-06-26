from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import requests
from django import template
import datetime
import sys

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
