
# WR2MDX: Generate MDD/MDX mdict Dictionary from WordReference

This project allows you to generate MDD/MDX dictionary files from [wordreference.com](https://wordreference.com) using a script developed by Wissam. You can find the original post and more details about the script [here](https://forum.freemdict.com/t/topic/24867).

## Getting Started

Follow the steps below to set up the project and generate your own dictionary files.

### 1. Dependencies

Install the required Python libraries using `pip`:

```bash
pip install requests bs4 mdict-utils
```

### 2. Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/anatolepain/wr2mdx.git
cd wr2mdx
```

### 3. Obtain a Word List

You need to provide a word list for the dictionary. You can find word lists online by searching or generating your own. Different lists are available for various languages.

### 4. Create a Dictionary and Download Audio Files

Use the `wr-scraper.py` script to create a `.txt` dictionary file that can later be exported to MDX format. You can also download audio files for the dictionary.

#### Get Help

Run the following command to see usage instructions:

```bash
python3 wr-scraper.py -h
```

```bash
usage: wr-scraper.py [-h] [-l] [-a SOUND_DIRECTORY] DICTIONARY_CODE wordlist outputfile

Retrieve translations from wordreference.com.

positional arguments:
  DICTIONARY_CODE       Dictionary code (use `-l` to list available dictionaries).
  wordlist              The word list file to translate.
  outputfile            Output file for the translated dictionary.

optional arguments:
  -h, --help            Show this help message and exit.
  -l, --list-available-dictionaries
                        List available dictionaries and their codes.
  -a SOUND_DIRECTORY, --audio SOUND_DIRECTORY
                        Directory to download audio files.
```

#### Example

In this example, we create an English-to-French MDX dictionary with audio files using the `word-list.txt`:

```bash
python3 wr-scraper.py enfr -a ./mdd/sound word-list.txt mdx/wordreference.mdx.txt
```

> **Note:** The WordReference website might show a captcha after scraping a large number of words (between 1,500 and 2,000). The script will prompt you to solve the captcha before continuing.

### 5. Create MDD and MDX Files

#### MDX

```bash
mdict --title ./mdx/wordreference.mdx.title.html --description ./mdx/wordreference.mdx.description.html -a ./mdx/wordreference.mdx.txt ./build/wordreference.mdx
```

You can customize the title and description by editing the files `./mdx/wordreference.mdx.title.html` and `./mdx/wordreference.mdx.description.html`.

Example:

```bash
cat ./mdx/wordreference.mdx.description.html
```
```html
<p>wordreference.com</p>
<p>English - French</p>
<hr>
<p style="color:red;text-align:center;">Compiled on September 05 2024</p>
```

```bash
cat ./mdx/wordreference.mdx.title.html
```
```html
WordReference English-French
```

#### MDD

```bash
mdict --title ./mdx/wordreference.mdx.title.html --description ./mdx/wordreference.mdx.description.html -a mdd/ ./build/wordreference.mdd
```

### 6. Build Output

In the `./build/` directory, you will find everything needed to import into your mdict app: MDD and MDX files, along with a CSS and PNG file.
