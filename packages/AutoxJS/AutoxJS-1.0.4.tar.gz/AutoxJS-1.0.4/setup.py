# -*-coding:utf-8;-*-
from setuptools import setup

setup(
    name="AutoxJS",
    version="1.0.4",
    author="Enbuging",
    author_email="electricfan@yeah.net",
    license="MIT",
    description="Launch Auto.js and Autox.js scripts with Python in Termux.",
    keywords=["Auto.js", "Autox.js", "Termux", "Android", "automation"],
    package_data={
        "autojs": ["call_locator.js", "call_sensors.js", "execute_file.js", "execute_string.js"]
    },
    packages=["autojs"]
)
