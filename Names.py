
# coding: utf-8
from typing import List
from random import choice, randint

def make_name() -> str:
    if randint(0,1):
        return (choice(given_names_female) + ' ' + choice(surnames)).strip()
    if randint(0,len(given_names)) < len(unknown):
        return choice(unknown)
    if randint(0,len(given_names)) < len(only_names):
        return choice(only_names)
    return (choice(given_names) + ' ' + choice(surnames)).strip()

def try_add_names(components, min_split_index, max_split_index, all_female=False):
    if min_split_index == max_split_index:
        individual_given_names.update(components[:max_split_index])
        if ' '.join(components[:max_split_index]) in [' ', '']:
            print(components)
        if all_female:
            given_names_female.add(' '.join(components[:max_split_index]))
        else:
            given_names.add(' '.join(components[:max_split_index]))
        surnames.add(' '.join(components[max_split_index:]))
        return True
    return False

def process_name(name : str, all_female : bool = False) -> List[str]:
    components = name.split(' ')
    if len(components) == 1:
        only_names.add(components[0])
        return
    min_split_index = 1
    max_split_index = len(components) - 1
    if try_add_names(components, min_split_index,max_split_index, all_female): return
    for index, c in enumerate(components[1:],1):
        if c[0].islower() or c in ['Le', 'La', 'De', 'Di', 'Van', 'Della', 'Del', 'St.']:
            split_index = index
            if c in ['i', 'y']:
                split_index -= 1
            min_split_index = split_index
            max_split_index = split_index
            break
    if try_add_names(components, min_split_index,max_split_index, all_female): return
    if ' '.join(components[min_split_index:]) in surnames:
        max_split_index = min_split_index
    if try_add_names(components, min_split_index,max_split_index, all_female): return
    for index, c in enumerate(components[:max_split_index]):
        if (c.isupper() or
            c in individual_given_names or
            any(c.endswith(x) for x in ['slav','ich','ych'])):
            min_split_index = max(index + 1, min_split_index)
    if try_add_names(components, min_split_index,max_split_index, all_female): return
    roman_numerals = 'IVXLCDM'
    if (components[-1] in ['Jr.', 'Sr.'] or
        set(components[-1]).issubset(set(roman_numerals)) or
        set(components[-1]).issubset(set(roman_numerals.lower()))):
        max_split_index = min(len(components)-2, max_split_index)
    if try_add_names(components, min_split_index,max_split_index, all_female): return
    unknown.append(name)

individual_given_names = set([
    'Friedrich','Christoph','Xaver','Giacinta','Martino','Battista','Ludwig',
    'Frideric', 'Gottlieb', 'Marcy', 'Philip', 'Modeste', 'Theresia', 'Ira', 'Andreas',
    'Joseph', 'Jacinto', 'Manuel', 'Valentin', 'Ryan', 'Augustus', 'Fredrik', 'Michele',
    'Lena', 'Magnus', 'Frederik', 'Agata', 'Hieronymus', 'Amadeus', 'Moreno',
    'Nicolaus', 'Ivar', 'Georg', 'Ottavio', 'Uwe', 'Lorenzo', 'Heinrich','Friedemann',
    'Nikolaus', 'María', 'Edward', 'Bernardo', 'Wilhelm', 'Lee', 'Siegemund', 'Alonso',
    'Gregory', 'Feliks', 'Teresa', 'Francesco', 'Matteo', 'Baptista', 'Bernhard',
    'Nepomuk', 'Federico', 'Casimir', 'Maria', 'Bill', 'Aemilius', 'Gottlob', 'Matthias',
    'Gotifredo', 'Albert', 'Bautista', 'Willard', 'Orlando', 'Allison', 'Rodney', 'Hubert',
    'Barbara', 'Adolfo', 'Cecil', 'Nicola', 'Cesare', 'Theresa', 'Theophil', 'Baptiste',
    'Laurence', 'Octavian', 'Bernardino', 'Sigismund', 'Benedicta', 'Willibald', 'Henrik',
    'Baptist', 'Margarita', 'Cattarina', 'Désiré', 'Christian', 'Lorenz', 'Margaret',
    'Rudolph', 'Niclas', 'Stefan', 'Leslie', 'Benedetto', 'Ignác', 'Beatrice', 'Joanne',
    'Catlin', 'Hayden', 'Bartosch', 'Lucy', 'Stuart', 'Emily'])
given_names = set()
given_names_female = set()
surnames = set(['Lloyd Webber', 'Vaughan Williams'])
only_names = set()
unknown = []
with open("composers-raw.txt",encoding='utf8') as f:
    composers_raw = f.read().split('\n')
for name in composers_raw:
    process_name(name)
with open("composers-f-raw.txt",encoding='utf8') as f:
    composers_raw = f.read().split('\n')
for name in composers_raw:
    process_name(name, True)
given_names = list(given_names)
given_names_female = list(given_names_female)
surnames = list(surnames)
only_names = list(only_names)

len(given_names_female)
