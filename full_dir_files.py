import os

def get_list_files(path=None, type=".txt"):
    if path == None:
        return

    necessaryFiles = []

    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(file)
            fileType = os.path.splitext(f)[1]

            if fileType == type:
                necessaryFiles.append(os.path.join(root, file))
    
    return necessaryFiles

# path = r"E:\VolSU\Magistratura_2.2\VKR"
# #files = get_list_files(path, ".pdf")
# files = []
# for x in os.listdir(path):
#     if x.endswith(".pdf"):
#         files.append(os.path.join(path, x))
# print(len(files))
