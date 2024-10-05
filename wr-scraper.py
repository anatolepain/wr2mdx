#!/usr/bin/env python

import argparse
import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.wordreference.com"

wr_available_dictinoaries = (
("enar" , "English-Arabic"),
("enzh" , "English-Chinese"),
("encz" , "English-Czech"),
("ennl" , "English-Dutch"),
("enfr" , "English-French"),
("ende" , "English-German"),
("engr" , "English-Greek"),
("enis" , "English-Icelandic"),
("enit" , "English-Italian"),
("enja" , "English-Japanese"),
("enko" , "English-Korean"),
("enpl" , "English-Polish"),
("enpt" , "English-Portuguese"),
("enro" , "English-Romanian"),
("enru" , "English-Russian"),
("enes" , "English-Spanish"),
("ensv" , "English-Swedish"),
("entr" , "English-Turkish"),
("aren" , "Arabic-English"),
("czen" , "Czech-English"),
("deen" , "German-English"),
("dees" , "German-Spanish"),
("esde" , "Spanish-German"),
("esen" , "Spanish-English"),
("esfr" , "Spanish-French"),
("esit" , "Spanish-Italian"),
("espt" , "Spanish-Portuguese"),
("fren" , "French-English"),
("fres" , "French-Spanish"),
("gren" , "Greek-English"),
("isen" , "Icelandic-English"),
("iten" , "Italian-English"),
("ites" , "Italian-Spanish"),
("jaen" , "Japanese-English"),
("koen" , "Korean-English"),
("nlen" , "Dutch-English"),
("plen" , "Polish-English"),
("pten" , "Portuguese-English"),
("ptes" , "Portuguese-Spanish"),
("roen" , "Romanian-English"),
("ruen" , "Russian-English"),
("sven" , "Swedish-English"),
("tren" , "Turkish-English"),
("zhen" , "Chinese-English"))

def print_available_dictinaries():
    print('code  :  Dictionary\n-------------------')
    for dict in wr_available_dictinoaries:
        print(dict[0]," : ", dict[1])

