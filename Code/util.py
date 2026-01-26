import os
import random
import string
import numpy as np
import drjit as dr

import mitsuba as mi



def random_string(n=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def render_image(count, random_fB_papillary, random_fb_upper_blood, random_fb_reticular, random_fb_deep_blood, random_mel, random_lightName, IMAGE=True, verbose=True):
    
    models_dir = r"C:/Users/marin/ssynth_new/data/" #Chemin à modifier

    uniformScale = 1  # uniformly scale the models
    yOffset = -1.5  # this is to counter the y offset of the models in houdini which is not centered at 0.
    # lesionOffset = -2.5 #0 is on skin surface. # for outout10k
    roomSize = 20  # current skin size is 20x20x5mm, so the room should be large enough to fit the skin
    xtScale = 0.1  # extinction scale. 1 unit in mitsuba/houdini = 1mm, and optical coefficients are in inverse cm

    if verbose:
        # hair_albedo is used
        print("Model id = " + str(count))
        print("Blood fraction of Papillary Dermis material = " + str(random_fB_papillary))
        print("Blood fraction of Upper Blood Dermis material = " + str(random_fb_upper_blood))
        print("Blood fraction of Reticular Dermis material = " + str(random_fb_reticular))
        print("Blood fraction of Deep Blood Dermis material = " + str(random_fb_deep_blood))
        print("Melanosome fraction of Epidermis material = " + str(random_mel))
        print("Light name =  " + str(random_lightName))
        print()

    # refractive index for epidermis between 1.42-1.44
    iorEpi = 1.43

    # refractive index for hypodermis
    iorHypo = 1.44

    # refractive index for dermis is wavelength-dependent, but cannot input spectrum for ior in bsdf
    # therefore, will normalize to lambda = 500nm
    A = 1.3696
    B = 3916.8
    C = 2558.8
    iorDerm = A + (B / (500 ** 2)) + (C / (500 ** 4))

    scene = {'type': 'scene',
             'integrator': {'type': 'volpathmis','max_depth': 1000}}
    
    if IMAGE:
        scene['epidermis'] = {
            'type': 'obj',
            'filename': os.path.join(models_dir + 'OutputModels/1/',f"epidermis_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.1,
                     'int_ior': iorEpi,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + 'Materials/epidermis_alb_mel' + str(random_mel) + '.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + 'Materials/epidermis_ext_mel' + str(random_mel) + '.spd'
                },
                'scale': xtScale
            }
        }

        scene['papillary'] = {
            'type': 'obj',
            'filename': os.path.join (models_dir + 'OutputModels/1/', f"papillary_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.01,
                     'int_ior': iorDerm,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/papillary_alb_fB{random_fB_papillary}.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/papillary_ext_fB{random_fB_papillary}.spd'
                },
                'scale': xtScale
            }
        }

        scene['upper_blood'] = {
            'type': 'obj',
            'filename': os.path.join (models_dir + 'OutputModels/1/', f"upper_blood_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.01,
                     'int_ior': iorDerm,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/upper_blood_alb_fB{random_fb_upper_blood}.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/upper_blood_ext_fB{random_fb_upper_blood}.spd'
                },
                'scale': xtScale
            }
        }

        scene['reticular'] = {
            'type': 'obj',
            'filename': os.path.join (models_dir + 'OutputModels/1/', f"reticular_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.01,
                     'int_ior': iorDerm,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/reticular_alb_fB{random_fb_reticular}.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/reticular_ext_fB{random_fb_reticular}.spd'
                },
                'scale': xtScale
            }
        }

        scene['deep_blood'] = {
            'type': 'obj',
            'filename': os.path.join (models_dir + 'OutputModels/1/', f"deep_blood_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.01,
                     'int_ior': iorDerm,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/deep_blood_alb_fB{random_fb_deep_blood}.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + f'Materials/deep_blood_ext_fB{random_fb_deep_blood}.spd'
                },
                'scale': xtScale
            }
        }

        scene['subcutfat'] = {
            'type': 'obj',
            'filename': os.path.join (models_dir + 'OutputModels/1/', f"hypodermis_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'roughdielectric',
                     'alpha': 0.01,
                     'int_ior': iorHypo,
                     'ext_ior': 1.000277},
            'interior': {
                'type': 'homogeneous',
                'albedo': {
                    'type': 'spectrum',
                    'filename': models_dir + 'Materials/hypo_alb' + '.spd'
                },
                'sigma_t': {
                    'type': 'spectrum',
                    'filename': models_dir + 'Materials/hypo_ext' + '.spd'
                },
                'scale': xtScale
            }
        }
        if random_lightName == 'diffuse':
            scene['env_light'] = {
                'type': 'constant',
                'radiance': {
                    'type': 'd65',
                    'scale': 2.5
                }
            }
        else:
            scene['env_light'] = {
                'type': 'envmap',
                'filename': models_dir + 'hdri/' + random_lightName + '.exr',
                'scale': 3
            }

        scene['wall_floor'] = {
            'type': 'rectangle',
            'to_world': mi.ScalarTransform4f.scale([roomSize, 1, roomSize]).translate([0, -roomSize, 0]).rotate(
                [1, 0, 0], -90),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': 0.5
                    }
                }
            }
        }
    else:

        scene['epidermis'] = {
            'type': 'obj',
            'filename': os.path.join(models_dir + 'OutputModels/1/',f"epidermis_{count:03d}.obj"),
            'to_world': mi.ScalarTransform4f.scale(uniformScale).translate([0, yOffset, 0]).rotate([0, 0, 0], 0),
            'bsdf': {'type': 'diffuse',
                     'reflectance': {
                         'type': 'rgb',
                         'value': [0.0, 0.0, 0.0]
                     }
                     }
        }
        scene['shape_light'] = {
            'type': 'rectangle',
            'to_world': mi.ScalarTransform4f.scale([roomSize, 1, roomSize]).translate([0, roomSize, 0]).rotate(
                [1, 0, 0], 90),
            'emitter': {
                'type': 'area',
                'radiance': {
                    'type': 'd65',
                    'scale': 10
                }
            }
        }
        scene['wall_floor'] = {
            'type': 'rectangle',
            'to_world': mi.ScalarTransform4f.scale([roomSize, 1, roomSize]).translate([0, -roomSize, 0]).rotate(
                [1, 0, 0], -90),
            'bsdf': {
                'type': 'twosided',
                'material': {
                    'type': 'diffuse',
                    'reflectance': {
                        'type': 'rgb',
                        'value': [0.0, 0.0, 0.0]
                    }
                }
            }
        }


    scene_ref = mi.load_dict(scene)
    return scene_ref


