### Packages à installer
# spacy==3.7.6
# python -m spacy download en_core_web_md
# python -m spacy download fr_core_news_md

import spacy
model_fr = spacy.load("fr_core_news_md")
model_en = spacy.load("en_core_web_md")

def lemmatize_text(text, language="fr"):
    if language == "fr":
        nlp = model_fr
    elif language == "en":
        nlp = model_en
    else:
        return 0
    doc = nlp(text)
    for token in doc:
        print(token, token.pos_)
    lemmatized_text = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "VERB", "ADV", "ADJ"]]
    return " ".join(lemmatized_text)

fr = "Une grosse grue était perchée sur le haut de l'arbre, elle regardait attentivement"
en = "When I was there before, I had to consider buying the houses altogether"

print(lemmatize_text(fr, "fr"))
print(lemmatize_text(en, "en"))