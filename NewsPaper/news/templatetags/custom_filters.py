# from django import template
#
#
# register = template.Library()
#
#
# def censor(value):
#     if not isinstance(value, str):
#         raise ValueError('Нельзя цензурировать не строку')
#
# value_list = value.split()
# new_list = []
#
#     for word in value_list:
#         if word in stop_list_symbol:
#             new_list.append(word[0]+'*' * (len(word) - 1))
#         else:
#             new_list.append(word)
#
#     return " ".join(new_list)