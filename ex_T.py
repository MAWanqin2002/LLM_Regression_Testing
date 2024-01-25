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
   prompt1 = '''
   Classify the Twitter Comment as "toxic" or "non-toxic". Only reply with the label.
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
   Classify the Twitter Comment as "toxic" or "non-toxic". Only reply with the label.
   Label:
   '''
   
   prompt3 = '''
   Below is a Twitter Comment , sometimes the comment can get heated and be toxic. 
   Toxic comments can attack others' identity, can be insult, obscene,  sexual explicit and threat
   Please classify the Comment below. Only reply with the label 'toxic' or 'non-toxic'
   Document:
   """
   {text}
   """
   Label:
   '''
   
   prompt4 = '''
   Classify the Twitter Comment as "toxic" or "non-toxic". Only reply with the label.
   
   Document 1:
   """
   It's good to let kids get some exposure to manufacturing at the high school level.
   """
   Label: "Non-toxic"
   
   Document 2:
   """
   Anyone who knows Alex will find this ridiculous. I wonder why this people are not telling the truth. Fxxk you.
   """
   Label: "Toxic"
   
   Document 3:
   """
   {text}
   """
   Label: "
   '''
   
   p_list = [prompt1,prompt2,prompt3,prompt4]
   return p_list

def test_step_flip(model_name,p_list,ids,contents):
   Res_List = [30, 40, 54, 80, 89, 185, 432, 446, 522, 541, 553, 616, 706, 734, 751, 777, 807, 916, 941, 959]
   Impro_List = [48, 74, 129, 130, 134, 203, 212, 224, 248, 263, 267, 270, 271, 276, 368, 372, 435, 445, 476, 
                 483, 491, 502, 511, 513, 516, 525, 532, 559, 563, 580, 581, 607, 615, 623, 631, 639, 640, 643,
                 653, 669, 685, 693, 704, 714, 715, 722, 732, 763, 765, 774, 783, 785, 832, 881, 923, 935, 939, 948, 949, 971, 979]
   Unfilp_List = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 32, 33, 35, 36, 37, 38, 
                   39, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                   71, 72, 73, 75, 76, 77, 78, 79, 81, 82, 83, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95]
   List = [Res_List,Impro_List,Unfilp_List]
   file_name = ["__Res","__Imp","__Unf"]
   
   t=0.7
   for k in range(len(List)):
      sub_list = List[k]
      sub_name = file_name[k]
      for i in range(len(p_list)):
         txt_name = "./Twitter_0.7_test/"+model_name+sub_name+str(i+1)+".txt"
         p = p_list[i]
         print("Now test ",model_name," with prompt ",str(i+1))
         with open(txt_name,"w") as o:
            for y in range(len(sub_list)):
               index = sub_list[y]
               for j in range(20):
               # print("Now "+str(j+1)+" Test")
                  content = contents[index]
                  first_line = ids[index]
                  response = model_t(content,model_name,p,t)
                  print(str(first_line)+ "\t" + response)
                  o.write(str(first_line)+"\t"+response+"\n")

def test_step(model_name,p_list,ids,contents):
   t = 0
   for i in range(1):
      txt_name = "./Twitter_Results/"+model_name+"__"+str(i+1)+".txt"
      p = p_list[i]
      print("Now test ",model_name," with prompt ",str(i+1))
      with open(txt_name,"w") as o:
         for i in range(len(contents)):
            first_line = ids[i]
            content = contents[i]
            response = model_t(content,model_name,p,t)
            print(str(first_line)+ "\t" + response)
            o.write(str(first_line)+"\t"+response+"\n")

      
       
def main():
   #Initialization
   ids, target, contents = Tw_dataloader.read_csv("/home/wmaag/SR/Dataset/train.csv")
      
   print("Total dataset",len(contents))
 
   p_list = get_plist()
   model_list = ["gpt-3.5-turbo-instruct","gpt-3.5-turbo-0613","gpt-3.5-turbo-0301","text-davinci-003","text-davinci-002"]
   
   for i in range(len(model_list)):
      test_step(model_list[i],p_list,ids,contents)
      test_step_flip(model_list[i],p_list,ids,contents)
   
   print("finish")
   
if __name__ == "__main__":
    main()