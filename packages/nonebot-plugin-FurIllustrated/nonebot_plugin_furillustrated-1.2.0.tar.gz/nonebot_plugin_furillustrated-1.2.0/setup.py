from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setup(name='nonebot-plugin-FurIllustrated',    # 包名
      version='1.2.0',        # 版本号
      description='兽云祭插件',
      long_description=long_description,
      author='huilongxiji',
      author_email='2601515849@qq.com',
      url='https://github.com/huilongxiji/nonebot-plugin-FurIllustrated',
      install_requires=['nonebot2>=2.2.1', 'httpx>=0.27.0', 'nonebot-adapter-onebot>=2.4.3'],
      license='MIT',
      packages=find_packages())
