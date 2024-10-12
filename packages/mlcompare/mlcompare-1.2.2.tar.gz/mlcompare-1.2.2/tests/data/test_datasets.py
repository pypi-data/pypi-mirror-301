import logging
import os
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError
from openml.exceptions import OpenMLServerException
from pydantic import ValidationError

from mlcompare.data.datasets import (
    BaseDataset,
    DatasetFactory,
    HuggingFaceDataset,
    KaggleDataset,
    LocalDataset,
    OpenMLDataset,
    df_from_suffix,
)

logger = logging.getLogger("mlcompare.data.datasets")


def create_csv_file(file_path: str | Path) -> None:
    two_column_data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    data = pd.DataFrame(two_column_data)
    data.to_csv(file_path, index=False)


@pytest.mark.parametrize(
    "file_type,reader_func",
    [
        (".parquet", "read_parquet"),
        (".csv", "read_csv"),
        (".pkl", "read_pickle"),
        (".json", "read_json"),
    ],
)
def test_df_from_suffix_supported_types(file_type, reader_func):
    mock_path = Path(f"test{file_type}")
    with patch(f"pandas.{reader_func}") as mock_reader:
        mock_reader.return_value = pd.DataFrame()
        df = df_from_suffix(mock_path, logger)

        assert isinstance(df, pd.DataFrame)


def test_df_from_suffix_invalid_path():
    pytest.raises(FileNotFoundError, df_from_suffix, Path("invalid_path.csv"), logger)


def test_df_from_suffix_unsupported_file_type():
    pytest.raises(ValueError, df_from_suffix, Path("invalid_path.xml"), logger)


# Abstract base class with an abstract method `validate_data` shouldn't be instantiable
class TestBaseDataset:
    def test_init(self):
        with pytest.raises(TypeError):
            BaseDataset(target="target", drop=["col1"], oneHotEncode=["col2"])


# Minimal implementation of BaseDataset for testing
class BaseDatasetChild(BaseDataset):
    def model_post_init(self, Any) -> None:
        pass

    def create_save_name(self):
        pass

    def get_data(self) -> pd.DataFrame:
        return pd.DataFrame()


class TestBaseDatasetChild:
    def test_init(self):
        dummy_dataset = BaseDatasetChild(
            target="target", saveName="dummy_dataset", drop=["col1"], oneHotEncode=["col2", "col3"]
        )

        assert dummy_dataset.target == "target"
        assert dummy_dataset.save_name == "dummy_dataset"
        assert dummy_dataset.drop == ["col1"]
        assert dummy_dataset.one_hot_encode == ["col2", "col3"]

    def test_no_optional_columns(self):
        dummy_dataset = BaseDatasetChild(target="target")

        assert dummy_dataset.target == "target"
        assert dummy_dataset.drop is None
        assert dummy_dataset.one_hot_encode is None
        assert dummy_dataset.save_name is None

    def test_no_target(self):
        with pytest.raises(ValidationError):
            BaseDatasetChild()

    def test_invalid_target_type(self):
        with pytest.raises(ValidationError):
            BaseDatasetChild(target=123)

    def test_invalid_save_name_type(self):
        with pytest.raises(ValidationError):
            BaseDatasetChild(target="target", saveName=123)

    def test_invalid_drop_type(self):
        with pytest.raises(ValidationError):
            BaseDatasetChild(target="target", drop="123")

    def test_invalid_one_hot_encode_type(self):
        with pytest.raises(ValidationError):
            BaseDatasetChild(target="target", oneHotEncode="123")


