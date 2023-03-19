from newspaper import Article
import nltk


def summary_generator(url):
    a = Article(url)
    a.download()
    a.parse()
    a.nlp()
    summary = a.summary
    return summary 


