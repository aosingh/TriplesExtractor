import subprocess
import os
from configuration.properties import SYNTAXNET_DIRECTORY


class TreeConstructor:

    @staticmethod
    def callSyntaxNetShell(sentence, path):
        os.chdir(SYNTAXNET_DIRECTORY)
        filePath = path+"/temp.txt"
        print filePath
        shellCommand = "echo "+sentence+"| syntaxnet/demo.sh >"+filePath
        subprocess.call([shellCommand], shell = True)
        return filePath