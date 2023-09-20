# 🔍 MyRetriver 🔍

![logo](images/icon.png)

Query Magic: the Gathering cards according to a specific prompts

## How to install:

1. Install from source:

```
git clone https://github.com/chumpblocckami/myretriver
pip install -r requirements.txt
streamlit run app.py
```

2. Docker:

``` 
   docker build -f Dockerfile . -t myretriver 
   docker run -v ./cards:./cards -p 8080 myretriver
```

3. From website:
   Go to [www.streamlit.com/myretriver](https://myretriver.streamlit.app/)

### NB: It needs a valid OPENAI_API_KEY
