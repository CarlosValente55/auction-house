import re,os, logging
class TextOperator:
    def __init__(self):
        self.file_path = os.path.abspath(os.getcwd()+'/data')
        self.input_file = "/input.txt"
        self.output_file = "/output.txt"
        self.read_file = open(self.file_path+self.input_file, "r")
        self.write_file= open(self.file_path+self.output_file, "w")
    def read_lines(self):
        while True:
            line = re.sub('\|',' ',self.read_file.readline())
            line=line.split()
            if not line:
                break
            yield line

    def write_line(self,auction):
        line=""
        for field in auction:
            if auction[field] is not None:
                line=line+str(auction[field])+"|"
        self.write_file.write(line[:-1]+"\n")

logging.basicConfig(
    format='%(asctime)s::%(levelname)s-%(message)s')
logging.getLogger().setLevel(logging.INFO)

def logger(instruction):
    if len(instruction)==6:
        logging.info('[SELL] timestamp:{}-> Received from user {} with reserve value of {}.'.format(instruction[0],instruction[1],instruction[4]))
    elif len(instruction)==5:
        logging.info('[BID] timestamp:{}-> Received from user {} with the value of {}.'.format(instruction[0],instruction[1],instruction[4]))
    elif len(instruction)==1:
        logging.info('[Heart] timestamp:{}'.format(instruction[0]))