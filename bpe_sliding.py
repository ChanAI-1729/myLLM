import tiktoken
import torch
from torch.utils.data import Dataset,DataLoader

class GPTDatasetV1(Dataset):
    def __init__(self,txt,tokenizer,max_length,stride):
        self.input_ids=[]
        self.target_ids=[]

        token_ids=tokenizer.encode(txt,allowed_special={'<|endoftext|>'})
        for i in range(0,len(token_ids)-max_length,stride):
            input_chunk=token_ids[i:i+max_length]
            target_chunk=token_ids[i+1:i+max_length+1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx],self.target_ids[idx]

def create_dataloader_v1(txt,batch_size=4,max_length=256,stride=128,shuffle=True,drop_last=True,num_workers=0):
    tokenizer=tiktoken.get_encoding("gpt2")
    dataset=GPTDatasetV1(txt,tokenizer,max_length,stride)
    dataloader=DataLoader(dataset,batch_size=batch_size,shuffle=shuffle,drop_last=drop_last,num_workers=num_workers)
    return dataloader


with open("the_verdict.txt",'r') as f:
    raw_text=f.read()

dataloader=create_dataloader_v1(raw_text,batch_size=8,max_length=4,stride=1,shuffle=False)
data_iter=iter(dataloader)
inputs,targets=next(data_iter)

#Creating token embeddings
torch.manual_seed(123)
token_embedding_layer=torch.nn.Embedding(num_embeddings=50257,embedding_dim=256)
token_embeddings=token_embedding_layer(inputs)
# print(token_embeddings.shape)
# print(token_embeddings)

context_length=max_length=4
output_dim=256
pos_embedding_layer=torch.nn.Embedding(context_length,output_dim)
pos_embedding=pos_embedding_layer(torch.arange(max_length))

input_embeddings=token_embeddings+pos_embedding
print(input_embeddings)
