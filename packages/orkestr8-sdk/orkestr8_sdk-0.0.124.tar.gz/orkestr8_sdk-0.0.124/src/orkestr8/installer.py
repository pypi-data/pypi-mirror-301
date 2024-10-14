"""
Installs ML package on the machine by unzipping file and installing
"""
import logging
import os
import subprocess

logger = logging.getLogger()


def install():
    with open("log.txt", "w") as f:
        logger.info("Installing foodenie_ml..")
        print("DEBUG", os.listdir("."), sep="\n")
        subprocess.run(["tar -xvzf ~/foodenie_ml.tar.gz"], stdout=f)
        subprocess.run(
            [
                "cd foodenie_ml && python3 pip install -r requirements.txt && rm ../foodenie_ml.tar.gz"
            ],
            shell=True,
            stdout=f,
        )
