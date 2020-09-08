# Streamlit Vega-Lite

Making Vega-Lite selection created by user interactions available in Python.

## Dev Setup

Open two terminals in the dev container using VSCode's [Remote Containers Extension](https://code.visualstudio.com/docs/remote/containers).

In the first terminal, run:

```bash
# Install python module in editable mode
pip install -e .

# Launch streamlit app
streamlit run streamlit-vega-lite/__init__.py
```

In the second terminal:

```bash
# Switch to location of frontend code
cd streamlit-vega-lite/frontend
# Install dependencies
yarn
# Launch frontend assets
yarn start
```

Then open http://localhost:8501/.
