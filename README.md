# Tunestarter 0.1.0

## What is tunestarter?
Have you ever been to a folk session and wanted to play a set of tunes, but you simply couldn't remember how they began?

Or have you ever started a set and forgotten how the second or third tune starts?

Or are you simply tired of carrying 15 different printouts of the same tune, all arranged in different sets?

Then Tunestarter is for you. Tunestarter creates tune-starting helpers containing the first few bars of each tune in a set. This means you have the beginning of each tune visible at first glance.

As a bonus, it also includes the entire tune in a second chapter, complete with cross-references, so you can jump to the full tune from the set. From the tune, you can see what sets you have included it in.


### How does it work?
The steps are simple but currently require some programming knowledge from the user (this will change in the future, remember that this is the pre-alpha).

You need to define your sets in a YAML file similar to the one below There are examples included in the directory named examples.

```
 name: "Example Tune Starter" <-- Name of the tune starter
 sets:
    - name: "Set des Monats 22-02" <-- Name of set. When not set, the names of the tunes are used
      tunes:
        - source: "thesession" <-- the source for the tune. Currently only thesession is supported
          id: 4 <-- ID of the tune, used for query to download ABC file
          setting: 3 <-- Setting is a specific version of the tune. If left out, setting 1 is used
        - source: "thesession"
          name: "Drowsy Maggie" <-- You can also specify a name of a tune. Then the search function of thesession.org is used. If you get wrong or no results, make sure to test the search terms on thesession.org to make sure that the term gives the tune you want
    - tunes:
        - source: "thesession"
          id: 5
          setting: 1
        - source: "thesession"
          id: 19
```

In this file, you simply list the sets one by one, writing the index and version of the tune you want to add to the set.

Tunestarter will use this information to download the ABC files, sort them, and create LaTeX files for each set and tune, based on a boilerplate.

Finally, it will generate a PDF file you can bring with you on your phone or tablet or print it (but please don't... think about the trees).

### Usage
```usage: tunestarter [-h] [--keeptmp] filepath

Create a tunestarter for your session

positional arguments:
  filepath    path to the tune starter yaml file

optional arguments:
  -h, --help  show this help message and exit
  --keeptmp   the tmp file will be kept after generation is done (good for debugging)
  ```

### config.yaml
Some user settings and storage settings are stored in the file `config.yaml`. Here you can set the storage directories, path for the database, and also the number of measures that should be included in the tune set starters.

Below you can see an example of a config.yaml file.
```
---
  # User settings
  # Number of measures to include in sets
  num_measures: 4

  # Storage settings
  tmp_dir: "./tmp"
  db: "./tunestarter.db"
  
  # Debug settings
  debug_mode: True
  pdflatex_output: "./pdflatex.log"
  ```

### Current limitations
- Only works with thesession.org.
- Only tested on mac.
- pdflatex with package abc
- No real testing, error handling, etc. Be prepared to get nasty errors if you do something wrong.

### Roadmap
- Include more sources than thesession.org
- Create some kind of UI so that it will be easier to add and handle sets
- Make the boilerplate configurable
- Make Tunestarter cross-platform
- Maybe set up a web service?

### Reporting bugs
Please report issues through the repository's issues tab. Include as much info as you can, and make sure to include the error message and an example YAML file that causes it.

##### Note about sjkabc
To handle the ABC files, I am using the library sjkabc. This is a library that is without a license but is available here: https://github.com/sjktje/sjkabc. It is also included in this repository under the directory sjkabc.

If you are the owner/author of this library and would like me to remove any references to it, please create an issue to let me know.