def define_word(word,dict_code):
    captcha=False
    page = requests.get(URL+ '/' + dict_code + '/' + word)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("tr", {'class':['even', 'odd']})
    if (soup.find_all("div", {'id':'WarnNote'})):
        return ([],[],captcha)
    bad_rows = []

    if (soup.find_all("div", {'class':'g-recaptcha'})):
        captcha=True
        return ([],[],captcha)

    for row_number in range(len(results)):
        if "more" in results[row_number]['class']:
            bad_rows.append(row_number)

    for row_number in reversed(bad_rows):
        del results[row_number]

    translations = {}
    translation_number = 0
    example = []

    for row in results:
        if (row.find(class_="FrWrd")):
            if example: translation["examples"].append(example)
            if translation_number > 0: translations[translation_number] = translation
            translation_number += 1
            example = []
            translation = {"word" : "",
                "definition" : "",
                "meanings" : [],
                "examples" : []
                }
            translation["word"] = row.td.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["definition"] = row.td.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["meanings"].append(row.td.next_sibling.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        elif (row.find(class_="ToWrd")):
            to2 = ''
            if (row.find(class_="To2")):
                to2 = row.td.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'')
            translation["meanings"].append(row.td.next_sibling.next_sibling.get_text().strip().replace('⇒','').replace(u'\xa0', u' ').replace(u'\u24d8', u'') + to2)
        elif(row.find(class_="FrEx")):
            if example:
                translation["examples"].append(example)
            example = []
            example.append(row.td.next_sibling.get_text().strip().replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        elif(row.find(class_="ToEx")):
            example.append(row.td.next_sibling.get_text().strip().replace(u'\xa0', u' ').replace(u'\u24d8', u''))
        else:
            pass
    if example:
        translation["examples"].append(example)
    if translation_number > 0:
            translations[translation_number] = translation
    
    try:
        audio_links = soup.find("div",id = "listen_widget").script.string[18:-3].split(',')
        audio_links = [URL + link[1:-1] for link in audio_links]
    except:
        audio_links = []
        
    result = (translations, audio_links, captcha)
    return result

class list_dict_codes(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        return super().__init__(option_strings, dest, nargs=0, default=argparse.SUPPRESS, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string, **kwargs):
        print_available_dictinaries()
        parser.exit()

def print_translations(translations, colors=""):
    tr=''
    for value in translations.values():
        tr+= '<hr><div><span class="word">' + value['word'] + ': </span><span class="def">' + value['definition'] + "</span></div>"
        for meaning in value["meanings"]:
            tr+= '\n' + '<div class="meaning">' + meaning + "</div>"
        for examples_list in value["examples"]:
            for example in range(len(examples_list)):
                if not example:
                    tr+= '\n' '<div class="example">' + examples_list[example] + "</div>"
                else:
                    tr+= '\n' + '<div class="example_translation">' + examples_list[example] + "</div>"
        tr+= '\n'
    return tr

def download_audio(word, links, audio_path):
    audio_file_names=[]
    for audio_link in links:
        lang=audio_link.rsplit('/', 2)[1]
        path=audio_path+ word + '-' + lang + '.mp3'
        if os.path.exists(path):
            audio_file_names.append((word + '-' + lang + '.mp3',lang))
        else:
            file = requests.get(audio_link)
            if file.status_code == 200:    
                audio_file_names.append((word + '-' + lang + '.mp3',lang))
                open(path, 'wb').write(file.content)
    return audio_file_names

def parse_arguments():
    parser = argparse.ArgumentParser(description="get translation from wordreference.com ")
    parser.add_argument("dictionary_code", help = "dictionary code, use -l to list a list of available dictionaries", choices = ["enar","enzh","encz","ennl","enfr","ende","engr","enis","enit","enja","enko","enpl","enpt","enro","enru","enes","ensv","entr","aren","czen","deen","dees","esde","esen","esfr","esit","espt","fren","fres","gren","isen","iten","ites","jaen","koen","nlen","plen","pten","ptes","roen","ruen","sven","tren","zhen"], metavar ="DICTIONARY_CODE")
    parser.add_argument("-l", "--list-available-dictionaries", help = " list available dictionaries and their codes", action = list_dict_codes)
    parser.add_argument("-a", "--audio", help = "directory to download audio files", metavar="SOUND_DIRECTORY")
    parser.add_argument("wordlist", help = "wordlist file to translate")
    parser.add_argument("outputfile", help = "output dictionary file to translte later to mdx")
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    with open(args.wordlist) as words_file:
        for line in words_file:
            content= line.rstrip() + '\n' + '<link rel="stylesheet" type="text/css" href="wordreference.css" />' + '\n' + '<div class="headword">' + line.rstrip() + "</div>" +'\n'
            while True:
                print(line.rstrip())
                translations,audio_links,captcha = define_word(line.rstrip(), args.dictionary_code)
                if captcha:
                    inp = input("\nPlease go to wordreference.com and solve the captcha then press any key to continue\n")
                    break

                if translations:
                    if args.audio:
                        audio_files=download_audio(line.rstrip(), audio_links, args.audio)
                        if audio_files:
                            content+="<hr>"
                            for audio_file in audio_files:
                                content+= '<a href="sound://sound/'+ audio_file[0] + '">' + ' ' + audio_file[1] + ' ' + '<img class="spkr" src="img/spkr.png"></a> &nbsp;\n'

                        
                    content+= print_translations(translations) + '</>' + '\n'
                    with open(args.outputfile, "a") as myfile:
                        myfile.write(content)
                    break
                else:
                    print(line.rstrip() + ": word not found")
                    with open("errors.txt", "a") as myfile:
                        myfile.write(line.rstrip() + '\n')
                    break
    
if __name__ == '__main__':
    main()
