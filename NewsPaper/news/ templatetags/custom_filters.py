from django import template


register = template.Library()

stop_list_symbol = ['р', 'е', 'д', 'и', 'с', 'к', 'а']

@register.filter()
def censor(value):
      if not isinstance(value, str):
         raise ValueError('Нельзя цензурировать не строку')

      new_word = []
      for value in stop_list_symbol:
         if value is stop_list_symbol:
            new_word.append('*')

      return new_word
