import copy
import hashlib
import logging
import os
import pickle
from abc import ABC, abstractmethod

from f9columnar.root_dataloader import get_root_dataloader
from f9columnar.utils.helpers import load_json, load_yaml
from f9columnar.utils.regex_helpers import extract_campaign_from_file


class PhysicsDataset:
    def __init__(self, name, root_files, is_data):
        self.name = name

        if type(root_files) is not list:
            root_files = [root_files]

        self.root_files = root_files
        self.is_data = is_data

        self.root_files_desc_dct = None
        self.dataloader_config, self.dataloader, self.num_entries = None, None, None

    def _setup_root_files_desc_dct(self):
        pop_attrs = ["root_files", "dataloader", "num_entries", "root_files_desc_dct", "sample_weights_builder"]
        root_files_desc_dct = {}

        for root_file in self.root_files:
            dct = copy.deepcopy(self.__dict__)

            for attr in pop_attrs:
                dct.pop(attr, None)

            root_files_desc_dct[root_file] = dct

        return root_files_desc_dct

    def setup_dataloader(self, **kwargs):
        assert "processors" not in kwargs, "Processors should not be passed in setup_dataloader!"
        self.dataloader_config = kwargs

        if self.root_files_desc_dct is None:
            self.root_files_desc_dct = self._setup_root_files_desc_dct()
        else:
            assert set(self.root_files) == set(self.root_files_desc_dct.keys()), "Desc. dct keys mismatch!"

        return self

    def init_dataloader(self, processors=None):
        self.dataloader, self.num_entries = get_root_dataloader(
            self.root_files,
            self.name,
            root_files_desc_dct=self.root_files_desc_dct,
            processors=processors,
            **self.dataloader_config,
        )
        return self


class MergedPhysicsDataset:
    def __init__(self, name, datasets, is_data):
        self.name = name
        self.datasets = datasets
        self.is_data = is_data

        self.root_files, self.root_files_desc_dct = [], {}
        self.dataloader_config, self.dataloader, self.num_entries = None, None, None

    def merge(self):
        dataloader_configs = []

        for dataset in self.datasets:
            dataloader_configs.append(dataset.dataloader_config)
            self.root_files += dataset.root_files

            if set(dataset.root_files_desc_dct).issubset(set(self.root_files_desc_dct.keys())):
                logging.warning("Root files already in merged dataset! Overwriting...")

            self.root_files_desc_dct.update(dataset.root_files_desc_dct)

        logging.info(f"[green]Merged {len(self.datasets)} datasets into {self.name} dataset![/green]")

        self.dataloader_config = dataloader_configs[0]
        logging.info("Using first dataloader config.")

        return self

    def init_dataloader(self, processors=None):
        self.dataloader, self.num_entries = get_root_dataloader(
            self.root_files,
            self.name,
            root_files_desc_dct=self.root_files_desc_dct,
            processors=processors,
            **self.dataloader_config,
        )
        return self


class MCSampleWeightsBuilder(ABC):
    def __init__(self):
        self.campaign_years = load_json("f9columnar/data/campaigns.json")["campaigns"]
        self.n_events = None
        self.sample_weights = None

    @abstractmethod
    def build_weights(self, dsid, campaign):
        pass


class MCDataset(PhysicsDataset):
    def __init__(
        self,
        name,
        root_files,
        dsid,
        campaigns_dct,
        is_signal=False,
        sample_weights_builder=None,
    ):
        super().__init__(name, root_files, False)
        self.dsid = dsid
        self.campaigns_dct = campaigns_dct
        self.is_signal = is_signal

        self.sample_weights_builder = sample_weights_builder

        self.sample_weights = None

    def setup_weights(self):
        self.sample_weights = {}

        for f, campaign in self.campaigns_dct.items():
            weight = self.sample_weights_builder.build_weights(self.dsid, campaign)
            self.sample_weights[f] = weight

        return self

    def __str__(self):
        return f"name: {self.name}, dsid: {self.dsid}, campaign {self.campaign}, num. files: {len(self.root_files)}"


class DataDataset(PhysicsDataset):
    def __init__(self, name, root_files, year):
        super().__init__(name, root_files, True)
        self.year = year

    def __str__(self):
        return f"name: {self.name}, year: {self.year}, num. files: {len(self.root_files)}"


