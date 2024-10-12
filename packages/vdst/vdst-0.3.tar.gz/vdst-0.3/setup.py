from setuptools import setup , find_packages

setup(name='vdst',
      version='0.3',
      packages=find_packages(),
      entry_points={
          'console_scripts':[
              'create-data-science=vdst.template:create_vdst'
          ]
      },
      description='A python package for data-science project templates',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Vansh Khatri',
      author_email='khatrivansh43@gmail.com',
      url='https://github.com/vanshxo/vdst',
      license='MIT'

      )