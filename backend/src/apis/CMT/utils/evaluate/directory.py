import os

from apis.utils.directory import dire


def create_dir(fol, in_fol):
    old_path = os.path.join(dire.dataset_path, "old")
    if not os.path.exists(old_path):
        os.makedirs(old_path)
    fol_arr = [fol for fol in os.listdir(dire.dataset_path) if fol != "old"]

    results_path = os.path.join(dire.results_path, fol, in_fol)
    if not os.path.exists(results_path):
        os.makedirs(results_path)
