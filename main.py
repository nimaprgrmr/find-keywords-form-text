import pandas as pd
# from hazm import Normalizer, word_tokenize
import numpy as np
from timeit import default_timer as timer

forms = ['فروش', 'خرید', 'دریافت', 'پرداخت', 'تسویه', 'انتقال وجه', 'واریز', 'تنخواه']
scales_value = ['هزار', 'میلیون', 'میلیارد']
units_value = ['ریال', 'تومان']


def extract_form(sentence):
    global form_index
    form = None
    # Normalize the sentence
    #     normalizer = Normalizer()
    #     normalized_sentence = normalizer.normalize(sentence)

    # Tokenize the normalized sentence
    tokens = sentence.split(" ")

    for i, token in enumerate(tokens):
        if token in forms:
            form = "".join(tokens[i])
            form_index = i
            break

        elif token == 'انتقال':
            form = 'انتقال وجه'
            form_index = i

    if form is None:
        form = "form_unreachable"
        form_index = 0

    return form, form_index, tokens


def get_sentence():
    sentence = input("لطفا درخواست خود را وارد کنید: ")
    return sentence


def find_key_words(sentence=None):
    print(f"جمله وارد شده: {sentence}")
    if sentence is None:
        sentence = get_sentence()
    value = special = scale_value = unit_value = person1 = person2 = total_value = scale_value = unit_value = None
    b_index_value = None
    b_index_person = None
    form, form_index, tokens = extract_form(sentence)

    while form == 'form_unreachable':
        print("درخواست وارد شده معتبر نمیباشد")
        sentence = input("لطفا درخواست خود را وارد کنید: ")
        form, form_index, tokens = extract_form(sentence)

    # FIND B_INDEXES
    for i, token in enumerate(tokens):
        if token == 'به' and tokens[i + 1] != 'مبلغ':
            b_index_person = i

        elif token == 'به' and tokens[i + 1] == 'مبلغ':
            b_index_value = i

    # FIND AZ
    try:
        idx_az = tokens.index('از')
    except ValueError:
        idx_az = None

    # FIND ITEM IN SENTENCE
    if idx_az is not None and b_index_person is not None:
        item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value, idx_az)])
    elif idx_az is None and b_index_person is not None:
        item = " ".join(tokens[form_index + 1:min(b_index_person, b_index_value)])
    else:
        item = " ".join(tokens[form_index + 1:b_index_value])

    # FIND PERSON 1, DIGITS, SPECIAL, PERSON 2
    for i, token in enumerate(tokens):
        if tokens[i] == 'از' and b_index_person is None and idx_az is not None and idx_az > b_index_value:
            person1 = " ".join(tokens[i:])
        elif tokens[i] == 'از' and b_index_person is None and idx_az is not None and idx_az < b_index_value:
            person1 = " ".join(tokens[i:b_index_value])
        elif tokens[i] == 'از' and i > b_index_person:
            person1 = " ".join(tokens[i:])
        elif tokens[i] == 'از' and i < b_index_person and i < b_index_value:
            if b_index_person < b_index_value:
                person1 = " ".join(tokens[i:b_index_person])
            else:
                person1 = " ".join(tokens[i:b_index_value])
        elif tokens[i] == 'از' and b_index_person > i > b_index_value:
            person1 = " ".join(tokens[i:b_index_person])
        elif 'از' not in tokens:
            person1 = ''

        # find value, scale, unit based on digit or not
        if token.isdigit() and i + 1 < len(tokens):
            value = f"{token}"

        if form_index - 1 >= 0:
            special = " ".join(tokens[0:form_index])
        else:
            special = ""

        # FIND PERSON 2
        if idx_az is not None:
            if b_index_person is not None and b_index_person > b_index_value and b_index_person > idx_az:
                person2 = ' '.join(tokens[b_index_person:])
            elif b_index_person is not None and b_index_value < b_index_person < idx_az:
                person2 = ' '.join(tokens[b_index_person:idx_az])
            elif b_index_person is not None and b_index_person < b_index_value:
                person2 = ' '.join(tokens[b_index_person:b_index_value])
            else:
                person2 = ''
        else:
            if b_index_person is not None and b_index_person > b_index_value:
                person2 = ' '.join(tokens[b_index_person:])
            elif b_index_person is not None and b_index_person < b_index_value:
                person2 = ' '.join(tokens[b_index_person:b_index_value])
            else:
                person2 = ''

    # FIND SCALE VALUE AND UNIT VALUE
    for tok in tokens:
        if tok in scales_value:
            scale_value = tok
        elif tok in units_value:
            unit_value = tok

    if value is None:
        print("مبلغ تراکنش وارد نشده است")
        special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words()
    elif scale_value is None:
        print("مبنای مبلغ وارد شده صحیح نمیباشد(صد، هزار، میلیون، میلیارد)")
        special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words()
    elif unit_value is None:
        print("واحد پولی وارد شده صحیح نمیباشد(ریال، تومان)")
        special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words()

    return special, form, item, value, scale_value, unit_value, person1, person2


