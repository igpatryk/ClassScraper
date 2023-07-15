# ClassScraper

ClassScraper is a Python script able to scrape specific ClassMarker.com tests.

## Why

Had to scrape 200+ questions and answers so I chose to write an automation.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)

## Limitations

Currently, ClassScraper is able to scrape tests structured like this [test](https://www.classmarker.com/online-test/start/?quiz=6vd64b29e00df906):
* has instruction (pre-test guideliness or pre-test custom instructions)
* no password/access list
* no price
* no user info required
* no intro questions
* 1 question per page
* question grading and feedback during test + reveal correct answer during test option enabled
* only multiple choice questions with one correct answer and radio buttons (not checkboxes)

Please feel free to open pull requests and issues if you would like ClassScraper to support more scenarios.
## Usage

### Configuration

Before running automation, open `app-variables.env` file and fill in your preferences:
* `debug`:
   - `y` to enable debug logs, any other value to keep `INFO` minimal log level
* `url`:
   - your test's URL, example: `https://www.classmarker.com/online-test/start/?quiz=6vd64b29e00df906`
* `all_answers`:
   - `y` to scrape wrong and correct answers, any other value to scrape only correct answers
### Running automation
To run scrapping automation, simply run `run.sh` bash script.

```bash
./run.sh
```

Follow script output for details. Scrapped test will be saved in `output.txt` file on your local machine. If automation fails, script will save logs to `logs.txt` file on your local machine instead.

### Output format

With `all_answers` option set to `y`, output.txt file will look like this:
```
1. First question
WRONG: wrong answer
WRONG: wrong asnwer
RIGHT: correct answer
WRONG: wrong answer
2. Second question
WRONG: wrong answer
RIGHT: correct asnwer
WRONG: wrong answer
WRONG: wrong answer

and so on.
```

Without `all_answers` option enabled, output.txt file will look like this:
```
1. First question
correct answer
2. Second question
correct answer

and so on.
```
## Contributing

Please feel free to open pull requests and issues.