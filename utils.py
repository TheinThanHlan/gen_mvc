import os,config
def copyData(generator_root,project_root,lang,name):
    os.popen("cp "+generator_root+"/generators/"+config.lang.get(lang).get("postfix")+"/data/* "+project_root+"/"+name+"/lib/ -fr")

def copyInputTemplate(generator_root,project_root,lang):
    os.popen("cp "+generator_root+"/input "+project_root+" -fr")

