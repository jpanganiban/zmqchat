from setuptools import setup


install_requires = [
    'gevent',
    'gevent_zeromq',
]


setup(name="zmqchat",
      install_requires=install_requires)
