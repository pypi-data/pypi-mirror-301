"""
Installs ML package on the machine by unzipping file and installing
"""

import subprocess


def install():
    with "log.txt" as f:
        subprocess.run(["tar -xvzf foodenie_ml.tar.gz"], stdout=f)
        subprocess.run(
            [
                "cd foodenie_ml && python3 pip install -r requirements.txt && rm ../foodenie_ml.tar.gz"
            ],
            shell=True,
            stdout=f,
        )
