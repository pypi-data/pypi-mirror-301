from setuptools import setup

setup(name='thoro_barman_exporter',
      version='2.0.0',
      description='Fork of ahes Barman exporter for Prometheus',
      long_description='Fork of ahes Barman exporter for Prometheus. Full description at https://github.com/thoro/prometheus-barman-exporter',
      url='https://github.com/thoro/prometheus-barman-exporter',
      author='Thomas Rosenstein',
      author_email='thomas@thoro.at',
      license='MIT',
      packages=['barman_exporter'],
      keywords='prometheus barman exporter barman-exporter',
      entry_points={
          'console_scripts': ['barman-exporter=barman_exporter.barman_exporter:main'],
      },
      install_requires=[
          'prometheus-client',
          'sh'
      ],
      zip_safe=False)
