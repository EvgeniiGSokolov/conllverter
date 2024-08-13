from nltk import sent_tokenize as st
from tkinter.filedialog import askopenfilename as ask
import re, stanza, conllu, chardet, docx

pipeline = stanza.Pipeline(lang='orv',processors='lemma,tokenize,pos,depparse')

def new_gettext(file):
    try:
        if file.endswith('.txt'):
            text = open(rf'{file}','rb')
            text_body = text.read()
            enc = chardet.detect(text_body).get("encoding")
            if enc and enc.lower() != "utf-8" and enc.lower() != "windows-1251":
                text_body = text_body.decode(enc)
                text_body = text_body.encode("utf-8")
                text_body = text_body.decode("utf-8")
                return text_body
            elif enc and enc.lower() == "windows-1251":
                text = open(rf'{file}', 'r', encoding = 'windows-1251')
                text_body = text.read()
                text.close()
                return text_body
            else:
                text = open(rf'{file}', 'r', encoding = 'UTF-8')
                text_body = text.read()
                text.close()
                return text_body
        elif file.endswith('.docx'):
            doc = docx.Document(rf'{file}')
            text = (paragraph.text for paragraph in doc.paragraphs)
            text_body = '\n'.join(text)
            return text_body
        else:
            pass
    except:
        pass

address = ask()
filename = address.split('/')[-1]
name = filename.split('.')[0]
text = new_gettext(address)
text = re.sub('[\[\]\<\>]','',text)
text = re.sub('\/.+\/','',text) #Убрать обозначения листов
text = '\n\n'.join(st(text))
doc = pipeline(text)

res = "{:C}".format(doc)
sents = conllu.parse_tree(res)
serialized = [sent.serialize() for sent in sents]
joined = '\n'.join(serialized)
with open(rf'C:\Users\pan_l\Desktop\Thesis\Conllu\{name}.conllu','w',encoding='UTF-8') as conl:
    conl.write(joined)
    conl.close()