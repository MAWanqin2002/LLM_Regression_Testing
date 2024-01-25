import csv
import sys

def read_csv(csv_path):
    ids = []
    target = []
    contents = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        count = 0
        next(reader)
        for row in reader:
            if count > 999:
                break
            col1, col2, col3 = row[:3]
            ids.append(col1)
            target.append(col2)
            contents.append(col3)
            count +=1
    return ids, target, contents

def write_txt(ids,target,content):
    with open("./Twitter.txt",'w') as f:
        for i in range(len(ids)):
            num = float(target[i])
            if num > 0.5:
                t = "1 toxic"
            else:
                t = "0 non-toxic"
            f.write(str(ids[i])+"  "+t+"\n"
                    +content[i]+"\n\n")

if __name__ == "__main__":
    ids, target, contents = read_csv("./train.csv")
    # count = 0
    # for i in range(len(target)):
    #     num = float(target[i])
    #     if num > 0.5:
    #         count += 1
    
    # print(target)
    write_txt(ids,target,contents)