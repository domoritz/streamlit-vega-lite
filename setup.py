import setuptools

setuptools.setup(
    name="streamlit-vega-lite",
    version="0.0.3",
    author="Dominik Moritz, Cameron Yick",
    author_email="",
    description="A Vega-Lite Component for Streamlit that Supports Selections",
    long_description="",
    long_description_content_type="text/plain",
    url="https://github.com/domoritz/streamlit-vega-lite",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
