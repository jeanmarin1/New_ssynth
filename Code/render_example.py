import util
import importlib
importlib.reload(util)
import pandas as pd
import mitsuba as mi
mi.set_variant('scalar_spectral')

from matplotlib import pyplot as plt

save_folder = '../data/OutputImages/Quick'

csv_save_name = '..\\data\\params_lists\\blood_model_quick.csv'

data_csv = pd.read_csv(csv_save_name)



# get render camera (une seule fois)
cam_top = util.get_sensor(5)

# boucle sur toutes les lignes du CSV
for row in range(len(data_csv)):

    params = data_csv.iloc[row]

    id_model = int(params['id_model'])
    id_fB_papillary = float(params['id_fB_papillary'])
    id_fb_upper_blood = float(params['id_fb_upper_blood'])
    id_fb_reticular = float(params['id_fb_reticular'])
    id_fb_deep_blood = float(params['id_fb_deep_blood'])
    id_mel = float(params['id_mel'])
    id_light = int(params['id_light'])


    # get material names
    sel_lightName = util.get_materials_names(id_light)

    # render image
    scene_ref = util.render_image(id_model,id_fB_papillary, id_fb_upper_blood, id_fb_reticular, id_fb_deep_blood, id_mel, sel_lightName, IMAGE=True)

    ref_image = mi.render(scene_ref, sensor=cam_top, spp=32)

    image_name = f"{save_folder}/Image_{row+1:02d}.png"
    mi.util.write_bitmap(image_name, ref_image)

    print(f"Saved {image_name}")