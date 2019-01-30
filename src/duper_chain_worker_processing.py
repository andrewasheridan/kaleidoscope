from tools import load_obj

# recieve image_paths.pickle
# TODO: should not be hardcoded
s3_objects_pickle_path = '../s3_keys/batch_0000000000.pickle'

# open image_paths.pickle 
s3_objects = load_obj(s3_objects_pickle_path)

# for each path
#   load image, augment & save to s3 (or maybe save locally and then push to s3 en masse)
#   load tagline, create new taglines, write taglines locally, p
for path in s3_objects:
    print(path)

# rec
