
import json
import os
import hashlib
# import vlc

def fetchJson(jsonname):
    with open(str(jsonname) + ".json", "r") as jsonfile:
        jsondata = json.load(jsonfile)
        return jsondata

def writeJson(jsonname, jsondata):
    with open(str(jsonname) + ".json", "w") as jsonfile:
        json.dump(jsondata, jsonfile, indent=4)


def onStartHashCheck():
    Jsondata = fetchJson("MusicTags")
    DuplicatesData = fetchJson("DuplicateMusic")

    #If there aren't any hashes in MusicTags:
    if not Jsondata:
        ListofMusicFiles = os.listdir("MusicFiles")
        HashDictionary = {}
        DuplicatesDictionary = DuplicatesData

        #This shit works as intended
        for filename in ListofMusicFiles:
            MusicPath = "MusicFiles\\" + filename
            currenthash = hashFile(MusicPath, chunk_size=8192)
            if currenthash not in HashDictionary:
                HashDictionary[currenthash] = filename
            
            else:
                if currenthash not in DuplicatesDictionary:
                    DuplicatesDictionary[currenthash] = [filename, HashDictionary[currenthash]]
                
                else:
                    DuplicatesDictionary[currenthash].append(filename)
        
        print(HashDictionary)
        print()
        print(DuplicatesDictionary)

        writeJson("DuplicateMusic", DuplicatesData)

        for hashes in HashDictionary:
            Jsondata[hashes] = {"filepath": HashDictionary[hashes], "tags": []}
        
        writeJson("MusicTags", Jsondata)
        

    elif Jsondata:
        
        #Grab all filepaths in MusicFIles
        ListofMusicFiles = os.listdir("MusicFiles")

        #Make a list of the hashs in the json file
        ListofCurrentHashes = []
        for hashes in Jsondata:
            ListofCurrentHashes.append(hashes)

        # print()

        #For each hash in the list of hashes from the json file:
        # for currenthashes in ListofCurrentHashes:
        for currenthashes in Jsondata:


            #Check if the associated file path exists in the list of all filepaths
            if Jsondata[currenthashes]['filepath'] in ListofMusicFiles:
                
                #If it does then remove that filepath from the list of all filepaths and remove the hash from the list of hashes
                ListofCurrentHashes.remove(currenthashes)
                ListofMusicFiles.remove(Jsondata[currenthashes]['filepath'])


        # DuplicatesDictionary = DuplicatesData
        NonMusicTagsDictionary = {}

        #Creates a copy of the list instead of simply modifying ListofMusicFiles with CurrentMusicFiles = ListofMusicFiles
        #because python is fucking stupid and I hate this shit
        CurrentMusicFiles = list(ListofMusicFiles)

        HashMusicFiles = []
        Deletedhashes = []

        for item in CurrentMusicFiles:
            MusicPath = "MusicFiles\\" + item
            curhash = hashFile(MusicPath, chunk_size=8192)
            HashMusicFiles.append(curhash)
        
        for hash in ListofCurrentHashes:
            if hash not in HashMusicFiles:
                print("File has been deleted!!!!!!!!")
                Deletedhashes.append(hash)
            
            else:
                pass

        print(Deletedhashes)
        print(HashMusicFiles)

        for items in Deletedhashes:
            del Jsondata[items]

            if items in DuplicatesData:
                del DuplicatesData[items]

            ListofCurrentHashes.remove(items)
            


        #For each remaining filepath in the list of all filepaths:
        for filepath in ListofMusicFiles:
            MusicPath = "MusicFiles\\" + filepath

            #Hash the file
            filehash = hashFile(MusicPath, chunk_size=8192)

            # Tells us either it is a duplicate or it has been added
            if filehash not in ListofCurrentHashes:

                if filehash not in NonMusicTagsDictionary:
                    NonMusicTagsDictionary[filehash] = [filepath]

                else:
                    NonMusicTagsDictionary[filehash].append(filepath)

                


        #Cover adding and duplicates
        for hashes in NonMusicTagsDictionary:
            if hashes not in Jsondata:
                if len(NonMusicTagsDictionary[hashes]) > 1:

                    #Think about this more, we probably need to initialize the hash in DuplicateMusic
                    DuplicatesData[hashes] = []

                    for items in NonMusicTagsDictionary[hashes]:
   
                        DuplicatesData[hashes].append(items)

                        #Test this
                        CurrentMusicFiles.remove(items)
                    
                    Jsondata[hashes] = {"filepath": NonMusicTagsDictionary[hashes][0], "tags": []}
                    

                else:
                    Jsondata[hashes] = {"filepath": NonMusicTagsDictionary[hashes][0], "tags": []}

                    #Test This
                    CurrentMusicFiles.remove(NonMusicTagsDictionary[hashes][0])

            #If the hash is already in JsonData, we know its a duplicate
            else:

                #Prevents duplicate names being store in DuplicateMusic
                for items in NonMusicTagsDictionary[hashes]:

                    #Test this
                    CurrentMusicFiles.remove(items)

                    #If the duplicate is already known, just add the name to the duplicates dictionary
                    if hashes in DuplicatesData:
                        if items not in DuplicatesData[hashes]:
                            DuplicatesData[hashes].append(items)
                    
                    #If the duplicate doesn't already exist, initialize it
                    else:
                        DuplicatesData[hashes] = [items, Jsondata[hashes]['filepath']]

        RenamedDictionary = {}

        for hashes in ListofCurrentHashes:
            RenamedDictionary[hashes] = []

        for items in CurrentMusicFiles:
            MusicPath = "MusicFiles\\" + items
            renamedhashfile = hashFile(MusicPath, chunk_size=8192)

            RenamedDictionary[renamedhashfile].append(items)
            
        for hashes in RenamedDictionary:

            #Covers Duplicates
            if len(RenamedDictionary[hashes]) > 1:

                for items in RenamedDictionary[hashes]:

                    DuplicatesData[hashes].append(items)
                
                Jsondata[hashes]["filepath"] = RenamedDictionary[hashes][0]

            else:
                Jsondata[hashes]["filepath"] = RenamedDictionary[hashes][0]

        writeJson("DuplicateMusic", DuplicatesData)
        writeJson("MusicTags", Jsondata)

def onStartPlaylistsCheck():
    MusicTagsData = fetchJson("MusicTags")
    PlaylistsData = fetchJson("Playlists")

    if PlaylistsData:
        for Playlists in PlaylistsData:
            RemovedItems = []

            for items in PlaylistsData[Playlists]:
                if items not in MusicTagsData:
                    RemovedItems.append(items)

            #Makes it so that we don't have to remove items from the list we are iterating from
            for entries in RemovedItems:
                PlaylistsData[Playlists].remove(entries)

    writeJson("Playlists", PlaylistsData)


def hashFile(filepath, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as filetohash:
        while chunk := filetohash.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()

def ValidateExistance(filepath):
    ListOfMusicFiles = os.listdir("MusicFiles")
    ListOfMusicFiles = set(ListOfMusicFiles)
    if filepath in ListOfMusicFiles:
        return True
    else:
        return False
