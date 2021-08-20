from os.path import exists
from os import mkdir, popen, walk
from random import randrange as rr
from shutil import rmtree
import requests as rq

#common variables
url_apktool = 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.5.0.jar'
url_dex2jar = ''
name_storage = 'playwithapk'
out_storage = f'{name_storage}/out/'
util_storage = f'{name_storage}/util/'
target_storage = f'{name_storage}/target/'

#Make folder on start
if not exists('playwithapk'):
    mkdir(name_storage)
    mkdir(out_storage)
    mkdir(util_storage)
    mkdir(target_storage)
    print('[i] Created program storage since the storage was not detected.')

#Lazy command display
def disp(strcmd):
    print('-'*100)
    print(popen(strcmd).read())
    print('-'*100)

#Menu -> Download utils
def download():
    try:
        print('[i] Downloading apktool...')
        bintemp = rq.get(url_apktool).content
    except:
        print('[i] Internet error, aborted.')
    
    open(f'{util_storage}apktool.jar', 'wb').write(bintemp)
    print('[i] OK...')


#Menu -> Decompile
def decom():
    targets = next(walk(target_storage), (None, None, []))[2]
    
    if len(targets) == 0:
        print("[e] No apk exist.")
    else:
        for i in range(len(targets)):
            #add range options here
            require = input(f'For {targets[i]} ,Decompile? (a)ll/(r)esrc/(s)rc: ')
            srcapk = f'{target_storage}{targets[i]}'
            out = f'{out_storage}{targets[i]}'
            print(f'[i] Decompiling "{targets[i]}"...')
            if require == 'a':
                disp(f'java -jar {util_storage}apktool.jar d "{srcapk}" -o "{out}"')
            elif require == 'r':
                disp(f'java -jar {util_storage}apktool.jar d "{srcapk}" -o "{out}" -s')
            elif require == 's':
                disp(f'java -jar {util_storage}apktool.jar d "{srcapk}" -o "{out}" -r')
            else:
                print('[e] Invalid command, skipped.')

#Menu -> Recompile
def recom():
    targets = next(walk(out_storage), (None, None, []))[2]
    retarget = input('Specify folder name (*=all): ')
    if retarget == '*':
        for i in range(len(targets)):
            print(f'[i] Recompiling {targets[i]}...')
            disp(f'java -jar {util_storage}apktool.jar b "{out_storage}{targets[i]}"')
    else:
        try:
            print(f'[i] Recompiling {retarget}...')
            disp(f'java -jar {util_storage}apktool.jar b "{out_storage}{retarget}"')
            print('[i] Built apk can be found in the "dist" folder')
        except:
            print("[e] Invalid name.")
#Menu -> hack -> replace all strings
def rep_str():
    pass

#clean
def clean():
    deltarget = input('Specify folder name (*=all): ')
    if deltarget == '*':
        print("[i] Removing... Please don't stop this script until I say done...")
        rmtree(out_storage)
        mkdir(out_storage)
        print("[i] Done")
    else:
        try:
            print("[i] Removing... Please don't stop this script until I say done...")
            rmtree(f'{out_storage}{deltarget}')
            print("[i] Done")
        except:
            print("[e] Invalid name.")
            
def Tutorial():
    pass

def menu():
    print('\n\nWelcome to playwithapk\n[i] Make sure java environment is installed on this system.\n[i] To decompile, put your apks inside the "target" folder.\n\nOptions: ')
    print('0: Tutorial')
    print('1: Download utils (do it first if you first time run this script)')
    print('2: Decompile apk')
    print('3: Recompile apk')
    print('98: Clean output')
    print('99: Exit')
    option = int(input('Select your option (num): '))

    if option == 0:
        tutorial()
    elif option == 1:
        download()
    elif option == 2:
        decom()
    elif option == 3:
        recom()
    elif option == 98:
        clean()
    elif option == 99:
        exit()
    
    menu()

menu()
    
