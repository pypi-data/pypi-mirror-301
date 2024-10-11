from num2geotext.number_to_word import num_text


def one_or_two_digit_int_number(number: int) -> str:
    num = str(number)
    if len(num) == 1 or len(num) == 2:
      return f'{num_text[int(num[:])]}'
    else:
      raise ValueError("Not supported! The whole number must have one or two digits.")


def three_digit_int_number(number: int) -> str:
    num = str(number)
    if len(num) == 3:
      if num[0] == '1':
          if num[1:] == '00':
              return 'ასი'
          return f'ას {num_text[int(num[1:])]}'
      elif num_text[int(num[0])].endswith('ი') and num[1:] == '00':
          return f'{num_text[int(num[0])][:-1]}ასი'
      elif num_text[int(num[0])].endswith('ი') and num[1:] != '00':
          return f'{num_text[int(num[0])][:-1]}ას {one_or_two_digit_int_number(int(num[1:]))}'
      elif num_text[int(num[0])].endswith('ი') == False and num[1:] == '00':
          return f'{num_text[int(num[0])]}ასი'
      elif num_text[int(num[0])].endswith('ი') == False:
          return f'{num_text[int(num[0])]}ას {one_or_two_digit_int_number(int(num[1:]))}'
    else:
      raise ValueError("Not supported! The whole number must have three digits.")


def four_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 4:
    if num[0] == '1':
      if num[1:] == '000':
        return 'ათასი'
      elif num[1] == '1':
        return f'ათას ას {one_or_two_digit_int_number(int(num[2:]))}'
      elif num[1] == '0':
        return f'ათას {one_or_two_digit_int_number(int(num[2:]))}'
      else:
        return f'ათას {three_digit_int_number(int(num[1:]))}'
    elif num[0] != 1 and num[1] == '0' and num[2:] != '00':
      return f'{num_text[int(num[0])]} ათას {one_or_two_digit_int_number(int(num[2:]))}'
    elif num[0] != 1 and num[1:] == '000':
      return f'{num_text[int(num[0])]} ათასი'
    else:
      return f'{num_text[int(num[0])]} ათას {three_digit_int_number(int(num[1:]))}'
  else:
    raise ValueError("Not supported! The whole number must have four digits.")


def five_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 5:
    if num[2:] == '000':
      return f'{num_text[int(num[:2])]} ათასი'
    elif num[2] == '0' and num[3:] != '00':
      return f'{num_text[int(num[:2])]} ათას {one_or_two_digit_int_number(int(num[3:]))}'
    return f'{num_text[int(num[:2])]} ათას {three_digit_int_number(int(num[2:]))}'
  else:
    raise ValueError("Not supported! The whole number must have five digits.")


def six_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 6:
    if num[3:] == '000':
      return f'{three_digit_int_number(int(num[0:3]))} ათასი'
    elif num[3:5] == '00' and num[5] != 0:
      return f'{three_digit_int_number(int(num[0:3]))} ათას {one_or_two_digit_int_number(int(num[5:]))}'
    elif num[3] == '0' and num[4:] != '00':
      return f'{three_digit_int_number(int(num[0:3]))} ათას {one_or_two_digit_int_number(int(num[3:]))}'
    else:
      return f'{three_digit_int_number(int(num[0:3]))} ათას {three_digit_int_number(int(num[3:]))}'
  else:
    raise ValueError("Not supported! The whole number must have six digits.")


def seven_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 7:
    if num[1:] == '000000':
      return f'{num_text[int(num[0])]} მილიონი'
    elif num[1:5] == '0000':
      return f'{num_text[int(num[0])]} მილიონ {one_or_two_digit_int_number(int(num[5:]))}'
    elif num[1:4] == '000':
      return f'{num_text[int(num[0])]} მილიონ {three_digit_int_number(int(num[4:]))}'
    elif num[1:3] == '00':
      return f'{num_text[int(num[0])]} მილიონ {four_digit_int_number(int(num[3:]))}'
    elif num[1] == '0':
      return f'{num_text[int(num[0])]} მილიონ {five_digit_int_number(int(num[2:]))}'
    else:
      return f'{num_text[int(num[0])]} მილიონ {six_digit_int_number(int(num[1:]))}'
  else:
    raise ValueError("Not supported! The whole number must have seven digits.")


def eight_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 8:
    if num[2:] == '000000':
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონი'
    elif num[2:6] == '0000':
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონ {one_or_two_digit_int_number(int(num[6:]))}'
    elif num[2:5] == '000':
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონ {three_digit_int_number(int(num[5:]))}'
    elif num[2:4] == '00':
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონ {four_digit_int_number(int(num[4:]))}'
    elif num[2] == '0':
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონ {five_digit_int_number(int(num[3:]))}'
    else:
      return f'{one_or_two_digit_int_number(int(num[0:2]))} მილიონ {six_digit_int_number(int(num[2:]))}'
  else:
    raise ValueError("Not supported! The whole number must have eight digits.")


