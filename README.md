
# GEN_MVC

This is the tool to generate the MVC archatecutre for flutter.



## Features

- generate model
- generate dao
- generate database for sqlite
- generate controllers
- generate views


## Installation

clone my project

```bash
git clone https://TheinThanHlan@bitbucket.org/theinthanhlan/gen_mvc.git
```
___
Set permission for executable
```bash
cd gen_mvc
chmod +x gen_mvc
```
___

set path
```bash
x=pwd
export PATH=$PATH:$x
```

or

export path into your .bashrc

---



## Run

create a project directory and go there
```bash
mkdir test
cd test
```

Initialize the gen_mvc
```bash
gen_mvc i flutter

```
* create the files in input directories
* template.py is the example for input

generate the project

```bash
gen_mvc g
```


* the output files will be in output directory
* copy them into your flutter project






