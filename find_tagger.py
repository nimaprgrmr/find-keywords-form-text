from hazm import *

normalizer = Normalizer()
normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')

sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')
word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')

tagger = POSTagger(model='pos_tagger.model')
response = tagger.tag(word_tokenize('دریافت نقدی صندق مبلغ 500 هزار تومان از نیما اصل توقیری'))


chunker = Chunker(model='chunker.model')
tagged = tagger.tag(word_tokenize(normalizer.normalize('درخواست دریافت نقدی به صندوق به مبلغ 500 هزار تومان از نیما اصل توقیری را دارم')))
response2 = tree2brackets(chunker.parse(tagged))
print(response2)


