import pandas as pd

import os

workspace_path = '/home/wons/evsim_chat'  # 파일 업로드한 경로 반영
path = os.path.join(workspace_path, 'game_record.csv')
df = pd.read_csv(path)

next_com = []

input_com = ['for', '_', 'in', 'range(5)', ':', 'won.F()']

df = df[df['Result'] == 'Command success']
df = df[df['Chat_ID'] == 5156920429]
df = df[df['Agent'] == 'won']

Command = list(df.Command.values)
com = []

for i in ['button R', 'button L', 'button F', 'button B'] :
  Command = [word for word in Command if word != i]

for i in Command :
    com.append([x for x in i.replace('\n','').split(' ') if x!=''])
    
for i in range(len(com)) : 
  if input_com == com[i]:
        next_com.append(com[i+1])

print(next_com)