import json
import os

DATASET_PATH = "f9columnar/submit/config"


def make_datasets_rse(dataset_path=DATASET_PATH):
    if not os.path.exists(f"{dataset_path}/datasets_rse.txt"):
        print("Making datasets_rse.txt...")

        os.system("rucio list-datasets-rse SIGNET_LOCALGROUPDISK > datasets_rse.txt")
        os.system(f"mv datasets_rse.txt {dataset_path}/datasets_rse.txt")
    else:
        print("datasets_rse.txt already exists!")

    return True


def get_rucio_datasets(match_str, dataset_path=DATASET_PATH):
    make_datasets_rse(dataset_path)

    datasets = []
    with open(f"{dataset_path}/datasets_rse.txt") as f:
        for line in f:
            if match_str in line:
                datasets.append(line.rstrip())

    return datasets


def get_rucio_files(datasets, dataset_path=DATASET_PATH):
    dataset_files = {}

    for i, dataset in enumerate(datasets):
        os.system(f"rucio list-files {dataset} --csv > files.txt")

        dataset_files[dataset] = []

        with open("files.txt") as f:
            for line in f:
                dataset_files[dataset].append(line.split(",")[0])

        if i % 10 == 0:
            print(f"Processed {i / len(datasets) * 100:.2f}%")

    os.system("rm files.txt")

    with open(f"{dataset_path}/dataset_files.json", "w") as f:
        json.dump(dataset_files, f, indent=4)

    return dataset_files


def local_download(match_str, download_path, dataset_path=DATASET_PATH, hist_only=False, dataset_dirs=None):
    make_datasets_rse(dataset_path)

    if dataset_dirs is None:
        dataset_dirs = get_rucio_datasets(match_str, dataset_path)

    current_dir = os.getcwd()
    os.chdir(download_path)

    n_dirs = len(dataset_dirs)
    for i, d in enumerate(dataset_dirs):
        if hist_only and "_hist" not in d:
            continue

        print(f"\nDownloading {i}/{n_dirs}: {d}\n")
        os.system(f"rucio download {d}")

    os.chdir(current_dir)


def validate_local_download(match_str, download_path, dataset_path=DATASET_PATH, hist_only=False):
    dataset_dirs = get_rucio_datasets(match_str, dataset_path)

    current_dir = os.getcwd()
    os.chdir(download_path)

    dataset_dirs_split = [d.split(":", 1)[1] for d in dataset_dirs]
    downloaded_dirs = [name for name in os.listdir(".") if os.path.isdir(os.path.join("", name))]

    if len(dataset_dirs) == 0:
        print("No datasets found!")
        return None

    missing, missing_idx = [], []
    for i, d in enumerate(dataset_dirs_split):
        if d not in downloaded_dirs:
            if hist_only and "_hist" not in d:
                continue

            missing.append(dataset_dirs[i])
            missing_idx.append(i)
            print(f"Missing: {d}")

    print(f"Missing {len(missing)} datasets")

    missing_dirs = []
    for i in missing_idx:
        missing_dirs.append(dataset_dirs[i])

    os.chdir(current_dir)

    return missing_dirs


def make_rucio_url(user, file):
    """Make a rucio URL for batch processing.

    Example
    -------
    rucio://rucio-lb-prod.cern.ch/replicas/user.jedebevc/user.jedebevc.00278912.physics_Main.r9264_p3083_p5314.39484806._000035.tree.root

    Parameters
    ----------
    user : str
        Rucio user.
    file : str
        Root file.

    Returns
    -------
    str
        URL for rucio file.
    """
    base_url = "rucio://rucio-lb-prod.cern.ch/replicas"
    return f"{base_url}/user.{user}/{file}"
