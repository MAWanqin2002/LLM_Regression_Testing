import openai
import time
from dataset import Tw_dataloader
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
import sys


openai.api_key = "" #Type your own api key here
openai.Model.list()
txt_file1 = "./dataset/Github.txt"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)
 
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff2(**kwargs):
    return openai.Completion.create(**kwargs)

def model_t(content,model_name,prompts,t):
   model_prompt = prompts.format(text = content)
   # print(model_prompt)
   
   if model_name == "gpt-3.5-turbo" or model_name == "gpt-3.5-turbo-0301" :
      try:
         response = completion_with_backoff(                
                model=model_name,
                messages=[{"role": "user", "content": model_prompt}],
                max_tokens=1000,
                temperature=t)
         return response['choices'][0]['message']['content']
      except:
         response = "Invalid"
         return response
   else :
      try: 
         response = completion_with_backoff2(
                 model=model_name,
                 prompt=model_prompt,
                 max_tokens=1000,
                 temperature=t,
               )
         return response['choices'][0]['text'].replace('\n', '')
      except:
         response = "Invalid"
         return response

def get_plist():
   prompt1 ='''
   Classify the Github Discussion as "toxic" or "non-toxic". Only reply with the label.
   Document:
   """
   {text}
   """
   Label:
   '''
   
   
   prompt2 = '''
   Document:
   """
   {text}
   """
   Classify the Github Discussion as "toxic" or "non-toxic". Only reply with the label.
   Label:
   '''
   
   prompt3 = '''
   Below is a GitHub issue discussion, sometimes the discussion can get heated and have toxic comments. 
   Toxic comments can contain curse words, can sound condescending, can be mean to others, or can make people feel angry without using offensive words
   Please classify the discussion below. Only reply with the label 'toxic' or 'non-toxic'
   Document:
   """
   {text}
   """
   Label:
   '''
   
   
   prompt4 = '''
   Classify the document as "toxic" or "non-toxic". Only reply with the label.
   
   Document 1:
   """
   User nof:  I am now faced with the following error; ModuleNotFoundError: No module named 'imageai'
   User vina: Try installing !pip install opencv-python.
   """
   Label: "Non-toxic"
   
   Document 2:
   """
   User prob: A multi-platform app UI toolkit with the name of maui was introduced by Microsoft on May 19th, 2020 according to https://devblogs.microsoft.com/dotnet/introducing-net-multi-platform-app-ui/
   User dan: You find the comparison between a city in Hawaii and MauiKit ridiculous just like I find your comparison between an the Maui abbreviation and MauiKit ridiculous
   """
   Label: "Toxic"
   
   Document 3:
   """
   {text}
   """
   Label: "
   # '''
   
   
   p_list = [prompt1,prompt2,prompt3,prompt4]
   return p_list

def test_step_flip(model_name,p_list,contents):
   Res_List = [75, 117, 121, 124, 148, 153, 159, 165, 168, 172]
   Impro_List = [112, 123, 127, 143, 145, 147, 156, 163, 166, 169, 171]
   Unfilp_List = [0,1,2,3,4,5,6,7,8,9,10,101,102,103,104,105,106,107,108,109,110]
   List = [Res_List,Impro_List,Unfilp_List]
   file_name = ["__Res","__Imp","__Unf"]
   
   t=0.7
   for k in range(len(List)):
      sub_list = List[k]
      sub_name = file_name[k]
      for i in range(len(p_list)):
         txt_name = "./Github_0.7_test/"+model_name+sub_name+str(i+1)+".txt"
         p = p_list[i]
         print("Now test ",model_name," with prompt ",str(i+1))
         with open(txt_name,"w") as o:
            for y in range(len(sub_list)):
               index = sub_list[y]
               for j in range(20):
               # print("Now "+str(j+1)+" Test")
                  content = contents[index]
                  # first_line = ids[index]
                  first_line = content.split('\n')[0]
                  content = content.split('\n')[1:]
                  response = model_t(content,model_name,p,t)
                  print(str(first_line)+ "\t" + response)
                  o.write(str(first_line)+"\t"+response+"\n")

def test_step(model_name,p_list,contents):
   t = 0
   for i in range(1):
      txt_name = "./Github_Results/"+model_name+"__"+str(i+1)+".txt"
      p = p_list[i]
      print("Now test ",model_name," with prompt ",str(i+1))
      with open(txt_name,"w") as o:
         for i in range(len(contents)):
            first_line = contents[i].split('\n')[0]
            # first_line = ids[i]
            content = contents[i].split('\n')[1:]
            # print(content)
            # content = contents[i]
            response = model_t(content,model_name,p,t)
            print(str(first_line)+ "\t" + response)
            o.write(str(first_line)+"\t"+response+"\n")

      
       
def main():
   #Initialization
   with open(txt_file1, 'r') as file:
      contents = file.read().split("---------END---------\n")
   print("Total dataset",len(contents))

   p_list = get_plist()
   model_list = ["gpt-3.5-turbo-instruct","gpt-3.5-turbo-0613","gpt-3.5-turbo-0301","text-davinci-003","text-davinci-002"]
   
   for i in range(len(model_list)):
      test_step(model_list[i],p_list,contents) 
      test_step_flip(model_list[i],p_list,contents)
   
   print("finish")
   
if __name__ == "__main__":
    main()