def nine_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 9:
    if num[3:] == '000000':
      return f'{three_digit_int_number(int(num[0:3]))} მილიონი'
    elif num[3:7] == '0000':
      return f'{three_digit_int_number(int(num[0:3]))} მილიონ {one_or_two_digit_int_number(int(num[7:]))}'
    elif num[3:6] == '000':
      return f'{three_digit_int_number(int(num[0:3]))} მილიონ {three_digit_int_number(int(num[6:]))}'
    elif num[3:5] == '00':
      return f'{three_digit_int_number(int(num[0:3]))} მილიონ {four_digit_int_number(int(num[5:]))}'
    elif num[3] == '0':
      return f'{three_digit_int_number(int(num[0:3]))} მილიონ {five_digit_int_number(int(num[4:]))}'
    else:
      return f'{three_digit_int_number(int(num[0:3]))} მილიონ {six_digit_int_number(int(num[3:]))}'
  else:
    raise ValueError("Not supported! The whole number must have nine digits.")


def ten_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 10:
    if num[1:] == '000000000':
      return f'{num_text[int(num[0])]} მილიარდი'
    elif num[1:8] == '0000000':
      return f'{num_text[int(num[0])]} მილიარდ {one_or_two_digit_int_number(int(num[8:]))}'
    elif num[1:7] == '000000':
      return f'{num_text[int(num[0])]} მილიარდ {three_digit_int_number(int(num[7:]))}'
    elif num[1:6] == '00000':
      return f'{num_text[int(num[0])]} მილიარდ {four_digit_int_number(int(num[6:]))}'
    elif num[1:5] == '0000':
      return f'{num_text[int(num[0])]} მილიარდ {five_digit_int_number(int(num[5:]))}'
    elif num[1:4] == '000':
      return f'{num_text[int(num[0])]} მილიარდ {six_digit_int_number(int(num[4:]))}'
    elif num[1:3] == '00':
      return f'{num_text[int(num[0])]} მილიარდ {seven_digit_int_number(int(num[3:]))}'
    elif num[1:2] == '0':
      return f'{num_text[int(num[0])]} მილიარდ {eight_digit_int_number(int(num[2:]))}'
    else:
      return f'{num_text[int(num[0])]} მილიარდ {nine_digit_int_number(int(num[1:]))}'
  else:
    raise ValueError("Not supported! The whole number must have ten digits.")


def eleven_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 11:
    if num[1:] == '0000000000':
      return f'{num_text[int(num[0:2])]} მილიარდი'
    elif num[1:9] == '00000000':
      return f'{num_text[int(num[0:2])]} მილიარდ {one_or_two_digit_int_number(int(num[9:]))}'
    elif num[1:8] == '0000000':
      return f'{num_text[int(num[0:2])]} მილიარდ {three_digit_int_number(int(num[8:]))}'
    elif num[1:7] == '000000':
      return f'{num_text[int(num[0:2])]} მილიარდ {four_digit_int_number(int(num[7:]))}'
    elif num[1:6] == '00000':
      return f'{num_text[int(num[0:2])]} მილიარდ {five_digit_int_number(int(num[6:]))}'
    elif num[1:5] == '0000':
      return f'{num_text[int(num[0:2])]} მილიარდ {six_digit_int_number(int(num[5:]))}'
    elif num[1:4] == '000':
      return f'{num_text[int(num[0:2])]} მილიარდ {seven_digit_int_number(int(num[4:]))}'
    elif num[1:3] == '00':
      return f'{num_text[int(num[0:2])]} მილიარდ {eight_digit_int_number(int(num[3:]))}'
    else:
      return f'{num_text[int(num[0:2])]} მილიარდ {nine_digit_int_number(int(num[2:]))}'
  else:
    raise ValueError("Not supported! The whole number must have eleven digits.")


def twelve_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 12:
    if num[3:] == '000000000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდი'
    elif num[3:10] == '0000000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {one_or_two_digit_int_number(int(num[10:]))}'
    elif num[3:9] == '000000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {three_digit_int_number(int(num[9:]))}'
    elif num[3:8] == '00000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {four_digit_int_number(int(num[8:]))}'
    elif num[3:7] == '0000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {five_digit_int_number(int(num[7:]))}'
    elif num[3:6] == '000':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {six_digit_int_number(int(num[6:]))}'
    elif num[3:5] == '00':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {seven_digit_int_number(int(num[5:]))}'
    elif num[3:4] == '0':
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {eight_digit_int_number(int(num[4:]))}'
    else:
      return f'{three_digit_int_number(int(num[:3]))} მილიარდ {nine_digit_int_number(int(num[3:]))}'
  else:
    raise ValueError("Not supported! The whole number must have twelve digits.")


