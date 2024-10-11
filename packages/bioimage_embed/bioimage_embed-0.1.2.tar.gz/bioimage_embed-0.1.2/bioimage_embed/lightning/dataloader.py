from torch.utils.data import DataLoader, WeightedRandomSampler
import pytorch_lightning as pl
import torch
from torch.utils.data import Dataset, random_split
from typing import Tuple
from functools import partial
import numpy as np


class StratifiedSampler(WeightedRandomSampler):
    def __init__(self, dataset, replacement=True):
        # Get the labels (targets) from the dataset
        self.targets = np.array([dataset[i][1] for i in range(len(dataset))])

        # Count the occurrences of each class
        class_counts = np.bincount(self.targets)

        # Calculate the weight for each class (inverse of frequency)
        class_weights = 1.0 / class_counts

        # Assign weights to each sample based on its class
        sample_weights = class_weights[self.targets]

        # Initialize the parent class (WeightedRandomSampler) with sample weights
        super().__init__(
            weights=sample_weights,
            num_samples=len(self.targets),
            replacement=replacement,
        )


# https://stackoverflow.com/questions/74931838/cant-pickle-local-object-evaluationloop-advance-locals-batch-to-device-pyto
class Collator:
    def collate_filter_for_none(self, batch):
        """
        Collate function that filters out None values from the batch.

        Args:
            batch: The batch to be filtered.

        Returns:
            The filtered batch.
        """
        batch = list(filter(lambda x: x is not None, batch))
        return torch.utils.data.dataloader.default_collate(batch)

    def __call__(self, incoming):
        # do stuff with incoming
        return self.collate_filter_for_none(incoming)


class DataModule(pl.LightningDataModule):
    """
    A PyTorch Lightning DataModule for handling dataset loading and splitting.

    Attributes:
        dataset: The dataset to be handled.
        batch_size: The size of each batch.
        num_workers: The number of workers for data loading.
        pin_memory: Whether to use pinned memory for data loading.
        drop_last: Whether to drop the last incomplete batch.
        collate_fn: The function to use for collating data into batches.
    """

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = 32,
        num_workers: int = 4,
        pin_memory: bool = False,
        drop_last: bool = False,
        # sampler=None,
        sampler=StratifiedSampler,
    ):
        """
        Initializes the DataModule with the given dataset and parameters.

        Args:
            dataset: The dataset to be handled.
            batch_size: The size of each batch. Default is 32.
            num_workers: The number of workers for data loading. Default is 4.
            pin_memory: Whether to use pinned memory for data loading. Default is False.
            drop_last: Whether to drop the last incomplete batch. Default is False.
            collate_fn: The function to use for collating data into batches. Default is None.
        """
        super().__init__()
        self.dataset = dataset
        self.collator = Collator()
        self.sampler = sampler
        self.dataloader = partial(
            DataLoader,
            batch_size=batch_size,
            num_workers=num_workers,
            pin_memory=pin_memory,
            drop_last=drop_last,
            collate_fn=self.collator,
        )

        self.train_dataset = None
        self.val_dataset = None
        self.test_dataset = None
        self.setup()

    def setup(self, stage=None):
        """
        Sets up the datasets by splitting the main dataset into train, validation, and test sets.

        Args:
            stage: The stage of the setup. Default is None.
        """
        (
            self.train_dataset,
            self.val_dataset,
            self.test_dataset,
        ) = self.splitting(self.dataset)

    def splitting(
        self, dataset: Dataset, split_train=0.8, split_val=0.1, seed=42
    ) -> Tuple[Dataset, Dataset, Dataset]:
        """
        Splits the dataset into train, validation, and test sets.

        Args:
            dataset: The dataset to be split.
            split_train: The proportion of the dataset to be used for training. Default is 0.8.
            split_val: The proportion of the dataset to be used for validation. Default is 0.1.
            seed: The random seed for splitting the dataset. Default is 42.

        Returns:
            A tuple containing the train, validation, and test datasets.
        """
        dataset_size = len(dataset)
        indices = list(range(dataset_size))
        train_size = int(split_train * dataset_size)
        val_size = int(split_val * dataset_size)
        test_size = dataset_size - train_size - val_size

        if train_size + val_size + test_size != dataset_size:
            raise ValueError(
                "The splitting ratios do not add up to the length of the dataset"
            )

        torch.manual_seed(seed)
        train_indices, val_indices, test_indices = random_split(
            indices, [train_size, val_size, test_size]
        )

        train_dataset = torch.utils.data.Subset(dataset, train_indices)
        val_dataset = torch.utils.data.Subset(dataset, val_indices)
        test_dataset = torch.utils.data.Subset(dataset, test_indices)

        return train_dataset, val_dataset, test_dataset

    def get_dataset(self):
        return self.dataset

    def train_dataloader(self):
        return self.init_dataloader(
            self.train_dataset,
            shuffle=False,
            sampler=self.sampler(self.train_dataset),
        )

    def val_dataloader(self):
        return self.init_dataloader(self.val_dataset, shuffle=False)

    def test_dataloader(self):
        return self.init_dataloader(self.test_dataset, shuffle=False)

    def predict_dataloader(self):
        return self.init_dataloader(self.dataset, shuffle=False)

    def init_dataloader(self, dataset, shuffle=False, sampler=None):
        """
        Initializes a dataloader for the given dataset.

        Args:
            dataset: The dataset to be loaded.
            shuffle: Whether to shuffle the dataset. Default is False.

        Returns:
            The dataloader for the dataset.
        """
        return (
            self.dataloader(
                dataset,
                shuffle=shuffle,
                sampler=sampler,
            )
            if dataset
            else None
        )


def valid_indices(dataset):
    valid_indices = []
    # Iterate through the dataset and apply the transform to each image
    for idx in range(len(dataset)):
        try:
            image, label = dataset[idx]
            # If the transform works without errors, add the index to the list of valid indices
            valid_indices.append(idx)
        except Exception as e:
            # A better way to do with would be with batch collation
            print(f"Error occurred for image {idx}: {e}")

    # Create a Subset using the valid indices
    subset = torch.utils.data.Subset(dataset, valid_indices)
    return subset
