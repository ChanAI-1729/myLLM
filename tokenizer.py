import os
import re
import tiktoken
import urllib.request

if not os.path.exists("the_verdict.txt"):
    url = ("https://raw.githubusercontent.com/rasbt/"
           "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
           "the-verdict.txt")
    file_path="the_verdict.txt"
    urllib.request.urlretrieve(url, file_path)

with open("the_verdict.txt","r") as f:
    raw_text=f.read()

result=re.split(r'([,.:;?_!"()\']|--|\s)',raw_text)

preprocessed=[item.strip() for item in result if item.strip()]

#converting tokens into token id
all_words=sorted(set(preprocessed))
all_words.extend(['<|endoftext|>','<|unk|>'])
vocab_size=len(all_words)
print(vocab_size)

vocab={vocab:tok for tok,vocab in enumerate(all_words)}

class SimpleTokenizerV1:
    def __init__(self,vocab):
        self.str_to_int=vocab
        self.int_to_str={s:i for i,s in vocab.items()}
    def encode(self,text):
        result=re.split(r'([,.:;?_!"()\']|--|\s)',text)
        preprocessed=[item.strip() for item in result if item.strip()]
        ids=[self.str_to_int[s] for s in preprocessed]
        return ids
    def decode(self,ids):
        text=" ".join([self.int_to_str[id] for id in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

# tokenizer=SimpleTokenizerV1(vocab)
# text="it's the last he painted, you know"
# encoded=tokenizer.encode(text)
# decoded=tokenizer.decode(encoded)
# print(encoded,decoded)

class SimpleTokenizerV2:
    def __init__(self,vocab):
        self.str_to_int=vocab
        self.int_to_str={s:i for i,s in vocab.items()}
    def encode(self,text):
        result=re.split(r'([,.:;?_!"()\']|--|\s)',text)
        preprocessed=[item.strip() for item in result if item.strip()]
        preprocessed=[item if item in vocab else "<|unk|>" for item in preprocessed]
        ids=[self.str_to_int[s] for s in preprocessed]
        return ids
    def decode(self,ids):
        text=" ".join([self.int_to_str[id] for id in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text
# tokenizer=SimpleTokenizerV2(vocab)
# text="it's the lst he painted, you know"
# encoded=tokenizer.encode(text)
# decoded=tokenizer.decode(encoded)
# print(encoded,decoded)

