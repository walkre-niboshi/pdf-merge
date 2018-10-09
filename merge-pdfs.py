#!/usr/bin/env python
# import modules
from PyPDF2 import PdfFileReader, PdfFileMerger
from pdfrw import PdfReader, PdfWriter, PageMerge
import os

# setup merger
merger = PdfFileMerger()

# define function to generate 4 page versions
def get4(srcpages):
    scale = 0.5
    srcpages = PageMerge() + srcpages
    x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])

    for i, page in enumerate(srcpages):
        page.scale(scale)
        page.x = x_increment if i & 1 else 0
        page.y = 0 if i & 2 else y_increment
    return srcpages.render()

# get initial file list
def get_file_list():
    filelist = [(os.path.getctime(fname), fname) for fname in os.listdir('.') if fname.endswith(".pdf")]
    filelist = sorted(filelist)
    return filelist

# iterate through list of files and create 4 page version
def create_4page_versions():
    files = get_file_list()
    fnames = [file[1] for file in files]
        
    for fname in fnames:
        inpfn = fname
        outfn = "4pageversion_" + fname

        pages = PdfReader(inpfn).pages
        writer = PdfWriter(outfn)
        
        for index in range(0, len(pages), 4):
            writer.addpage(get4(pages[index:index + 4]))

        writer.write()

# get sorted list of the 4 page files
def get_new_file_list():
    filelist = [(os.path.getctime(fname), fname) for fname in os.listdir('.') if fname.startswith("4pageversion")]
    filelist = sorted(filelist)
    return filelist

# iterate through 4 page versions to combine them
def combine_4page_versions():
    files = get_new_file_list()
    fnames = [file[1] for file in files]

    for fname in fnames:
        merger.append(PdfFileReader(open(fname, "rb")))

    merger.write("combined_receipts.pdf")

def remove_temp_files():
    file_list = [x for x in os.listdir('.') if x.startswith("4pageversion_")]
    for fname in file_list:
        os.remove(fname)

def move_individual_files():
    file_list = [x for x in os.listdir('.') if not x.startswith("combined")]
    os.mkdir("Originals")
    for fname in file_list:
        os.rename(fname, "./Originals/"+fname)

# ultimate function
def execute():
    create_4page_versions()
    #combine_4page_versions()
    #remove_temp_files()
    #move_individual_files()

execute()