class DatasetBuilder(ABC):
    def __init__(self, sample_config_path=None, sample_config=None, sample_weights_builder=None):
        """Base class for building datasets.

        Parameters
        ----------
        sample_config_path : str, optional
            Path to the sample config yaml file, by default None.
        sample_config : dict, optional
            Sample config dict if no yaml file, by default None.
        sample_weights_builder : object, optional
            MCSampleWeightsBuilder instance with build_weights method, by default None.

        Other parameters
        ----------------
        sample_config : dict
            {"samples": {sample1: [dsid1, dsid2, ...], sample2: [dsid3, dsid4, ...], ...},
             "campaigns": {campaign1: [sample1, sample2, ...], campaign2: [sample1, sample2, ...], ...},
             "years": [year1, year2, ...]}
        mc_datasets : list
            List of MCDataset instances.
        data_datasets : list
            List of DataDataset instances.
        dataloader_config : dict
            Dataloader configuration.
        branches : list
            List of branches used (needed for caching).

        Methods
        -------
        _validate_sample_config()
            Validate if sample config is correct.
        search_name(dsid)
            Find sample name given a dsid.
        search_campaign(name)
            Find campaign given a sample name.

        Abstract methods
        ----------------
        build_mc_datasets()
        build_data_datasets()
        setup_dataloaders(dataloader_config=None)
        init_dataloaders(processors=None)

        Raises
        ------
        AssertionError
            If sample config is not valid.

        """
        self.sample_config_path = sample_config_path

        if sample_config_path is not None:
            self.sample_config = load_yaml(self.sample_config_path)
        else:
            self.sample_config = sample_config

        self.sample_weights_builder = sample_weights_builder

        self._validate_sample_config()

        self.dataloader_config = None
        self.branches = None
        self.mc_datasets, self.data_datasets = [], []

    def _validate_sample_config(self):
        for key in ["samples", "campaigns", "years"]:
            assert key in self.sample_config.keys(), f"Key {key} not found in sample config!"

        assert isinstance(self.sample_config["samples"], dict)
        assert isinstance(self.sample_config["campaigns"], dict)
        assert isinstance(self.sample_config["years"], list)

        if "path" in self.sample_config.keys():
            assert isinstance(self.sample_config["path"], str)
            assert os.path.isdir(self.sample_config["path"]), f"Directory {self.sample_config['path']} does not exist!"

        for year in self.sample_config["years"]:
            assert isinstance(year, int)

        for name, dsids in self.sample_config["samples"].items():
            isinstance(name, str)
            isinstance(dsids, list)

            for dsid in dsids:
                isinstance(dsid, int)
                assert len(str(dsid)) == 6

        for campaign, samples in self.sample_config["campaigns"].items():
            isinstance(campaign, str)
            isinstance(samples, list)

            for sample in samples:
                isinstance(sample, str)

        for year in self.sample_config["years"]:
            assert isinstance(year, int)
            assert len(str(year)) == 2

        logging.info("Sample config validated!")

        return True

    def search_name(self, dsid):
        """Find sample name given a dsid."""
        for name, dsids in self.sample_config["samples"].items():
            if dsid in dsids:
                return name

    def search_campaign(self, name):
        """Find campaign given a sample name."""
        for campaign, samples in self.sample_config["campaigns"].items():
            if name in samples:
                return campaign

    @abstractmethod
    def build_mc_datasets(self):
        """Build MC datasets. Returns a list of MCDataset instances."""
        pass

    @abstractmethod
    def build_data_datasets(self):
        """Build data datasets. Returns a list of DataDataset instances."""
        pass

    @abstractmethod
    def setup_dataloaders(self, dataloader_config=None):
        """Setup dataloaders for MC and data datasets."""
        pass

    @abstractmethod
    def init_dataloaders(self, processors=None, description_dct=None):
        """Initialize dataloaders for MC and data datasets."""
        pass

    @abstractmethod
    def build(self, dataloader_config=None, processors=None, branches=None, cache=False):
        """Build datasets, setup cache, setup dataloaders and initialize dataloaders."""
        pass

    def _get_hash(self, mc_datasets, data_datasets, additional_cache_args=None):
        hash_lst = []

        if additional_cache_args is not None:
            hash_lst.append(additional_cache_args)

        hash_lst.append(self.sample_config)
        hash_lst.append(self.branches)

        hash_lst.append([d.root_files for d in mc_datasets])
        hash_lst.append([d.root_files for d in data_datasets])

        hash_lst.append(self.sample_weights_builder.sow_dsid_dct)

        dataloader_config = self.dataloader_config.copy()
        del dataloader_config["filter_branch"]
        hash_lst.append(dataloader_config)

        return hashlib.sha256(str(hash_lst).encode("utf-8")).hexdigest()

    def _dump_to_cache(self, mc_datasets, data_datasets, additional_cache_args=None, cache_name="datasets"):
        logging.info("[green]Caching datasets![/green]")

        os.makedirs("cache", exist_ok=True)
        hash_value = self._get_hash(mc_datasets, data_datasets, additional_cache_args)

        with open(f"cache/{cache_name}_{hash_value}.p", "wb") as f:
            pickle.dump([mc_datasets, data_datasets], f)

    def _load_from_cache(self, mc_datasets, data_datasets, additional_cache_args=None, cache_name="datasets"):
        hash_value = self._get_hash(mc_datasets, data_datasets, additional_cache_args)
        hash_path = f"cache/{cache_name}_{hash_value}.p"

        if os.path.isfile(hash_path):
            logging.info("[green]Loading cached datasets![/green]")

            with open(hash_path, "rb") as f:
                mc_datasets, data_datasets = pickle.load(f)

            if self.processors is not None:
                for data_dataset, mc_dataset in zip(data_datasets, mc_datasets):
                    data_dataset.dataloader.dataset.processors = self.processors
                    mc_dataset.dataloader.dataset.processors = self.processors

            return mc_datasets, data_datasets
        else:
            logging.info("[red]No cache found, building datasets![/red]")
            return None


