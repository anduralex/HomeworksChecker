import subprocess
import sys
import os

class RunPyCode(object):

    def __init__(self, code=None):
        self.code = code
        if not os.path.exists('classroom/running'):
            os.mkdir('classroom/running')

    def _run_py_prog(self, cmd="classroom/running/a.py"):
        cmd = [sys.executable, cmd]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.wait()
        a, b = p.communicate()
        self.stdout, self.stderr = a.decode("utf-8"), b.decode("utf-8")
        return result

    def run_py_code(self, code=None):
        filename = "classroom/running/a.py"
        if not code:
            code = self.code
        with open(filename, "w") as f:
            f.write(code)
        self._run_py_prog(filename)
        return self.stderr, self.stdout
