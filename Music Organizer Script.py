import shutil
import os
import mutagen
import re

errors = []

def fixFolderNames(s):
    s = s.strip()
    snew = ""
    for character in s: # iteration only for each character, and no embedded iteration anywhere in the loop body
        if not re.match(r"[/\\:*?\"<>|]", character):
            snew += character
    return snew

def sendToDirectory(metadata): # 0:artist, 1:album, 2:title, 3:name
    here = os.path.dirname(os.path.abspath(__file__)) + '/' 
    artistdir = here + fixFolderNames(metadata[0]) + '/'
    albumdir = artistdir + fixFolderNames(metadata[1]) + '/'
    name = metadata[3]

    print("Sending ", name, " to ", albumdir, "...", sep = "")

    # If any directory doesn't exist, create it
    if not os.path.isdir(artistdir):
        os.mkdir(artistdir)
    if not os.path.isdir(albumdir):
        os.mkdir(albumdir)
        
    try:
        if os.path.exists(here + name): # There's an mp3 file in the source folder of this file
            if os.path.exists(albumdir + name): # There's a like-named mp3 file in the appropriate location. Deleting it!
                os.remove(albumdir + name)
            shutil.move(name, albumdir)
    except:
        print("PROBLEM WITH MOVING", name)

def processMetadata(name):
    mutfile = mutagen.File(os.listdir()[i])
    found = 0
    album = None #keys["TALB"]
    title = None #keys["TIT2"]
    artist = None #keys["TPE1"]
    print(name)
    for key in mutfile.keys():
        if (key == "TALB"):
            album = mutfile[key].text[0]
        elif (key == "TIT2"):
            title = mutfile[key].text[0]
        elif (key == "TPE1"):
            artist = mutfile[key].text[0]
    metadata = [artist, album, title, name]
    if (album == None or title == None or artist == None):
        errors.append((name, metadata))
        raise Exception("file is missing TALB, TIT2, and/or TPEI")
    print("\t", metadata[0:3], sep = "")
    print()
    #print('o ', end="")
    return metadata

def output(counter, directory):
    print('\n','\n','\n','\n','\n','\n','\n')
    print("Done.", counter, "files parsed of", len(directory))
    print(len(errors), "audio files lacked metadata (filename, metadata found):")
    for error in sorted(errors, key=lambda x: x[0]):
        print('\t', error)

if __name__== "__main__":
    print("Running...")
    counter = 0
    directory = os.listdir()
    metadatalist = []
    for i in range(len(directory)):
        try:
            metadata = processMetadata(directory[i])
            metadatalist.append(metadata)
            counter += 1
        except Exception as e:
            print("\t", "[EXCEPTION] Can't process because ", e, '\n', sep="")
            #print('x ', end="")
    for m in metadatalist:
        sendToDirectory(m)
    output(counter, directory)
    
