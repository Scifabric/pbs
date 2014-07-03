from setuptools import setup

setup(
    name="pbs",
    version="1.0",
    py_modules=['pbs'],
    install_requires=['Click', 'pybossa-client', 'requests', 'nose', 'mock', 'coverage',
                      'rednose'],
    entry_points='''
        [console_scripts]
        pbs=pbs:cli
    '''
)