def get_sensor(id_origin_y):
    return mi.load_dict({
        'type': 'orthographic',
        'to_world': mi.scalar_spectral.Transform4f.look_at(
            origin=[0, id_origin_y, 0],
            target=[0, 0, 0],
            up=[0, 0, 1]
        ),
        'film': {
            'type': 'hdrfilm',
            'width': 1024,
            'height': 1024
        }
    })


def get_l_model():  # model ID
    l_model = list(range(20))
    return l_model


def get_l_fractionBlood():  # blood fraction value
    l_fractionBlood = [0.002, 0.005, 0.02, 0.05]
    return l_fractionBlood


def get_l_melanosomes():  # melanosomes fraction value
    l_melanosomes = [float(x) / 100 for x in range(1, 51)]
    return l_melanosomes


def get_l_light():  # light model ID
    l_light = list(range(19))
    return l_light



def get_param_combo(light_id=None):
    l_model = get_l_model()
    l_fractionBlood = get_l_fractionBlood()
    l_melanosomes = get_l_melanosomes()
    l_light = get_l_light()

    id_model = random.choice(l_model)
    id_fracBlood = random.choice(l_fractionBlood)
    id_mel = random.choice(l_melanosomes)

    if not light_id:
        id_light = random.choice(l_light)
    else:
        id_light = light_id

    print('id_model ' + str(id_model))
    print('id_fracBlood ' + str(id_fracBlood))
    print('id_mel ' + str(id_mel))
    print('id_light ' + str(id_light))

    sel_lightName = get_light_names(id_light)

    return id_model, id_fracBlood, id_mel, sel_lightName




def get_light_names():
    exr_files = ['rural_asphalt_road_4k', 'comfy_cafe_4k', 'reading_room_4k', 'school_hall_4k', 'bathroom_4k',
                 'floral_tent_4k',
                 'st_fagans_interior_4k', 'vulture_hide_4k', 'lapa_4k', 'surgery_4k', 'veranda_4k',
                 'vintage_measuring_lab_4k',
                 'yaris_interior_garage_4k', 'hospital_room_4k', 'bush_restaurant_4k', 'lythwood_room_4k',
                 'kiara_interior_4k',
                 'reinforced_concrete_01_4k', 'graffiti_shelter_4k', 'diffuse']
    return exr_files

def get_materials_names(id_light):

    exr_files = get_light_names()
    sel_lightName = exr_files[id_light]
    return  sel_lightName


def get_save_folder(saveDir, count, random_hair_model, random_mel, random_fB, random_lesion, random_timePoint,
                    random_lesionMat, hair_albedo, random_lightName, mi_variant, id_lesionScale,
                    id_origin_y=None):
    folder = saveDir + "output/skin_" + f'{count:03d}'
    folder += "/hairModel_" + f'{random_hair_model:03d}'
    folder += "/mel_" + str(random_mel)
    folder += "/fB_" + str(random_fB)
    folder += "/lesion_" + str(random_lesion)
    folder += "/T_" + f'{random_timePoint:03d}'
    folder += "/" + str(random_lesionMat)
    folder += "/hairAlb_" + '-'.join([str(x) for x in hair_albedo])  # str(hair_albedo_id)
    folder += "/lesionScale_" + str(id_lesionScale) + "/"
    folder += "/light_" + random_lightName + "/"
    if id_origin_y:
        folder += "/origin_y_" + str(id_origin_y) + "/"
    folder += "/mi_" + mi_variant + "/"
    os.makedirs(folder, exist_ok=True)
    return folder