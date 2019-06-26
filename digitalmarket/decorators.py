from django.http import Http404 
import functools 


# from functools import partial, update_wrapper
# # after : http://louistiao.me/posts/adding-__name__-and-__doc__-attributes-to-functoolspartial-objects/
# def wrapped_partial(func, *args, **kwargs):
#     partial_func = partial(func, *args, **kwargs)
#     update_wrapper(partial_func, func)
#     return partial_func


# https://stackoverflow.com/questions/308999/what-does-functools-wraps-do/309000#309000
# mitch = initial
def ajax_required(function):
	'''
	This is a doc string 
	'''
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			raise Http404("AJAX REQUIRED - regards from DECORATORS.py")
		return function(request, *args, **kwargs)

	# wrap.__doc__ = function.__doc__
	# wrap.__name__ = function.__name__
	# # ERROR:  'functools.partial' object has no attribute '__name__'
	# # https://bugs.python.org/issue3445
	# # https://bugs.python.org/issue4113
	return wrap



# do not do: 
# from functools import wraps 
# as functools.wraps only preserves the name and the docstring of the wrapper callable



# Graham D. http://blog.dscpl.com.au/2014/01/how-you-implemented-your-python.html, https://github.com/GrahamDumpleton/wrapt/tree/master/blog

# import wrapt # after Hynek Schlawack  https://hynek.me/articles/decorators/#tldr
# pip install wrapt 
# @wrapt.decorator
# def wrapt_decorator(wrapped, instance, args, kw):
#     print('Calling decorated function')
#     return wrapped(*args, **kw) 

# class C:
#     @wrapt_decorator
#     @classmethod
#     def cm(cls):
#         return 44322

