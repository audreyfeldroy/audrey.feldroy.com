# JSON to SQLite With sqlite-utils

How to get JSON into a local SQLite database fast.

## Background

Last year I downloaded and read the sqlite-utils docs as an .epub file to read like a book on the Eurostar from Paris to London. It was then that I discovered the amazing command-line side of sqlite-utils. It's powerful and I'm only scratching the surface of what can be done with it.

## Create or Download the JSON

To start, I had Grok 3 generate a list of Filipino languages in JSON. I saved it as langs.json. I had it include an integer primary key. (I also tried Claude 3.7, Deepseek, Gemini 2.5 Pro, ChatGPT 4.5. Grok 3 gave me the longest list, though quite incorrect.)

## Import With sqlite-utils

I like to use the sqlite-utils CLI tool as a uvx tool, giving it its own isolated environment. This one-liner turns the JSON into a SQLite database:

```sh
uvx sqlite-utils insert langs.db langs langs.json --pk=id
```

* `langs.db` is the database filename
* `langs` is the table name I want for the data
* `langs.json` is the file containing the data to import, which I created earlier.

## Check It

```sh
uvx datasette langs.db
```

Then go to http://127.0.0.1:8001/langs/langs and you should see all the entries in a nicely-browsable table.
