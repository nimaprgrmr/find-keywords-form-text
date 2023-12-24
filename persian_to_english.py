from googletrans import Translator


def translate_to_english(sentence):
    translator = Translator()
    translation = translator.translate(sentence, src='fa', dest='en')
    return translation.text


# print(translate_to_english("دریافت نقدی به صندق به مبلغ 500 هزار تومان از نیما اصل توقیری"))


from hazm import Normalizer, word_tokenize

def custom_ner(sentence):
    # Your rule-based logic to identify entities
    # This is a simple example and needs adaptation for Persian

    entities = []
    if "نقدی" in sentence:
        entities.append(("topic", "دریافت نقدی"))
    if "صندق" in sentence:
        entities.append(("subject", "صندق"))

    # Regular expression patterns for potential entities
    patterns = [
        (r'\d+ هزار تومان', 'value'),  # Matches patterns like "500 هزار تومان"
        (r'از (.+)', 'object'),  # Matches patterns like "از نیما اصل توقیری"
    ]

    tokens = word_tokenize(sentence)
    sentence = ' '.join(tokens)

    for pattern, label in patterns:
        match = re.search(pattern, sentence)
        if match:
            entities.append((label, match.group(0)))

    return entities

# Example usage
import re

persian_sentence = "دریافت نقدی به صندق به مبلغ 500 هزار تومان از نیما اصل توقیری"
result = custom_ner(persian_sentence)
print(result)

