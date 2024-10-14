"""
Installs ML package on the machine by unzipping file and installing
"""
import logging
import subprocess

logger = logging.getLogger()


def install():
    with open("log.txt", "w") as f:
        logger.info("Installing foodenie_ml..")
        subprocess.run(["tar -xvzf foodenie_ml.tar.gz"], shell=True, stdout=f)
        subprocess.run(
            [
                "cd foodenie_ml && python3 pip install -r requirements.txt && rm ../foodenie_ml.tar.gz"
            ],
            shell=True,
            stdout=f,
        )