# Currently the `validate_data` and `create_save_name` methods are run at initialization
class TestLocalDataset:
    test_path = Path("local_dataset.csv")
    create_csv_file(test_path)

    def test_init(self):
        dataset = LocalDataset(
            path=self.test_path,
            target="target",
            saveName="testing_local_dataset",
            drop=["col1", "col2"],
            oneHotEncode=["col3"],
        )

        assert dataset.file_path == self.test_path
        assert dataset.target == "target"
        assert dataset.save_name == "testing_local_dataset"
        assert dataset.drop == ["col1", "col2"]
        assert dataset.one_hot_encode == ["col3"]

    def test_init_with_str_path(self):
        dataset = LocalDataset(path="local_dataset.csv", target="target")

        assert isinstance(dataset.file_path, Path)

    def test_invalid_path_with_path_object(self):
        with pytest.raises(FileNotFoundError):
            LocalDataset(path=Path("file.csv"), target="target")

    def test_invalid_path_with_str(self):
        with pytest.raises(FileNotFoundError):
            LocalDataset(path="file.csv", target="target")

    def test_invalid_path_type(self):
        with pytest.raises(ValidationError):
            LocalDataset(path=123, target="target")

    def test_no_path(self):
        with pytest.raises(ValidationError):
            LocalDataset(target="target")

    def test_validate_data_method_explicitly(self):
        dataset = LocalDataset(path=self.test_path, target="target")
        dataset.validate_data()  # Will throw an error if it fails

    def test_create_save_name_method_explicitly(self):
        dataset = LocalDataset(path="local_dataset.csv", target="target")
        dataset.create_save_name()

        assert dataset.save_name == "local_dataset"

    def test_get_data(self):
        dataset = LocalDataset(path=self.test_path, target="target")
        data = dataset.get_data()

        assert isinstance(data, pd.DataFrame)
        assert data.shape == (3, 2)

    def test_get_data_with_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            dataset = LocalDataset(path="invalid_path.csv", target="target")
            dataset.get_data()


class TestKaggleDataset:
    valid_user = "gorororororo23"
    valid_dataset = "plant-growth-data-classification"
    valid_file = "plant_growth_data.csv"

    def test_init(self):
        dataset = KaggleDataset(
            user="some_user",
            dataset="some_dataset",
            file="some_file.csv",
            target="target",
            saveName="testing_kaggle_dataset",
            drop=["col1", "col2"],
            oneHotEncode=["col3"],
        )

        assert dataset.user == "some_user"
        assert dataset.dataset == "some_dataset"
        assert dataset.file == "some_file.csv"
        assert dataset.target == "target"
        assert dataset.save_name == "testing_kaggle_dataset"
        assert dataset.drop == ["col1", "col2"]
        assert dataset.one_hot_encode == ["col3"]

    def test_invalid_user_type(self):
        with pytest.raises(ValidationError):
            KaggleDataset(user=123, dataset="some_dataset", file="some_file.csv", target="target")

    def test_invalid_dataset_type(self):
        with pytest.raises(ValidationError):
            KaggleDataset(user="some_user", dataset=123, file="some_file.csv", target="target")

    def test_invalid_file_type(self):
        with pytest.raises(ValidationError):
            KaggleDataset(user="some_user", dataset="some_dataset", file=123, target="target")

    def test_validate_data_method_explicitly(self):
        dataset = KaggleDataset(
            user="some_user", dataset="some_dataset", file="some_file.csv", target="target"
        )
        dataset.validate_data()  # Will throw an error if it fails

    def test_invalid_file_extension(self):
        with pytest.raises(ValueError):
            dataset = KaggleDataset(user="user", dataset="dataset", file="file", target="target")
            dataset.validate_data()  # Already called at initialization currently

    def test_create_save_name_method_explicitly(self):
        dataset = KaggleDataset(
            user="some_user", dataset="some_dataset", file="some_file.csv", target="target"
        )
        dataset.create_save_name()

        assert dataset.save_name == dataset.user + "_" + dataset.dataset

    def test_get_data(self):
        dataset = KaggleDataset(
            user=self.valid_user,
            dataset=self.valid_dataset,
            file=self.valid_file,
            target="Growth_Milestone",
        )
        data = dataset.get_data()

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0

    def test_get_data_with_invalid_user(self):
        with pytest.raises(ValueError):
            dataset = KaggleDataset(
                user="invalid_user",
                dataset=self.valid_dataset,
                file=self.valid_file,
                target="Growth_Milestone",
            )
            dataset.get_data()

    def test_get_data_with_invalid_dataset(self):
        with pytest.raises(ValueError):
            dataset = KaggleDataset(
                user=self.valid_user,
                dataset="invalid_dataset",
                file=self.valid_file,
                target="Growth_Milestone",
            )
            dataset.get_data()

    def test_get_data_with_invalid_file(self):
        with pytest.raises(FileNotFoundError):
            dataset = KaggleDataset(
                user=self.valid_user,
                dataset=self.valid_dataset,
                file="invalid_file.csv",
                target="Growth_Milestone",
            )
            dataset.get_data()


