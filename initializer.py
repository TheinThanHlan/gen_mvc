import os,sys
import utils
def init(generator_root,program_root,lang):
    name=input("Name of the project : > ")
    config={"name":name,"lang":lang}
    with open(program_root+"/.config","w") as f:
        f.write(str(config));

    os.system("flutter create "+program_root+"/"+name)

    utils.copyData(generator_root,program_root,lang,name);
    utils.copyInputTemplate(generator_root,program_root,lang);


