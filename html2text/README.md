A tool for extracting text from HTML. Given a URL it extracts the text part,
removing <script> and <style> elements, stripping empty spaces and lines,
and excluding those string that are part of the template (headers, footers,
navigation elements, ...).

-----

Install requirements in a dedicated virtual environment:

```
pip install -r requirements.txt
```

Run the script providing a URL:

```
python html2text.py [URL]
```

