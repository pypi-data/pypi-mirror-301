from setuptools import setup, find_packages

setup(
    author= "Dear Norathee",
    description="the extension of sklearn to help the your modeling code becomes more concise with common useful tool for modeling",
    name="modeling_tool",
    version="0.1.3rc2",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "scikit-learn",
        "lightgbm",
        "xgboost",
        "imblearn",
        "playsound"
        ],
    python_requires='>=3.10.0',
    extras_require={
        'torch': ['torch>=1.0']  # Optional torch dependency
    },
    # example
    # install_requires=['pandas>=1.0',
    # 'scipy==1.1',
    # 'matplotlib>=2.2.1,<3'],
    

)