class TestHuggingFaceDataset:
    valid_repo = "rubend18/ChatGPT-Jailbreak-Prompts"
    valid_file = "dataset.csv"

    def test_init(self):
        dataset = HuggingFaceDataset(
            repo="some_dataset",
            file="train.csv",
            target="target",
            saveName="testing_huggingface_dataset",
            drop=["col1", "col2"],
            oneHotEncode=["col3"],
        )

        assert dataset.repo == "some_dataset"
        assert dataset.file == "train.csv"
        assert dataset.target == "target"
        assert dataset.save_name == "testing_huggingface_dataset"
        assert dataset.drop == ["col1", "col2"]
        assert dataset.one_hot_encode == ["col3"]

    def test_invalid_repo_type(self):
        with pytest.raises(ValidationError):
            HuggingFaceDataset(repo=123, file="train.csv", target="target")

    def test_invalid_file_type(self):
        with pytest.raises(ValidationError):
            HuggingFaceDataset(repo="some_dataset", file=123, target="target")

    def test_create_save_name_method_explicitly(self):
        dataset = HuggingFaceDataset(repo="some_dataset", file="train.csv", target="target")
        dataset.create_save_name()

        assert dataset.save_name == dataset.repo

    def test_get_data(self):
        dataset = HuggingFaceDataset(repo=self.valid_repo, file=self.valid_file, target="target")
        data = dataset.get_data()

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0

    def test_get_data_with_invalid_repo(self):
        with pytest.raises(RepositoryNotFoundError):
            dataset = HuggingFaceDataset(repo="invalid_repo", file=self.valid_file, target="target")
            dataset.get_data()

    def test_get_data_with_invalid_file(self):
        with pytest.raises(EntryNotFoundError):
            dataset = HuggingFaceDataset(repo=self.valid_repo, file="invalid_file.csv", target="target")
            dataset.get_data()


class TestOpenMLDataset:
    valid_id = 31

    def test_init(self):
        dataset = OpenMLDataset(
            id=1,
            target="target",
            saveName="testing_openml_dataset",
            drop=["col1", "col2"],
            oneHotEncode=["col3"],
        )

        assert dataset.id == 1
        assert dataset.target == "target"
        assert dataset.save_name == "testing_openml_dataset"
        assert dataset.drop == ["col1", "col2"]
        assert dataset.one_hot_encode == ["col3"]

    def test_init_without_id(self):
        with pytest.raises(ValidationError):
            OpenMLDataset(target="target")

    def test_invalid_id_type(self):
        with pytest.raises(ValidationError):
            OpenMLDataset(id=1.5, target="target")

    def test_get_data(self):
        dataset = OpenMLDataset(id=self.valid_id, target="target")
        data = dataset.get_data()

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0

    def test_get_data_with_invalid_id(self):
        with pytest.raises(OpenMLServerException):
            dataset = OpenMLDataset(id=999999, target="target")
            dataset.get_data()

    def test_get_data_with_negative_id(self):
        with pytest.raises(OpenMLServerException):
            dataset = OpenMLDataset(id=-1, target="target")
            dataset.get_data()

    def test_create_save_name_explicitly(self):
        dataset = OpenMLDataset(id=self.valid_id, target="target")

        dataset.create_save_name()
        assert dataset.save_name == f"openml_dataset_{self.valid_id}"


