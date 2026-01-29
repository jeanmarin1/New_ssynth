import os
import itertools
import pandas as pd

# ==========================================================
# Listes de valeurs autorisées
# ==========================================================

ID_MODELS = [0, 1, 2]

ID_FB_PAPILLARY = [0.011, 0.015, 0.020, 0.025]

ID_FB_UPPER_BLOOD = [
    0.02, 0.03, 0.04, 0.05,
    0.1, 0.2, 0.3, 0.4, 0.5
]

ID_FB_RETICULAR = [0.0075, 0.01, 0.012, 0.014]

ID_FB_DEEP_BLOOD = [
    0.01, 0.02, 0.03, 0.04,
    0.1, 0.2, 0.3, 0.4, 0.5
]

# Mélanine
ID_MELS_FULL = [round(x, 2) for x in list(pd.np.linspace(0.01, 0.50, 50))]
ID_MELS_INTERMEDIATE = [
    0.01, 0.05, 0.1, 0.15, 0.2,
    0.25, 0.3, 0.35, 0.4, 0.45, 0.5
]

# ==========================================================
# Quick parameters
# ==========================================================

MODELS_QUICK = [0, 1, 2]

SANG_QUICK = [
    [0.011, 0.02, 0.0075, 0.01],  # MINIMUM
    [0.025, 0.5, 0.014, 0.5],     # MAXIMUM
    [0.015, 0.1, 0.01, 0.1]       # INTERMÉDIAIRE
]

MELS_QUICK = [0.01, 0.1, 0.25]

# ==========================================================
# Règle upper / deep
# ==========================================================

def is_valid_upper_deep_pair(upper, deep):
    """
    deep == upper
    ou deep == valeur immédiatement inférieure
    dans ID_FB_DEEP_BLOOD
    """
    if deep == upper:
        return True

    deep_values = sorted(ID_FB_DEEP_BLOOD)

    if deep not in deep_values or upper not in ID_FB_UPPER_BLOOD:
        return False

    if upper not in deep_values:
        return False

    idx = deep_values.index(upper)
    if idx == 0:
        return False

    return deep == deep_values[idx - 1]

# ==========================================================
# QUICK
# ==========================================================

def create_quick_df():
    rows = []
    for model in MODELS_QUICK:
        for pap, upper, retic, deep in SANG_QUICK:
            if not is_valid_upper_deep_pair(upper, deep):
                continue
            for mel in MELS_QUICK:
                rows.append([model, pap, upper, retic, deep, mel, 19])

    return pd.DataFrame(rows, columns=[
        'id_model',
        'id_fB_papillary',
        'id_fb_upper_blood',
        'id_fb_reticular',
        'id_fb_deep_blood',
        'id_mel',
        'id_light',
    ])

# ==========================================================
# INTERMEDIATE
# ==========================================================

def create_intermediate_df():
    rows = []
    for model, pap, upper, retic, deep, mel in itertools.product(
        ID_MODELS,
        ID_FB_PAPILLARY,
        ID_FB_UPPER_BLOOD,
        ID_FB_RETICULAR,
        ID_FB_DEEP_BLOOD,
        ID_MELS_INTERMEDIATE
    ):
        if not is_valid_upper_deep_pair(upper, deep):
            continue
        rows.append([model, pap, upper, retic, deep, mel, 19])

    return pd.DataFrame(rows, columns=[
        'id_model',
        'id_fB_papillary',
        'id_fb_upper_blood',
        'id_fb_reticular',
        'id_fb_deep_blood',
        'id_mel',
        'id_light',
    ])

# ==========================================================
# FULL
# ==========================================================

def create_full_df():
    rows = []
    for model, pap, upper, retic, deep, mel in itertools.product(
        ID_MODELS,
        ID_FB_PAPILLARY,
        ID_FB_UPPER_BLOOD,
        ID_FB_RETICULAR,
        ID_FB_DEEP_BLOOD,
        ID_MELS_FULL
    ):
        if not is_valid_upper_deep_pair(upper, deep):
            continue
        rows.append([model, pap, upper, retic, deep, mel, 19])

    return pd.DataFrame(rows, columns=[
        'id_model',
        'id_fB_papillary',
        'id_fb_upper_blood',
        'id_fb_reticular',
        'id_fb_deep_blood',
        'id_mel',
        'id_light',
    ])

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    save_path = "../data/params_lists/"
    os.makedirs(save_path, exist_ok=True)

    df_quick = create_quick_df()
    df_quick.to_csv(os.path.join(save_path, "blood_model_quick.csv"), index=False)
    print(f"✅ Quick file : {len(df_quick)} lignes")

    df_inter = create_intermediate_df()
    df_inter.to_csv(os.path.join(save_path, "blood_model_intermediate.csv"), index=False)
    print(f"✅ Intermediate file : {len(df_inter)} lignes")

    df_full = create_full_df()
    df_full.to_csv(os.path.join(save_path, "blood_model_full.csv"), index=False)
    print(f"✅ Full file : {len(df_full)} lignes")

