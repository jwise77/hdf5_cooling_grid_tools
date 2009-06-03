import h5py
import numpy as na

dataTypes = {"<type 'float'>":'>f8',"<type 'int'>":'>i8'}

def get_attributes(file):
    "Get all dataset attributes and their datatypes."

    attributes = {}

    closeFile = False

    if type(file) == h5py.highlevel.File:
        input = file
    else:
        input = h5py.File(file,'r')
        closeFile = True

    # Get all dataset attributes.
    for dataset in input.listnames():
        attributes[dataset] = {}
        for attribute in input[dataset].attrs.listnames():
            attributes[dataset][attribute] = {}
            if type(input[dataset].attrs[attribute]) == na.ndarray:
                attributes[dataset][attribute]['dtype'] = input[dataset].attrs[attribute].dtype
            else:
                thisType = type(input[dataset].attrs[attribute])
                if dataTypes.has_key("%s" % thisType):
                    attributes[dataset][attribute]['dtype'] = dataTypes["%s" % thisType]
                else:
                    attributes[dataset][attribute]['dtype'] = thisType
            attributes[dataset][attribute]['value'] = input[dataset].attrs[attribute]

    if closeFile:
        input.close()

    return attributes

def write_attributes(output,attributes):
    "Write out all dataset attributes."

    for dataset in attributes.keys():
        for attribute in attributes[dataset].keys():
            if type(attributes[dataset][attribute]['value']) == na.ndarray:
                output[dataset].attrs[attribute] = attributes[dataset][attribute]['value']
            else:
                output[dataset].attrs[attribute] = na.array(attributes[dataset][attribute]['value'],
                                                            dtype=attributes[dataset][attribute]['dtype'])
