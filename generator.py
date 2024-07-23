import os,sys

from generators.dart import Generator as dart

import utils
#utils.copy(generator_root,program_root,"dart");
def generate(generator_root,program_root):
    input_dir=program_root+"/input/"
    input_files=os.listdir(input_dir)
    program_config=0
    data={}
    with open(program_root+"/.config") as f:
        program_config=eval(f.read())
    for a in input_files:
        b=a.split(".")[0]
        with open(input_dir+a) as f:
            data[b]=eval(f.read())

    for class_name in data.keys():
        dart.generate(class_name,data,program_config,program_root)