class NtupleDatasetBuilder(DatasetBuilder):
    def __init__(self, ntuple_path=None, processors=None, max_root_files=None, local_run=True, **kwargs):
        """Base class for building datasets from ntuples.

        Parameters
        ----------
        ntuple_path : str, optional
            Path to the ntuples directory (if None check path in yaml config), by default None.
        processors : ProcessorsGraph, optional
            Processors graph for the dataloaders, by default None.
        max_root_files : int or None, optional
            Maximum number of root files in a dataloader, by default None.
        local_run : bool, optional
            If running locally. If False will take base names of root files, by default True.

        Note
        ----
        Only the build_sample_map method needs to be implemented in the derived class.

        """
        super().__init__(**kwargs)
        self.ntuple_path = ntuple_path
        self.processors = processors
        self.max_root_files = max_root_files
        self.local_run = local_run

        self.sample_map = None

    @abstractmethod
    def build_sample_map(self):
        """Mapping from specific dsid to corresponding root files.

        Return
        ------
        dict
            {"mc": {dsid1: root_files, dsid2: root_files, ...}, "data": {year1: root_files, year2: root_files, ...}}
        """
        pass

    def _validate_sample_map(self):
        for dsid, root_files in self.sample_map["mc"].items():
            if len(root_files) == 0:
                logging.warning(f"[red]No root files found for DSID {dsid}![/red]")

        for year, root_files in self.sample_map["data"].items():
            if len(root_files) == 0:
                logging.warning(f"[red]No root files found for year {year}![/red]")

        return self

    def _build_mc_dataset(self, root_files, sample_name, dsid, campaigns_dct, sample_weights_builder):
        datasets = []

        for root_file in root_files:  # root_files is a list of lists or just a list
            mc_dataset = MCDataset(
                sample_name,
                root_file,
                dsid,
                campaigns_dct,
                sample_weights_builder=sample_weights_builder,
            )

            if sample_weights_builder is not None:
                mc_dataset.setup_weights()

            datasets.append(mc_dataset)

        return datasets

    def _build_data_dataset(self, root_files, year):
        datasets = []

        for root_file in root_files:
            data_dataset = DataDataset(
                f"data{year}",
                root_file,
                year,
            )
            datasets.append(data_dataset)

        return datasets

    def _split_max_root_files(self, root_files):
        split_root_files = []

        for i in range(len(root_files) // self.max_root_files + 1):
            split = root_files[i * self.max_root_files : (i + 1) * self.max_root_files]
            if len(split) != 0:
                split_root_files.append(split)

        return split_root_files

    def build_mc_datasets(self):
        logging.info("[green]Building MC datasets![/green]")

        mc_sample_map = self.sample_map["mc"]
        samples = self.sample_config["samples"]

        sample_name_lst = list(samples.keys())

        mc_datasets, num_root_files = [], 0
        for sample_name in sample_name_lst:

            dsids = samples[sample_name]
            for dsid in dsids:
                if dsid not in mc_sample_map.keys():
                    logging.info(f"[yellow]Skipping {sample_name} sample with DSID {dsid}[/yellow]")
                    continue

                root_files = mc_sample_map[dsid]
                num_root_files += len(root_files)
                campaigns_dct = {os.path.basename(f): extract_campaign_from_file(f) for f in root_files}

                if not self.local_run:
                    root_files = [os.path.basename(f) for f in root_files]

                logging.info(f"Setting up {sample_name} sample with DSID {dsid} and {len(root_files)} root files!")

                if self.max_root_files:
                    root_files = self._split_max_root_files(root_files)
                else:
                    root_files = [root_files]

                mc_datasets += self._build_mc_dataset(
                    root_files,
                    sample_name,
                    dsid,
                    campaigns_dct,
                    self.sample_weights_builder,
                )

        logging.info(f"Built {len(mc_datasets)} MC datasets from {num_root_files} root files!")
        return mc_datasets

    def build_data_datasets(self):
        logging.info("[green]Building data datasets![/green]")

        data = self.sample_map["data"]

        data_datasets, num_root_files = [], 0
        for year, root_files in data.items():
            num_root_files += len(root_files)

            if not self.local_run:
                root_files = [os.path.basename(f) for f in root_files]

            logging.info(f"Setting up data for year {year} with {len(root_files)} root files!")

            if self.max_root_files:
                root_files = self._split_max_root_files(root_files)
            else:
                root_files = [root_files]

            data_datasets += self._build_data_dataset(root_files, year)

        logging.info(f"Built {len(data_datasets)} data datasets from {num_root_files} root files!")
        return data_datasets

    def setup_dataloaders(self, dataloader_config=None):
        if dataloader_config is None:
            dataloader_config = {}

        self.dataloader_config = dataloader_config

        logging.info("Setting up MC dataloaders!")
        for mc in self.mc_datasets:
            mc.setup_dataloader(**dataloader_config)

        logging.info("Setting up data dataloaders!")
        for data in self.data_datasets:
            data.setup_dataloader(**dataloader_config)

        return self

    @staticmethod
    def _dataloader_init(datasets, processors):
        for dataset in datasets:
            dataset.init_dataloader(processors=processors)
        return datasets

    def _dataloaders_init_executor(self, datasets):
        dataset_results = self._dataloader_init(datasets, self.processors)
        return dataset_results

    def init_dataloaders(self, cache=False):
        logging.info("[green]Initializing MC dataloaders![/green]")
        mc_datasets_init = self._dataloaders_init_executor(copy.deepcopy(self.mc_datasets))

        logging.info("[green]Initializing data dataloaders![/green]")
        data_datasets_init = self._dataloaders_init_executor(copy.deepcopy(self.data_datasets))

        if cache:
            self._dump_to_cache(mc_datasets_init, data_datasets_init)

        return mc_datasets_init, data_datasets_init

    def build(self, dataloader_config=None, merge=False):
        self.sample_map = self.build_sample_map()
        self._validate_sample_map()

        self.mc_datasets = self.build_mc_datasets()
        self.data_datasets = self.build_data_datasets()

        self.setup_dataloaders(dataloader_config)

        if merge:
            self.mc_datasets = [MergedPhysicsDataset("MC", self.mc_datasets, is_data=False).merge()]
            self.data_datasets = [MergedPhysicsDataset("Data", self.data_datasets, is_data=True).merge()]

        return self

    def init(self, branches=None, cache=False):
        run_init = False

        if cache:
            assert branches is not None, "Branches must be passed for caching!"
            self.branches = branches

            cached_datasets = self._load_from_cache(self.mc_datasets, self.data_datasets)

            if cached_datasets is None:
                run_init = True
            else:
                mc_datasets, data_datasets = cached_datasets
                run_init = False
        else:
            run_init = True

        if run_init:
            mc_datasets, data_datasets = self.init_dataloaders(cache)

        logging.info(f"Initialized {len(mc_datasets)} MC datasets and {len(data_datasets)} data datasets!")

        return mc_datasets, data_datasets
