from setuptools import setup, find_packages, find_namespace_packages

setup(name = 'codegenai',
      version = '5.7',
      description = "AI Algorithms And Computer Network Related Code",
      author = 'Anonymus',
      package_data={'':['licence.txt', 'README.md', 'data\\**']},
      include_package_data = True,
      install_requires = ['networkx','matplotlib','tqdm','numpy','scipy','sklearn'],
      packages = find_namespace_packages(),
      zip_safe = False)