def thirteen_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 13:
    if num[1:] == '000000000000':
      return f'{num_text[int(num[0])]} ტრილიონი'
    elif num[1:11] == '0000000000':
      return f'{num_text[int(num[0])]} ტრილიონ {one_or_two_digit_int_number(int(num[11:]))}'
    elif num[1:10] == '000000000':
      return f'{num_text[int(num[0])]} ტრილიონ {three_digit_int_number(int(num[10:]))}'
    elif num[1:9] == '00000000':
      return f'{num_text[int(num[0])]} ტრილიონ {four_digit_int_number(int(num[9:]))}'
    elif num[1:8] == '0000000':
      return f'{num_text[int(num[0])]} ტრილიონ {five_digit_int_number(int(num[8:]))}'
    elif num[1:7] == '000000':
      return f'{num_text[int(num[0])]} ტრილიონ {six_digit_int_number(int(num[7:]))}'
    elif num[1:6] == '00000':
      return f'{num_text[int(num[0])]} ტრილიონ {seven_digit_int_number(int(num[6:]))}'
    elif num[1:5] == '0000':
      return f'{num_text[int(num[0])]} ტრილიონ {eight_digit_int_number(int(num[5:]))}'
    elif num[1:4] == '000':
      return f'{num_text[int(num[0])]} ტრილიონ {nine_digit_int_number(int(num[4:]))}'
    elif num[1:3] == '00':
      return f'{num_text[int(num[0])]} ტრილიონ {ten_digit_int_number(int(num[3:]))}'
    elif num[1:2] == '0':
      return f'{num_text[int(num[0])]} ტრილიონ {eleven_digit_int_number(int(num[2:]))}'
    else:
      return f'{num_text[int(num[0])]} ტრილიონ {twelve_digit_int_number(int(num[1:]))}'
  else:
    raise ValueError("Not supported! The whole number must have thirteen digits.")


def fourteen_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 14:
    if num[2:] == '000000000000':
      return f'{num_text[int(num[0:2])]} ტრილიონი'
    elif num[1:12] == '00000000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {one_or_two_digit_int_number(int(num[12:]))}'
    elif num[1:11] == '0000000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {three_digit_int_number(int(num[11:]))}'
    elif num[1:10] == '000000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {four_digit_int_number(int(num[10:]))}'
    elif num[1:9] == '00000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {five_digit_int_number(int(num[9:]))}'
    elif num[1:8] == '0000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {six_digit_int_number(int(num[8:]))}'
    elif num[1:7] == '000000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {seven_digit_int_number(int(num[7:]))}'
    elif num[1:6] == '00000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {eight_digit_int_number(int(num[6:]))}'
    elif num[1:5] == '0000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {nine_digit_int_number(int(num[5:]))}'
    elif num[1:4] == '000':
      return f'{num_text[int(num[0:2])]} ტრილიონ {ten_digit_int_number(int(num[4:]))}'
    elif num[1:3] == '00':
      return f'{num_text[int(num[0:2])]} ტრილიონ {eleven_digit_int_number(int(num[3:]))}'
    else:
      return f'{num_text[int(num[0:2])]} ტრილიონ {twelve_digit_int_number(int(num[2:]))}'
  else:
    raise ValueError("Not supported! The whole number must have fourteen digits.")


def fifteen_digit_int_number(number: int) -> str:
  num = str(number)

  if len(num) == 15:
    if num[3:] == '000000000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონი'
    elif num[3:13] == '0000000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {one_or_two_digit_int_number(int(num[13:]))}'
    elif num[3:12] == '000000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {three_digit_int_number(int(num[12:]))}'
    elif num[3:11] == '00000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {four_digit_int_number(int(num[11:]))}'
    elif num[3:10] == '0000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {five_digit_int_number(int(num[10:]))}'
    elif num[3:9] == '000000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {six_digit_int_number(int(num[9:]))}'
    elif num[3:8] == '00000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {seven_digit_int_number(int(num[8:]))}'
    elif num[3:7] == '0000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {eight_digit_int_number(int(num[7:]))}'
    elif num[3:6] == '000':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {nine_digit_int_number(int(num[6:]))}'
    elif num[3:5] == '00':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {ten_digit_int_number(int(num[5:]))}'
    elif num[3:4] == '0':
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {eleven_digit_int_number(int(num[4:]))}'
    else:
      return f'{three_digit_int_number(int(num[0:3]))} ტრილიონ {twelve_digit_int_number(int(num[3:]))}'
  else:
    raise ValueError("Not supported! The whole number must have fifteen digits.")


def int_num_to_geo_text(number: int) -> str:
    num = str(number)
    num_len = len(num)

    if num_len == 1 or num_len == 2:
        return one_or_two_digit_int_number(number)
    elif num_len == 3:
        return three_digit_int_number(number)
    elif num_len == 4:
        return four_digit_int_number(number)
    elif num_len == 5:
        return five_digit_int_number(number)
    elif num_len == 6:
        return six_digit_int_number(number)
    elif num_len == 7:
        return seven_digit_int_number(number)
    elif num_len == 8:
        return eight_digit_int_number(number)
    elif num_len == 9:
        return nine_digit_int_number(number)
    elif num_len == 10:
        return ten_digit_int_number(number)
    elif num_len == 11:
        return eleven_digit_int_number(number)
    elif num_len == 12:
        return twelve_digit_int_number(number)
    elif num_len == 13:
        return thirteen_digit_int_number(number)
    elif num_len == 14:
        return fourteen_digit_int_number(number)
    elif num_len == 15:
        return fifteen_digit_int_number(number)
    else:
        raise ValueError("Not supported! The maximum allowable digits is 15")

