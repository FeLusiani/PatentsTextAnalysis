import fasttext
import glob
import progressbar
import os
import pandas as pd
import codecs

def concatenate_txt(output_path, glob_filter=None, filenames=None, description=""):
    if filenames is None:
        filenames = glob.glob(glob_filter)

    with codecs.open(output_path, 'w', "utf-8") as outfile:
        bar_widgets = [description, progressbar.Percentage(), progressbar.Bar()]
        bar = progressbar.ProgressBar(widgets=bar_widgets, maxval=len(filenames)).start()
        for i in range(len(filenames)):
            fname = filenames[i]
            bar.update(i)
            if not os.path.isfile(fname):
                continue
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line.lower())

        bar.finish()

if __name__ == "__main__":
    ####    TEXT CONCATENATION
    # Concatenates all files, if full file does not exist
    output_path = "data/text_agglomerates/full_text.txt"
    if len(glob.glob(output_path)) == 0:
        print("No full text detected. Computing concatenated file.")
        glob_filter = 'clean_texts/*.txt'
        concatenate_txt(output_path=output_path, glob_filter=glob_filter, description="Concatenating files with filter " + glob_filter)
        print("Full text agglomerate computed and saved.\n")
    else:
        print("Full text agglomerate found.\n")

    # Concatenates all files by year, if they dont exist
    if len(glob.glob('data/text_agglomerates/*.txt')) < 21:
        print("Some year agglomerate text was not found. Computing concatenated files.")

        # Loop each year
        files = glob.glob('metadata/*.csv')
        for file in files:
            year_str = file[9:13]
            output_path = "data/text_agglomerates/" + year_str + "_text.txt"

            df = pd.read_csv(file)
            filenames = ["clean_texts/" + x[:-4] + ".txt" for x in df.loc[:,'Name']]

            concatenate_txt(output_path=output_path, filenames=filenames, description="Concatenating files from " + year_str + " ")

        print("Year agglomerates computed and saved.\n")
    else:
        print("All year agglomerates found.\n")

    ####    MODEL TRAINING
    # Trains fasttext on the agglomerates
    print("Training models:\n")
    model_folder = "data/fasttext/models"

    # Full text model
    model_path = model_folder + "/full_text.bin"
    if os.path.isfile(model_path):
        print(f"Full text model already found.")
    else:
        print(f"Training full text model.")
        model = fasttext.train_unsupervised(f"data/text_agglomerates/full_text.txt")
        print("Sample words:", model.words[:10])
        model.save_model(model_path)

    # Different years models
    for year in range(2000, 2020):
        model_path = model_folder + f"/{year}.bin"

        if os.path.isfile(model_path):
            print(f"Year {year} already found.")
            continue
        else:
            print(f"\nTraining year {year}.")

        #try:
        model = fasttext.train_unsupervised(f"data/text_agglomerates/{year}_text.txt")
        print("Sample words:", model.words[:10])
        model.save_model(model_path)
        #except:
        #    print(f"Year {year} has insufficient data.")