# Init tests implicitly test the ParamsReader class as well
class TestDatasetFactory:
    test_path = Path("local_dataset.csv")
    test_path_string = "local_dataset.csv"
    create_csv_file(test_path)
    local_params_list = [
        {
            "type": "local",
            "path": "local_dataset.csv",
            "target": "target",
        }
    ]
    kaggle_params_list = [
        {
            "type": "kaggle",
            "user": "user1",
            "dataset": "dataset1",
            "file": "file1.csv",
            "target": "target",
        },
        {
            "type": "kaggle",
            "user": "user2",
            "dataset": "dataset2",
            "file": "file2.csv",
            "target": "target",
        },
    ]
    hugging_face_params_list = [
        {
            "type": "huggingface",
            "repo": "repo1",
            "file": "file1.csv",
            "target": "target",
        },
        {
            "type": "huggingface",
            "repo": "repo2",
            "file": "file2.csv",
            "target": "target",
        },
    ]
    openml_params_list = [
        {
            "type": "openml",
            "id": 31,
            "target": "target",
        },
        {
            "type": "openml",
            "id": 2,
            "target": "target",
        },
    ]
    mixed_params_list = [
        {
            "type": "kaggle",
            "user": "user1",
            "dataset": "dataset1",
            "file": "file1.csv",
            "target": "target",
        },
        {
            "type": "kaggle",
            "user": "user2",
            "dataset": "dataset2",
            "file": "file2.csv",
            "target": "target",
        },
        {
            "type": "local",
            "path": "local_dataset.csv",
            "target": "target",
        },
        {
            "type": "huggingface",
            "repo": "repo1",
            "file": "file1.csv",
            "target": "target",
        },
        {
            "type": "huggingface",
            "repo": "repo2",
            "file": "file2.csv",
            "target": "target",
        },
        {
            "type": "openml",
            "id": 31,
            "target": "target",
        },
        {
            "type": "openml",
            "id": 2,
            "target": "target",
        },
    ]

    def test_init_local_dataset(self):
        DatasetFactory(self.local_params_list)

    def test_create_local_dataset_directly(self):
        dataset = DatasetFactory(self.local_params_list)
        local_dataset = dataset.create(**self.local_params_list[0])
        assert isinstance(local_dataset, LocalDataset)

    def test_iter_local_datasets(self):
        dataset_count = 0
        factory = DatasetFactory(self.local_params_list)

        for dataset in factory:
            dataset_count += 1
            assert isinstance(dataset, LocalDataset)
        assert dataset_count == len(self.local_params_list)

    def test_iter_kaggle_datasets(self):
        dataset_count = 0
        factory = DatasetFactory(self.kaggle_params_list)

        for dataset in factory:
            dataset_count += 1
            assert isinstance(dataset, KaggleDataset)
        assert dataset_count == len(self.kaggle_params_list)

    def test_iter_huggingface_datasets(self):
        dataset_count = 0
        factory = DatasetFactory(self.hugging_face_params_list)

        for dataset in factory:
            dataset_count += 1
            assert isinstance(dataset, HuggingFaceDataset)
        assert dataset_count == len(self.hugging_face_params_list)

    def test_iter_openml_datasets(self):
        dataset_count = 0
        factory = DatasetFactory(self.openml_params_list)

        for dataset in factory:
            dataset_count += 1
            assert isinstance(dataset, OpenMLDataset)
        assert dataset_count == len(self.openml_params_list)

    def test_iter_mixed_datasets(self):
        dataset_count = 0
        datasets = DatasetFactory(self.mixed_params_list)

        for dataset in datasets:
            dataset_count += 1
            assert isinstance(dataset, (LocalDataset, KaggleDataset, HuggingFaceDataset, OpenMLDataset))
        assert dataset_count == len(self.mixed_params_list)

    def test_invalid_type(self):
        with pytest.raises(ValueError):
            params_list = [
                {
                    "type": "invalid",
                    "file": "local_dataset.csv",
                    "target": "target",
                },
            ]
            datasets = DatasetFactory(params_list)
            for dataset in datasets:
                pass

    def test_invalid_type_type(self):
        with pytest.raises(ValueError):
            params_list = [
                {
                    "type": 123,
                    "file": "local_dataset.csv",
                    "target": "target",
                },
            ]
            datasets = DatasetFactory(params_list)
            for dataset in datasets:
                pass


def test_remove_csv_file() -> None:
    file_path = "local_dataset.csv"
    os.remove(file_path)
