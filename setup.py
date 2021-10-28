import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("checkout.py", base=base)
]

buildOptions = dict(
        packages = ["PyQt5"],
        includes = [],
        include_files = ["Rockwell.ttc","650x5000px.png","31x41px PDF Ícon_Prancheta 1 (1).png","498x600px.png","795x233px.png","1000x1000px.png","1532-x-826px.png","2000x2000px.png","checkout.ui","Logo wild PRETA.png","menu_editar.ui","pdfsalvo.ui","registro.ui"],
        excludes = []
)




setup(
    name = "Checkout",
    version = "1.8",
    description = "checkout",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