def return_keywords(special, form, item, value, scale_value, unit_value, person1, person2):
    if form == 'فروش':
        while person2 == '':
            print("مشخص نشد به چه شخصی یا به چه کسی باید فروش برسد")
            sentence = get_sentence()
            special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)

        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value: {scale_value} | unit value: {unit_value} | person1: {person1} | person2: {person2}"

    # extract variables for buy
    if form == 'خرید':
        if len(special) > 2:
            while person2 == '':
                print(f"مشخص نشد به چه شخصی یا به چه کسی باید {special + ' ' + form} انجام شود")
                sentence = get_sentence()
                special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)
        else:
            while person1 == '':
                print("مشخص نشد خرید باید از چه شخصی یا از چه جایی انجام شود")
                sentence = get_sentence()
                special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)

        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value: {scale_value} | unit value: {unit_value} | person1: {person1} | person2: {person2}"

        # extract variables for recieve
    if form == 'دریافت':
        while person1 == '':
            print("مشخص نشد دریافت باید از چه شخصی یا از چه جایی انجام شود")
            sentence = get_sentence()
            special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)
        return f"form: {form} | item: {item} | value: {value} | scale value:{scale_value} | unit value: {unit_value} | person1: {person1} | person2: {person2}"

    # Extract variables for payment
    if form == 'پرداخت':
        while person2 == '':
            print("مشخص نشد پرداخت باید به چه شخصی یا به چه جایی انجام شود")
            sentence = get_sentence()
            special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)
        return f"form: {form} | item: {item} | value: {value} | scale value: {scale_value} | unit_value: {unit_value} | person1: {person1} | person2: {person2}"

    if form == 'تنخواه':
        return f"form: {special + ' ' + form} | item: {item} | value: {value} | scale value:{scale_value} | unit value: {unit_value} | person1: {person1} | person2: {person2}"

    # extract values from tankhah
    if form == 'انتقال وجه':
        if 'وجه' in item:
            item = item.replace('وجه', '')

        while person1 == '':
            print("مشخص نشد انتقال وجه باید از چه شخصی یا از چه جایی منتقل شود")
            sentence = get_sentence()
            special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)
        while person2 == '':
            print("مشخص نشد انتقال وجه باید به چه شخصی یا به چه منبعی منتقل شود")
            sentence = get_sentence()
            special, form, item, value, scale_value, unit_value, person1, person2 = find_key_words(sentence)

        return f"form: {form} | item: {item} | value: {value} | scale_value: {scale_value} | unit_value: {unit_value} | person1: {person1} | person2:{person2}"


s_time = timer()
sentence = "انتقال وجه از صندوق مرکزی به صندوق فروشگاه به مبلغ  45 هزار ریال"
key_words = find_key_words(sentence)
result = return_keywords(*key_words)
e_time = timer()
print(result)
print(f"{(e_time - s_time):.7f} Seconds")
