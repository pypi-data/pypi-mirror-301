from setuptools import setup
setup(
    name="CH347",
    version="1.0.1",
    author="Enbuging",
    author_email="electricfan@yeah.net",
    license="MIT",
    description="A wrapper for CH347DLL.DLL, which can be used to access SPI, JTAG, I2C, UARTs and GPIOs on CH347.",
    keywords=["hardware","interface","CH347","CH347DLL.DLL","CH347DLLA64.DLL"],
    packages=["ch347"]
)