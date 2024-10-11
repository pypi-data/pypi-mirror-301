from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import ModelCreateBody
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class Model(EasyMakerBaseModel):
    model_id: Optional[str] = None
    model_name: Optional[str] = None  # TODO. model_name이 BaseModel 예약어라 충돌이나는데 어떻게 처리할지 확인 필요
    model_status_code: Optional[str] = None
    training: Optional[Any] = None
    hyperparameter_tuning: Optional[Any] = None
    framework_version: Optional[str] = None
    model_type_code: Optional[str] = None
    model_upload_uri: Optional[str] = None

    def __init__(self, model_id: str = None):
        if model_id:
            response = easymaker.easymaker_config.api_sender.get_model_by_id(model_id)
            super().__init__(**response)

    def create(
        self,
        model_name: str,
        training_id: Optional[str] = None,
        hyperparameter_tuning_id: Optional[str] = None,
        model_description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
    ):
        """
        Args:
            model_name (str): Experiment name
            training_id (str): Training ID
            hyperparameter_tuning_id (str): Hyperparameter Tuning ID
            model_description (str): Experiment description
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                training_id=training_id,
                hyperparameter_tuning_id=hyperparameter_tuning_id,
                description=model_description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def create_by_model_upload_uri(
        self,
        model_name: str,
        model_type_code: Optional[str] = None,
        model_upload_uri: Optional[str] = None,
        model_description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
    ):
        """
        Args:
            model_name (str): Experiment name
            model_type_code (str): easymaker.TENSORFLOW or easymaker.PYTORCH or easymaker.SCIKIT_LEARN
            model_upload_uri (str): model upload uri (NHN Cloud Object Storage or NAS)
            model_description (str): Experiment description
            parameter_list (list): model parameter list
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                model_type_code=model_type_code,
                model_upload_uri=model_upload_uri,
                description=model_description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def create_hugging_face_model(
        self,
        model_name: str,
        model_description: Optional[str] = None,
        parameter_list: Optional[List[Any]] = None,
        tag_list: Optional[List[Any]] = None,
    ):
        """
        Args:
            model_name (str): Experiment name
            parameter_list (list): model parameter list
            model_description (str): Experiment description
            tag_list (list): tags
        Returns:
            Model
        """
        response = easymaker.easymaker_config.api_sender.create_model(
            ModelCreateBody(
                model_name=model_name,
                model_type_code=easymaker.HUGGING_FACE,
                description=model_description,
                parameter_list=parameter_list,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        print(f"[AI EasyMaker] Model create complete. model_id: {self.model_id}")
        return self

    def delete(self):
        if self.model_id:
            easymaker.easymaker_config.api_sender.delete_model_by_id(self.model_id)
            super().__init__()


def delete(model_id: str):
    if model_id:
        easymaker.easymaker_config.api_sender.delete_model_by_id(model_id)
