
import pandas as pd
import pickle

def _save(save_data, filename):
    with open(filename, 'wb') as f:  
        pickle.dump(save_data, f)    

def _load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)    

def _html(df, filename):
    with open(filename, 'w') as f:
        print(df.to_html(), file=f)

def _csv(df, filename):
    with open(filename, 'w') as f:
        print(df.to_csv(), file=f)

def _xlsx(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, 'Sheet1')
    writer.save()

def _txt(text_data, filename):
    with open(filename, 'w') as f:
        print(text_data, file=f)
