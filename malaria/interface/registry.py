''' This is the wagon code'''

import glob
import os
import time
import pickle
from colorama import Fore, Style
from tensorflow import keras
from taxifare.params import *
import mlflow
from mlflow.tracking import MlflowClient

def save_results(params: dict, metrics: dict) -> None:
    """
    Persist params & metrics locally on hard drive at
    "{LOCAL_REGISTRY_PATH}/params/{current_timestamp}.pickle"
    "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    - (unit 03 only) if MODEL_TARGET='mlflow', also persist them on mlflow
    """
    if MODEL_TARGET == "mlflow":
        # $CHA_BEGIN
        if params is not None:
            mlflow.log_params(params)
        if metrics is not None:
            mlflow.log_metrics(metrics)
        print("✅ Results saved on mlflow")
        # $CHA_END

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # save params locally
    if params is not None:
        params_path = os.path.join(LOCAL_REGISTRY_PATH, "params", timestamp + ".pickle")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics locally
    if metrics is not None:
        metrics_path = os.path.join(LOCAL_REGISTRY_PATH, "metrics", timestamp + ".pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    print("✅ Results saved locally")


def save_model(model: keras.Model = None) -> None:
    """
    Persist trained model locally on hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it on your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on mlflow instead of GCS (for unit 0703 only) --> unit 03 only
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # save model locally
    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", f"{timestamp}.h5")
    model.save(model_path)

    print("✅ Model saved locally")

    if MODEL_TARGET == "gcs":
        # 🎁 We give you this piece of code as a gift. Please read it carefully! Add breakpoint if you need!
        from google.cloud import storage

        model_filename = model_path.split("/")[-1] # e.g. "20230208-161047.h5" for instance
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"models/{model_filename}")
        blob.upload_from_filename(model_path)

        print("✅ Model saved to gcs")
        return None

    if MODEL_TARGET == "mlflow":
        # $CHA_BEGIN
        mlflow.tensorflow.log_model(model=model,
                                artifact_path="model",
                                registered_model_name=MLFLOW_MODEL_NAME
                                )
        print("✅ Model saved to mlflow")

        return None
        # $CHA_END

    return None


def load_model(stage="Production") -> keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model found

    """

    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)
        # Get latest model version name by timestamp on disk
        local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
        local_model_paths = glob.glob(f"{local_model_directory}/*")
        if not local_model_paths:
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]
        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)
        lastest_model = keras.models.load_model(most_recent_model_path_on_disk)
        print("✅ model loaded from local disk")

        return lastest_model

    elif MODEL_TARGET == "gcs":
        # 🎁 We give you this piece of code as a gift. Please read it carefully! Add breakpoint if you need!
        print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

        from google.cloud import storage
        client = storage.Client()
        blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))
        try:
            latest_blob = max(blobs, key=lambda x: x.updated)
            latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, latest_blob.name)
            latest_blob.download_to_filename(latest_model_path_to_save)
            latest_model = keras.models.load_model(latest_model_path_to_save)
            print("✅ Latest model downloaded from cloud storage")
            return latest_model
        except:
            print(f"\n❌ No model found on GCS bucket {BUCKET_NAME}")
            return None

    elif MODEL_TARGET == "mlflow":

        print(Fore.BLUE + f"\nLoad model {stage} stage from mlflow..." + Style.RESET_ALL)

        # load model from mlflow
        model = None
        # $CHA_BEGIN
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        client = MlflowClient()
        try:
            model_versions = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[stage])
            model_uri = model_versions[0].source
            assert model_uri is not None
        except:
            print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {stage}")
            return None

        model = mlflow.tensorflow.load_model(model_uri=model_uri)

        print("✅ model loaded from mlflow")
        # $CHA_END
        return model

    else:
        return None



def mlflow_transition_model(current_stage: str, new_stage: str) -> None:
    """
    Transition the latest model from current_stage stage to new_stage and archive the existing model in new_stage
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient()

    version = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[current_stage])

    if not version:
        print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {current_stage}")
        return None

    client.transition_model_version_stage(
        name=MLFLOW_MODEL_NAME,
        version=version[0].version,
        stage=new_stage,
        archive_existing_versions=True
    )

    print(f"✅ Model {MLFLOW_MODEL_NAME} version {version[0].version} transitioned from {current_stage} to {new_stage}")

    return None


def mlflow_run(func):
    """Generic function to log params and results to mlflow along with tensorflow autologging

    Args:
        func (function): Function you want to run within mlflow run
        params (dict, optional): Params to add to the run in mlflow. Defaults to None.
        context (str, optional): Param describing the context of the run. Defaults to "Train".
    """
    def wrapper(*args, **kwargs):
        mlflow.end_run()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT)
        with mlflow.start_run():
            mlflow.tensorflow.autolog()
            results = func(*args, **kwargs)
        print("✅ mlflow_run autolog done")
        return results
    return wrapper
