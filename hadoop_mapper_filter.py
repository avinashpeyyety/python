import sys
import csv

reader=csv.reader(sys.stdin,delimiter='\t')
writer=csv.writer(sys.stdout,delimiter='\t',quotechar='"', quoting=csv.QUOTE_ALL)
        
def mapper():
    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for line in reader:
        flag=0;
        for el in line:
            for s in ['.','?','!']:
                if s in el and el != line[len(line)-1]: flag+=1
        if flag== 0:  
           writer.writerow(line) 

test_text="""\"\"\t\"cats and dogs!\"\t\"\"
\"\"\t\"cats and rats!\"
\"\"\t\"bats and rats.\"\t"\"\"
\"\"\t\"cats and cows?\"\t\"\"
"""

def main():
    import StringIO
    sys.stdin = StringIO.StringIO(test_text)
    mapper()
    sys.stdin = sys.__stdin__

if __name__ == "__main__":
    main()
    
