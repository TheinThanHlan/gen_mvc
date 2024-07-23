import config
lang=" | ".join(config.lang.keys())

def printHelp():
    print(f"""gen_mvc [args]
    -i [lang]   - initialize the project
        [lang]  - {lang}

    -g  [lang]  - generate the source
        [lang]  - {lang}
    """)
