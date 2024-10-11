
from num2geotext.int_num_to_geo_text import one_or_two_digit_int_number, three_digit_int_number, four_digit_int_number, five_digit_int_number, six_digit_int_number, seven_digit_int_number, eight_digit_int_number, nine_digit_int_number, ten_digit_int_number, eleven_digit_int_number, twelve_digit_int_number, thirteen_digit_int_number, fourteen_digit_int_number, fifteen_digit_int_number


def custom_round(value: float, decimal_places: int):
    factor = 10 ** decimal_places
    return round(value * factor + 0.0001) / factor


def one_or_two_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has either one or two digits before the decimal point.")

  if (num.index('.') == 1 or num.index('.') == 2) and len(num) >= 5:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 100.0:
    return f"ასი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{one_or_two_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[-1]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{one_or_two_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1:]))} მეასედი"
  else:
    return None


def three_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has three digits before the decimal point.")

  if num.index('.') == 3 and len(num) > 6:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 1_000.0:
    return f"ათასი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{three_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{three_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def four_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has four digits before the decimal point.")

  if num.index('.') == 4 and len(num) > 7:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 10_000.0:
    return f"ათი ათასი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{four_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{four_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def five_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has five digits before the decimal point.")

  if num.index('.') == 5 and len(num) > 8:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 100_000.0:
    return f"ასი ათასი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{five_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{five_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def six_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has six digits before the decimal point.")

  if num.index('.') == 6 and len(num) > 9:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 1_000_000.0:
    return f"ერთი მილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{six_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{six_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def seven_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has seven digits before the decimal point.")

  if num.index('.') == 7 and len(num) > 10:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 10_000_000.0:
    return f"ათი მილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{seven_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{seven_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def eight_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has eight digits before the decimal point.")

  if num.index('.') == 8 and len(num) > 11:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 100_000_000.0:
    return f"ასი მილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{eight_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{eight_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def nine_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has nine digits before the decimal point.")

  if num.index('.') == 9 and len(num) > 12:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 1_000_000_000.0:
    return f"ერთი მილიარდი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{nine_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{nine_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def ten_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has ten digits before the decimal point.")

  if num.index('.') == 10 and len(num) > 13:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 10_000_000_000.0:
    return f"ათი მილიარდი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{ten_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{ten_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def eleven_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has eleven digits before the decimal point.")

  if num.index('.') == 11 and len(num) > 14:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 100_000_000_000.0:
    return f"ასი მილიარდი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{eleven_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{eleven_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def twelve_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has twelve digits before the decimal point.")

  if num.index('.') == 12 and len(num) > 15:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 1_000_000_000_000.0:
    return f"ერთი ტრილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{twelve_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{twelve_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def thirteen_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has thirteen digits before the decimal point.")

  if num.index('.') == 13 and len(num) > 16:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 10_000_000_000_000.0:
    return f"ათი ტრილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{thirteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{thirteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def fourteen_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has fourteen digits before the decimal point.")

  if num.index('.') == 14 and len(num) > 17:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 100_000_000_000_000.0:
    return f"ასი ტრილიონი მთელი, ნული მეათედი"
  elif len(num[num.index('.') + 1:]) == 1:
    return f"{fourteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{fourteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def fifteen_digit_float_number(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has fifteen digits before the decimal point.")

  if num.index('.') == 15 and len(num) > 18:
    num = str(custom_round(float(num), 2))

  if custom_round(float(num), 2) == 1_000_000_000_000_000.0:
    return f"ერთი კუადრილიონი მთელი, ნული მეათედი"
  if len(num[num.index('.') + 1:]) == 1:
    return f"{fifteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეათედი"
  elif len(num[num.index('.') + 1:]) == 2:
    return f"{fifteen_digit_int_number(int(num[:num.index('.')]))} მთელი, {one_or_two_digit_int_number(int(num[num.index('.') + 1 :]))} მეასედი"
  else:
    return None


def float_num_to_geo_text(number: float) -> str:
  if isinstance(number, float):
    num = str(number)
  else:
    raise ValueError(f"This function requires a float value that has a maximum of 15 digits before the decimal point.")


  if num.index('.') == 1 or num.index('.') == 2:
    return one_or_two_digit_float_number(number)
  elif num.index('.') == 3:
    return three_digit_float_number(number)
  elif num.index('.') == 4:
    return four_digit_float_number(number)
  elif num.index('.') == 5:
    return five_digit_float_number(number)
  elif num.index('.') == 6:
    return six_digit_float_number(number)
  elif num.index('.') == 7:
    return seven_digit_float_number(number)
  elif num.index('.') == 8:
    return eight_digit_float_number(number)
  elif num.index('.') == 9:
    return nine_digit_float_number(number)
  elif num.index('.') == 10:
    return ten_digit_float_number(number)
  elif num.index('.') == 11:
    return eleven_digit_float_number(number)
  elif num.index('.') == 12:
    return twelve_digit_float_number(number)
  elif num.index('.') == 13:
    return thirteen_digit_float_number(number)
  elif num.index('.') == 14:
    return fourteen_digit_float_number(number)
  elif num.index('.') == 15:
    return fifteen_digit_float_number(number)
  elif custom_round(float(num), 2) == 1_000_000_000_000_000.0:
    return f"ერთი კუადრილიონი მთელი, ნული მეათედი"
  else:
    raise ValueError(f"This function requires a float value that has a maximum of 15 digits before the decimal point.")

