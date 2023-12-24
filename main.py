import pandas as pd
from hazm import Normalizer, word_tokenize
import numpy as np
from timeit import default_timer as timer


keys = pd.read_excel("structure.xlsx")

forms = ['فروش', 'خرید', 'دریافت', 'پرداخت', 'تسویه', 'انتقال وجه', 'واریز', 'تنخواه']
scales_value = ['هزار', 'میلیون', 'میلیارد']
units_value = ['ریال', 'تومان']


def extract_form(sentence):
    # Normalize the sentence
    normalizer = Normalizer()
    normalized_sentence = normalizer.normalize(sentence)

    # Tokenize the normalized sentence
    tokens = word_tokenize(normalized_sentence)

    # Extract key information
    form = None

    for i, token in enumerate(tokens):

        if token in forms:
            form = "".join(tokens[i])
            form_index = i

        if token == 'انتقال':
            form = 'انتقال وجه'
            form_index = i

        if token == 'تنخواه':
            form = "تنخواه هما"
            form_index = i

    if form is None:
        print("Form isnt available  in sentence")
        return "form unreachable"

    return form, form_index, tokens


def get_form_and_result(sentence=None):
    if sentence == None:
        sentence = input("درخواست خود را وارد کنید: ")
    form, form_index, tokens = extract_form(sentence)

    # extract variables for Sale
    if form == 'فروش':
        item, value, value_scale, value_unit, person, special = None, None, None, None, None, None

        b_index_person = None
        b_index_value = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):

            if form_index - 1 >= 0:
                special = " ".join(tokens[0:form_index])

            # find item based on index of form until lowest 'be' index
            item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value)])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

            if b_index_person > b_index_value:
                person = ' '.join(tokens[b_index_person:])
            else:
                person = ' '.join(tokens[b_index_person:b_index_value])

        if special is None:
            special = ''

        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value: {scale_value} | unit value: {unit_value} | person: {person}"

    # extract variables for buy
    if form == 'خرید':
        item, value, value_scale, value_unit, person, special = None, None, None, None, None, None

        b_index_value = None
        b_index_person = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):

            if form_index - 1 >= 0:
                special = " ".join(tokens[0:form_index])

            # find item based on index of form until lowest 'be' index
            if b_index_person is not None:
                item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value)])
            else:
                item = " ".join(tokens[form_index + 1:b_index_value])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

            if b_index_person == None:
                if token == 'از':
                    person = " ".join(tokens[i:])

            elif b_index_person > b_index_value:
                person = ' '.join(tokens[b_index_person:])
            else:
                person = ' '.join(tokens[b_index_person:b_index_value])

        if special is None:
            special = ''

        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value: {scale_value} | unit value: {unit_value} | person: {person}"

        # extract variables for recieve
    if form == 'دریافت':
        item, value, value_scale, value_unit, person1, person2 = None, None, None, None, None, None

        b_index_value = None
        b_index_person = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):
            # find item based on index of form until lowest 'be' index
            if b_index_person is not None:
                item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value)])
            else:
                item = " ".join(tokens[form_index + 1:b_index_value])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

            if token == 'از':
                person2 = " ".join(tokens[i:b_index_person])
            elif b_index_person > b_index_value:
                person1 = ' '.join(tokens[b_index_person:])
            else:
                person1 = ' '.join(tokens[b_index_person:b_index_value])

        return f"form: {form} | item: {item} | value: {value} | scale value:{scale_value} | unit value: {unit_value} | person1: {person1} | person2: {person2}"

    # Extract variables for payment
    if form == 'پرداخت':
        item, value, value_scale, value_unit, person = None, None, None, None, None

        b_index_person = None
        b_index_value = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):

            # find item based on index of form until lowest 'be' index
            item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value)])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

            if b_index_person > b_index_value:
                person = ' '.join(tokens[b_index_person:])
            else:
                person = ' '.join(tokens[b_index_person:b_index_value])

        return f"form: {form} | item: {item} | value: {value} | scale value: {scale_value} | unit_value: {unit_value} | person: {person}"

    if form == 'تنخواه هما':
        item, value, value_scale, value_unit, person, special = None, None, None, None, None, None

        b_index_value = None
        b_index_person = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):
            # find item based on index of form until lowest 'be' index
            if b_index_person is not None:
                item = " ".join(tokens[form_index + 2:min(b_index_person, b_index_value)])
            else:
                item = " ".join(tokens[form_index + 2:b_index_value])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

            # find person
            if b_index_person == None:
                person = ""
            elif b_index_person > b_index_value:
                person = ' '.join(tokens[b_index_person:])
            else:
                person = ' '.join(tokens[b_index_person:b_index_value])

            # find person2
            if token == 'از':
                person2 = " ".join(tokens[i:])

            # find special
            if form_index - 1 >= 0:
                special = " ".join(tokens[0:form_index])

        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value:{scale_value} | unit value: {unit_value} | person: {person} | person2: {person2}"

    # extract values from tankhah
    if form == 'انتقال وجه':
        value, value_scale, value_unit, person1, person2 = None, None, None, None, None

        b_index_person = None
        b_index_value = None

        for i, token in enumerate(tokens):
            if token == 'به' and tokens[i + 1] != 'مبلغ':
                b_index_person = i

            elif token == 'به' and tokens[i + 1] == 'مبلغ':
                b_index_value = i

        for i, token in enumerate(tokens):
            if token == 'از':
                person1 = " ".join(tokens[i:b_index_person])

            if b_index_person > b_index_value:
                person2 = ' '.join(tokens[b_index_person:])
            else:
                person2 = ' '.join(tokens[b_index_person:b_index_value])

            # find value, scale, unit based on digit or not
            if token.isdigit() and i + 1 < len(tokens):
                value, scale_value, unit_value = f"{token}", f"{tokens[i + 1]}", f"{tokens[i + 2]}"

        return f"form: {form} | value: {value} | scale_value: {scale_value} | unit_value: {unit_value} | person1: {person1} | person2:{person2}"


sentence = "مالیات و عوارض فروش کالاهای مشمول مالیات به مبلغ 69750 هزار تومان به محمد"

s_time = timer()
result = get_form_and_result(sentence)
e_time = timer()
print(result)
print(f"{(e_time - s_time):.3f} Seconds")

