import os
import shutil
import numpy as np

path = os.getcwd()

def move_to_combined():
    splits = ['test', 'train', 'valid']

    for split in splits:
        for img in os.listdir(f'{path}/b_ds/{split}/images'):
            shutil.copy(f'{path}/b_ds/{split}/images/{img}', f'{path}/combined_ds/images/{img}')
        for label in os.listdir(f'{path}/b_ds/{split}/labels'):
            shutil.copy(f'{path}/b_ds/{split}/labels/{label}', f'{path}/combined_ds/labels/{label}')

def organize_to_names():
    names = ['anabaena', 'aphanizomenon', 'detritus', 'dolichospermum', 'microcystis', 'oscillatoria', 'synechococcus', 'water bubble', 'woronichinia']
    names_with_freqs = [0 for i in range(len(names))]
    x=0
    for label in os.listdir(path + "/combined_ds/labels"):
        # organize everything into folders based on
        
        with open(path + f"/combined_ds/labels/{label}") as file:
            # read first line
            asdf = file.readline().split(" ")[0]
            print(asdf)
            try:
                numval = int(asdf)
                print(numval)
                real_name = names[numval]
                # override previous folder
                if os.path.exists(path + f"/org_ds/{real_name}"):
                    shutil.rmtree(path + f"/org_ds/{real_name}")
                os.mkdir(path + f"/org_ds/{real_name}")
                # move image and label to folder
                shutil.copy(path + f"/combined_ds/images/{label[:-4]}.jpg", path + f"/org_ds/{real_name}/{f'{real_name}_{names_with_freqs[numval]+1}'}.jpg")
                x+=1
                names_with_freqs[numval] += 1
                # copy the label file to labels folder
                shutil.copy(path + f"/combined_ds/labels/{label}", path + f"/org_ds/labels/{f'{real_name}_{names_with_freqs[numval]}'}.txt")
            except:
                print("failure")
                # label does not exist
    print(x)

def get_train_val_test_splits():
    names = ['anabaena', 'aphanizomenon', 'detritus', 'dolichospermum', 'microcystis', 'oscillatoria', 'synechococcus', 'water bubble', 'woronichinia']

    ftrain, fval, ftest = np.array([]), np.array([]), np.array([])
    # stratify splitting of data
    for name in names:
        allFileNames = os.listdir(path + f"/org_ds/{name}")
        print(len(allFileNames))

        np.random.shuffle(allFileNames)

        train, val, test = np.split(np.array(allFileNames),[int(len(allFileNames)*0.8), int(len(allFileNames)*0.9)])
        print(len(train), len(val), len(test))

        ftrain = np.concatenate((ftrain, train))
        fval = np.concatenate((fval, val))
        ftest = np.concatenate((ftest, test))
    
    return ftrain, fval, ftest

def check_freqs(ftrain, fval, ftest):
    names = ['anabaena', 'aphanizomenon', 'detritus', 'dolichospermum', 'microcystis', 'oscillatoria', 'synechococcus', 'water bubble', 'woronichinia']
    name_counter = [0 for i in range(len(names))]
    splits = [ftrain, fval, ftest]
    print(len(ftrain), len(fval), len(ftest))
    print(len(ftrain)/(len(ftrain)+len(fval)+len(ftest)))
    for split in splits:
        print(split)
        for f in split:
            for n in names:
                if n in f:
                    name_counter[names.index(n)] += 1

        asdfasdf = 0
        for name in range(len(names)):
            print(names[name], name_counter[name])
            asdfasdf += name_counter[name]
        print(asdfasdf)

# re-organize everything back into same format
def reorganize_to_final(ftrain, fval, ftest):
    splits = ['test', 'train', 'valid']
    
    # clear existing final ds
    if os.path.exists(path + "/final_ds"):
        shutil.rmtree(path + "/final_ds")
    os.mkdir(path + "/final_ds")

    for split in splits:
        if os.path.exists(path + f"/final_ds/{split}"):
            shutil.rmtree(path + f"/final_ds/{split}")    
        if os.path.exists(path + f"/final_ds/{split}/images"):
            shutil.rmtree(path + f"/final_ds/{split}/images")
        if os.path.exists(path + f"/final_ds/{split}/labels"):
            shutil.rmtree(path + f"/final_ds/{split}/labels")
        
        os.mkdir(path + f"/final_ds/{split}")
        os.mkdir(path + f"/final_ds/{split}/images")
        os.mkdir(path + f"/final_ds/{split}/labels")

        thing = ftrain if split == 'train' else fval if split == 'val' else ftest
        print(thing)
        for file in thing:
            c = file.split("_")[0]
            shutil.copy(path + f"/org_ds/{c}/{file}", path + f"/final_ds/{split}/images/{file}")
            shutil.copy(path + f"/org_ds/labels/{file[:-4]}.txt", path + f"/final_ds/{split}/labels/{file[:-4]}.txt")

def rebalance_dataset():
    move_to_combined()
    organize_to_names()
    ftrain, fval, ftest = get_train_val_test_splits()
    check_freqs(ftrain, fval, ftest)
    reorganize_to_final(ftrain, fval, ftest)