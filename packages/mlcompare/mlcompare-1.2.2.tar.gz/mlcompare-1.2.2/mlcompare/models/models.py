from __future__ import annotations as _annotations

import inspect
import logging
import pickle
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import Any, Generator, Literal, TypeAlias

import pandas as pd
from pydantic import BaseModel

from ..params_reader import ParamsInput, ParamsReader

logger = logging.getLogger(__name__)

LibraryNames: TypeAlias = Literal[
    "sklearn",
    "scikit-learn",
    "skl",
    "xgboost",
    "xgb",
    "pytorch",
    "torch",
    "tensorflow",
    "tf",
]


class LibraryModel(ABC, BaseModel):
    name: str
    module: str | None = None
    params: dict | None = None
    _library: Literal["sklearn", "xgboost", "torch", "tensorflow"]
    _ml_model: Any = None
    """
    A base class for models from different machine learning libraries.

    Attributes:
    -----------
        name (str): Class name of the model. Ex: RandomForestRegressor.
        module (str | None): Module containing the model class if it's not imported at the library level.
        params (dict | None): Parameters to pass to the model class constructor if any.
        _ml_model (Any): Model object instantiated from the library, accessed by the `train` and `predict` methods.
    """

    @abstractmethod
    def model_post_init(self, Any) -> None: ...

    @abstractmethod
    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame | pd.Series) -> None: ...

    @abstractmethod
    def predict(self, X_test: pd.DataFrame): ...

    def save(self, save_directory: Path):
        save_file = save_directory / f"{self.name}.pkl"
        with open(save_file, "wb") as file:
            pickle.dump(self._ml_model, file)

    def resolve_model_submodule(self) -> Any | None:
        imported_library = import_module(self._library)
        library_modules = imported_library.__all__

        for module_name in library_modules:
            try:
                module = import_module(f"{imported_library.__name__}.{module_name}")
                for class_name, obj in inspect.getmembers(module, inspect.isclass):
                    if class_name == self.name:
                        logger.info(f"{self.name} found in module: {module_name}.")
                        return obj
            except Exception:
                pass
        return None

    def instantiate_model(self) -> None:
        if self.module:
            full_import = f"{self._library}.{self.module}"
        else:
            full_import = self._library

        try:
            model_module = import_module(full_import)
        except ImportError:
            logger.error(
                f"Could not import module {full_import}. Check that you have {self._library} "
                "installed or that the module name is spelled correctly."
            )
            raise

        # Get the model class from the module. If it fails and no module was given, try to find the class within submodules.
        try:
            model_class = getattr(model_module, self.name)
        except AttributeError:
            if self.module:
                logger.error(f"Could not find class: {self.name} in module: {self.module}.")
                raise
            else:
                logger.info(f"Searching {self._library} submodules for {self.name}.")
                model_class = self.resolve_model_submodule()
                if not model_class:
                    raise ImportError(
                        f"Could not find class {self.name} in any {self._library} submodules. Please provide a "
                        "module for the model within the config i.e. 'module': 'ensemble'."
                    )

        # Initialize the model with the given parameters
        try:
            if self.params:
                ml_model = model_class(**self.params)
            else:
                ml_model = model_class()
        except Exception:
            logger.error(f"Could not initialize model {self.name} with params {self.params}")
            raise

        self._ml_model = ml_model


class SklearnModel(LibraryModel):
    """
    A class used to instantiate and manage a Scikit-learn model.

    Attributes:
    -----------
        name (str): Class name of the model. Ex: RandomForestRegressor.
        module (str | None): Module containing the model class if it's not imported at the library level.
        params (dict | None): Parameters to pass to the model class constructor if any.
    """

    _library = "sklearn"

    def model_post_init(self, Any) -> None:
        self.instantiate_model()

    def train(self, X_train, y_train) -> None:
        self._ml_model.fit(X_train, y_train)

    def predict(self, X_test):
        return self._ml_model.predict(X_test)


class XGBoostModel(LibraryModel):
    """
    A class used to instantiate and manage an XGBoost model.

    Attributes:
    -----------
        name (str): Class name of the model. Ex: XGBRegressor.
        module (str | None): Module containing the model class if it's not imported at the library level.
        params (dict | None): Parameters to pass to the model class constructor if any.
    """

    _library = "xgboost"

    def model_post_init(self, Any) -> None:
        self.instantiate_model()

    def train(self, X_train, y_train) -> None:
        self._ml_model.fit(X_train, y_train)

    def predict(self, X_test):
        return self._ml_model.predict(X_test)


