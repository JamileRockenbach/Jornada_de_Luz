import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icone2.ico") ]
cx_Freeze.setup(
    name = "A Jornada de Luz",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["recursos"]
        }
    }, executables = executaveis
)
