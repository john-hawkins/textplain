import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torchtext.data import Field, Dataset, Example
from torchtext.data import TabularDataset, BucketIterator, Iterator
from transformers import BertTokenizer, BertForSequenceClassification

import PyTorchDataFrameDataset as pdfds

##############################################################################################
# Pipeline_PyTorch_Transformer_Classifier 
#
# A text classifer using a Pretrained-Transformer Network from the HuggingFace library
#
#
###############################################################################################
class BERT(nn.Module):
    def __init__(self):
        super(BERT, self).__init__()
        options_name = "bert-base-uncased"
        self.encoder = BertForSequenceClassification.from_pretrained(options_name)
    def forward(self, text, label):
        loss, text_fea = self.encoder(text, labels=label)[:2]
        return loss, text_fea


###############################################################################################
class Pipeline_PyTorch_Transformer_Classifier():

    # Model parameter
    MAX_SEQ_LEN = 128

    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.device = torch.device('cpu')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.PAD_INDEX = self.tokenizer.convert_tokens_to_ids(self.tokenizer.pad_token)
        self.UNK_INDEX = self.tokenizer.convert_tokens_to_ids(self.tokenizer.unk_token)
        self.num_epochs = 10
        self.criterion = nn.BCELoss()
        self.label_field = Field(sequential=False, use_vocab=False, batch_first=True, dtype=torch.float)
        self.text_field = Field(use_vocab=False, tokenize=self.tokenizer.encode, lower=False, include_lengths=False, batch_first=True,
                   fix_length=self.MAX_SEQ_LEN, pad_token=self.PAD_INDEX, unk_token=self.UNK_INDEX)



    ###################################################################################################
    def fit(self, df, text, label):
        """
            This function expects a pandas dataframe and two strings that determine the names of
            of the text features column and the target column.
        """
        train_iter, valid_iter = prepare_data_iterators(df, text, label)
        self.model = BERT()
        self.optimizer = optim.Adam(self.model.parameters(), lr=2e-5)
        self.train(rain_iter, valid_iter)
        return self


    ###################################################################################################
    def prepare_data_iterators(df, text, label):
        """
            This function will take a Pandas dataframe and the names of the text and label columns
            and it will generate PyTorch Dataset Iterators to be used for training the model.
            We allocate 10% of the data for validation.
        """
        mask = np.random.rand(len(df)) < 0.9
        train = df[mask]
        valid = df[~mask]
        self.fields = {'label': self.label_field, 'text': self.text_field}
        train_ds = pdfds.DataFrameDataset(train, self.fields)
        valid_ds = pdfds.DataFrameDataset(valid, self.fields)
        train_iter = BucketIterator(train_ds, batch_size=16, sort_key=lambda x: len(x.text),
                             train=True, sort=True, sort_within_batch=True)
        valid_iter = BucketIterator(valid_ds, batch_size=16, sort_key=lambda x: len(x.text),
                             train=True, sort=True, sort_within_batch=True)
        return train_iter, valid_iter 

    ###################################################################################################
    def train(self, train_loader, valid_loader):
        best_valid_loss = float("Inf")
        eval_every = len(train_loader) // 2
        # initialize running values
        running_loss, valid_running_loss = 0.0, 0.0
        global_step = 0
        train_loss_list = []
        valid_loss_list = []
        global_steps_list = []
        # training loop
        self.model.train()
        for epoch in range(self.num_epochs):
            for (labels, text), _ in train_loader:
                labels = labels.type(torch.LongTensor)
                text = text.type(torch.LongTensor)
                output = self.model(text, labels)
                loss, _ = output
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                # update running values
                running_loss += loss.item()
                global_step += 1
                # evaluation step
                if global_step % eval_every == 0:
                    self.model.eval()
                    with torch.no_grad():
                        # validation loop
                        for (labels, text), _ in valid_loader:
                            labels = labels.type(torch.LongTensor)
                            text = text.type(torch.LongTensor)
                            output = self.model(text, labels)
                            loss, _ = output
                            valid_running_loss += loss.item()
                    # evaluation
                    average_train_loss = running_loss / eval_every
                    average_valid_loss = valid_running_loss / len(valid_loader)
                    train_loss_list.append(average_train_loss)
                    valid_loss_list.append(average_valid_loss)
                    global_steps_list.append(global_step)
                    # resetting running values
                    running_loss = 0.0
                    valid_running_loss = 0.0
                    self.model.train()
                    # print progress 
                    print('Epoch [{}/{}], Step [{}/{}], Train Loss: {:.4f}, Valid Loss: {:.4f}'
                          .format(epoch+1, self.num_epochs, global_step, self.num_epochs*len(train_loader),
                                  average_train_loss, average_valid_loss))
                    # checkpoint
                    if best_valid_loss > average_valid_loss:
                        best_valid_loss = average_valid_loss
                        self.save_checkpoint(self.results_dir + '/' + 'self.model.pt', self.model, best_valid_loss)
                        self.save_metrics(self.results_dir + '/' + 'metrics.pt', train_loss_list, valid_loss_list, global_steps_list)
        self.save_metrics(self.results_dir + '/' + 'metrics.pt', train_loss_list, valid_loss_list, global_steps_list)
        print('Finished Training!')


    ###################################################################################################3
    def save_checkpoint(self, save_path, model, valid_loss):
        if save_path == None:
            return
        state_dict = {'model_state_dict': model.state_dict(),'valid_loss': valid_loss}
        torch.save(state_dict, save_path)
        print(f'Model saved to ==> {save_path}')

    ###################################################################################################3
    def load_checkpoint(self, load_path, model):
        if load_path==None:
            return
        state_dict = torch.load(load_path, map_location=device)
        print(f'Model loaded from <== {load_path}')
        model.load_state_dict(state_dict['model_state_dict'])
        return state_dict['valid_loss']

    ###################################################################################################3
    def save_metrics(self, save_path, train_loss_list, valid_loss_list, global_steps_list):
        if save_path == None:
            return
        state_dict = {'train_loss_list': train_loss_list,
                  'valid_loss_list': valid_loss_list,
                  'global_steps_list': global_steps_list}
        torch.save(state_dict, save_path)
        print(f'Model saved to ==> {save_path}')

    ###################################################################################################3
    def load_metrics(self, load_path):
        if load_path==None:
            return
        state_dict = torch.load(load_path, map_location=device)
        print(f'Model loaded from <== {load_path}')
        return state_dict['train_loss_list'], state_dict['valid_loss_list'], state_dict['global_steps_list']

    ###################################################################################################3
    def predict(self, df):
        """
            Given a DataFrame that has the two required fields from training, make predictions for
            each row.
        """
        results = []      
        _ds =  pdfds.DataFrameDataset(df, self.fields) 
        _iter = BucketIterator(_ds, batch_size=16, sort_key=lambda x: len(x.text),
                                 train=False, sort=True, sort_within_batch=True)
        self.odel.eval()
        with torch.no_grad():
            for (labels, text), _ in _iter:
                    labels = labels.type(torch.LongTensor)
                    text = text.type(torch.LongTensor)
                    _, output = self.model(text, labels)
                    sm = torch.nn.Softmax(dim=1)
                    results.extend( sm(output).tolist()[1] )
        return results

    ###################################################################################################3
