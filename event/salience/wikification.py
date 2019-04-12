import requests
import getpass
from urllib.parse import urlencode, quote, quote_plus
import json
import sys
import re
import logging


def call_tagme(in_file, out_path, freebase_map, token, username, password):
    url = 'https://tagme.d4science.org/tagme/tag'

    params = {
        'lang': 'en',
        'gcube-token': token,
        # 'gcube-token': '3ccca27e-d0a1-4752-a830-b906b7c089fa-843339462',
        'text': in_file.read()
    }

    r = requests.post(url, auth=(username, password), data=params)

    with open(out_path, 'w') as out:
        tagme_json = json.loads(r.text)
        for spot in tagme_json['annotations']:
            if 'title' in spot:
                wiki_title = get_wiki_name(spot['title'])
                fbid = freebase_map.get(wiki_title, None)
                if fbid:
                    spot['mid'] = fbid
        json.dump(tagme_json, out)
        out.write('\n')


def call_dbpedia(url, in_file, out_path, freebase_map):
    # url = 'http://localhost:2222/en/rest/annotate'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    file_offset = 0

    annotations = []

    for line in in_file:
        if line.strip() == "":
            file_offset += len(line)
            continue

        data = {
            'confidence': 0,
            'text': line,
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == 200:
            dbpedia_out = json.loads(r.text)
            for resource in dbpedia_out.get('Resources', []):
                keys = ['@offset', '@URI', '@surfaceForm']

                if any([key not in resource for key in keys]):
                    continue

                if any([resource[key] is None for key in keys]):
                    continue

                offset = int(resource['@offset']) + file_offset

                title = re.sub(r'http://(.*?)dbpedia.org/resource/', '',
                               resource['@URI'])

                fbid = freebase_map.get(title, None)

                annotation = {
                    'title': title,
                    'start': offset,
                    'end': len(resource['@surfaceForm']) + offset,
                    'link_probability': resource['@similarityScore'],
                    'spot': resource['@surfaceForm'],
                }

                if fbid:
                    annotation['mid'] = fbid
                annotations.append(annotation)
        else:
            pass

        file_offset += len(line)

    with open(out_path, 'w') as out:
        json.dump({'annotations': annotations}, out)
        out.write('\n')


def get_wiki_name(name):
    return name.title().replace(' ', '_')


def main(url, in_dir, out_dir, freebase_map_file, token):
    import os

    if not token == 'dbpedia':
        username = input('Username:')
        password = getpass.getpass('Password:')

    freebase_map = {}
    print("Reading freebase id.")
    with open(freebase_map_file) as infile:
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                mid, wiki_name = parts
                freebase_map[wiki_name] = mid
    print("Done.")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for fn in os.listdir(in_dir):
        if fn.endswith('.txt'):
            with open(os.path.join(in_dir, fn)) as infile:
                out_path = os.path.join(out_dir, fn + '.json')
                if token == 'dbpedia':
                    call_dbpedia(url, infile, out_path, freebase_map)
                else:
                    call_tagme(infile, out_path, freebase_map, token,
                               username, password)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