class PyTorchModel(LibraryModel):
    """
    A class used to instantiate and manage a PyTorch model.

    Attributes:
    -----------
        name (str): Class name of the model. Ex: LSTM.
        module (str | None): Module containing the model class if it's not imported at the library level.
        params (dict | None): Parameters to pass to the model class constructor if any.
    """

    _library = "torch"
    device: Literal["cuda", "mps", "cpu"] | None = None
    activation: str
    loss: str
    optimizer: str = "Adam"
    batch_size: int = 32
    epochs: int = 100

    def model_post_init(self, Any) -> None:
        import torch

        self.instantiate_model()
        if self.device is None:
            self.set_device()
        else:
            assert isinstance(self.device, torch.device)

    def train(self, X_train, y_train) -> None:
        self._ml_model.fit(X_train, y_train)

    def predict(self, X_test):
        return self._ml_model.predict(X_test)

    def set_device(self) -> None:
        import torch

        if self.device is not None:
            match self.device:
                case "cuda":
                    self._torch_device = torch.device("cuda")
                case "mps":
                    self._torch_device = torch.device("mps")
                case "cpu":
                    self._torch_device = torch.device("cpu")
                case _:
                    raise ValueError("Device must be one of 'cuda', 'mps', or 'cpu'.")
        else:
            if torch.cuda.is_available():
                self._torch_device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self._torch_device = torch.device("mps")
            else:
                self._torch_device = torch.device("cpu")

        logger.info(f"Pytorch device type set to: {self._torch_device.type}")


class TensorflowModel(LibraryModel):
    """
    A class used to instantiate and manage an TensorFlow model.

    Attributes:
    -----------
        name (str): Class name of the model. Ex: XGBRegressor.
        module (str | None): Module containing the model class if it's not imported at the library level.
        params (dict | None): Parameters to pass to the model class constructor if any.
        _ml_model (Any): Instantiated machine learning model, accessed by the `train` and `predict` methods.
    """

    _library = "tensorflow"
    activation: str
    loss: str
    optimizer: str = "Adam"
    epochs: int = 100

    def model_post_init(self, Any):
        self.instantiate_model()

    def train(self, X_train, y_train):
        self._ml_model.fit(X_train, y_train)

    def predict(self, X_test):
        return self._ml_model.predict(X_test)


MLModelType: TypeAlias = SklearnModel | XGBoostModel | PyTorchModel


class ModelFactory:
    """
    Takes in a list of dictionaries and constructs model classes based on the `library` keyword provided for each.
    The class is designed to be iterated over.

    Attributes:
    -----------
        params_list (list[dict[str, Any]] | str | Path): List of dictionaries containing dataset parameters or a path to
        a .json file with one. For a list of keys required in each dictionary, see below:

        Required keys:
        - `library` (Literal["sklearn", "xgboost", "pytorch", "tensorflow", "custom"]): The library to use.
        - `module` (str): Module containing the model class.
        - `name` (str): Name of the model class.

        Optional keys:
        - `params` (dict | None): The parameters to pass to the model class constructor

    Raises:
    -------
        AssertionError: If `dataset_params` is not a list of dictionaries or a path to a .json file containing one.
    """

    def __init__(self, params_list: ParamsInput) -> None:
        self.params_list = ParamsReader.read(params_list)

    def __iter__(self) -> Generator[MLModelType, None, None]:
        """
        Makes the class iterable, yielding dataset instances one by one.

        Yields:
        -------
            MLModelType: Instance of a LibraryModel child class.
        """
        for params in self.params_list:
            yield ModelFactory.create(**params)

    @staticmethod
    def create(library: LibraryNames, **kwargs) -> MLModelType:
        """
        Factory method to create a dataset instance based on the dataset type.

        Args:
        -----
            library (LibraryNames): Type of dataset to create.
            **kwargs: Arbitrary keyword arguments to be passed to the dataset class constructor.

        Returns:
        --------
            BaseDataset: An instance of a dataset class (KaggleDataset or LocalDataset).

        Raises:
        -------
            ValueError: If an unknown dataset type is provided.
        """
        assert isinstance(library, str), "Library must be a string."
        library = library.lower()  # type: ignore

        match library:
            case "sklearn" | "scikit-learn" | "skl":
                return SklearnModel(**kwargs)
            case "xgboost" | "xgb":
                return XGBoostModel(**kwargs)
            case "pytorch" | "torch":
                return PyTorchModel(**kwargs)
            case _:
                raise ValueError(
                    f"Library: {library} is not supported. Valid library names "
                    "are: 'sklearn', 'xgboost', 'pytorch', or 'tensorflow'. If your model is not "
                    "in one of these libraries use 'custom' and provide a value for 'custom_function' "
                    "that takes in train-test split data and returns an nd.array or pd.Series of "
                    "predictions. See the documentation for more details."
                )
