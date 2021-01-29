import fnmatch
import logging
import os
import re
import win32con,win32api
import zipfile



def folder_cleaner(path,delete_zip=False,*args):

    """this function goes through a directory and extract every zipped folder into a file that aligns with the corresponding zipped file name
        it then deletes the zipped folder depending on whether or not the user of the function wishes to delete the zipped file.
        the path argument declares where the function should operate, the delete_zip optional arguement declares whether or not the zipped file
        should be deleted and the *args argument highlights all the files that should be hidden during this process."""

    #hide specified files
    # for arg in args:
        # win32api.SetFileAttributes(args,win32con.FILE_ATTRIBUTE_HIDDEN)

    # go through path directory
    for file in os.listdir(path):
            os.chdir(path)
            #check if zipped file exists
            if fnmatch.fnmatch(file, "*.zip"):
                #pulls out the zipped
                with zipfile.ZipFile(file,"r") as obj:
                    try:
                        #check if  folder with that name already exists, if not creates a folder if so redirects to the existing folder and extracts content
                        if os.path.isdir(file)!=True:
                            file_name,file_ext= os.path.splitext(file)
                            # renaming of files to my pleasing
                            os.mkdir(file_name)
                            for folder in os.listdir(path):
                                if os.path.isdir(folder)==True and folder == file_name :
                                   os.chdir(os.path.join(path,folder))
                                   obj.extractall()
                                   os.chdir(path)
                        else:
                            continue

                    except FileExistsError as e:
                        # print(logging.error(e))
                        for i,ch in enumerate(file_name):
                            os.mkdir(file_name+ str(i+1))
                            for folder in os.listdir(path):
                                if os.path.isdir(folder)==True:
                                   print(folder)
                                   os.chdir(folder)
                                   # obj.extractall()
                                   os.chdir(path)
                            break


                    except Exception as e:
                        print (logging.error(e))

                os.remove(file)


    #unhide specified files
    # for arg in args:
        # for attrs in win32api.GetFileAttributes(args):
            # if attrs & FILE_ATTRIBUTE_HIDDEN:
                # win32api.SetFileAttributes(args,win32con.FILE_ATTRIBUTE_NORMAL)
    #moves files to a designated location based on the content of the folder
    # shutil.move("/Users/user pc/Downloads/jack hill perry/Screenshot","/Users/user pc/Pictures/Screenshot")


def file_rename(path):
    # muzmo_ru_Propaganda_-_Darkie_feat_Micah_Boures_Jackie_Hill-Perry_58307106
    pattern= re.compile(r"\w+[_-]\w+[_-]((\w+[_])+)-_((\w+[_])+)(\d+|\w?\d+\w?\d?\w?\w*)")
    for file in os.listdir(path):
        files=pattern.finditer(file)
        for f in files:
            os.chdir(path)
            file_name,file_ext=os.path.splitext(file)
            tite=pattern.sub(r"\3",file_name)
            song_title=str(tite).strip('_').split('_')
            title=" ".join(song_title)
            song_titles= f'{title}{file_ext}'
            os.rename(file,song_titles)
            if "Lamentations" in file:
                os.rename(file, "Lamentations" )


if __name__ == '__main__':
    file_rename(r"\Users\user pc\Music\Propaganda- Crimson Cord")
