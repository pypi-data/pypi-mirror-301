import json
import logging
import os
import time
import zipfile
import hashlib
import math
import requests
import re
import datetime
from pathlib import Path

# BACKEND_API_URI = "https://backend-api.scref.phenomic.ai"
BACKEND_API_URI = "http://127.0.0.1:5000"
CHUNK_SIZE = 2**20  # 1 Megabyte

# https://docs.hdfgroup.org/hdf5/v1_14/_f_m_t3.html#Superblock
H5AD_SIGNATURE = bytes.fromhex("894844460d0a1a0a")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
)
logger = logging.getLogger(__name__)


class PaiEmbeddings:
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

    def download_example_h5ad(self):
        logger.info("Downloading example h5ad")
        url = BACKEND_API_URI + "/download_example_h5ad"

        response = requests.get(url)

        adatas_dir = os.path.join(self.tmp_dir, "adatas")
        if not os.path.exists(adatas_dir):
            os.mkdir(adatas_dir)

        file_path = os.path.join(adatas_dir, "anndata_example.h5ad")
        with open(file_path, "wb") as binary_file:
            binary_file.write(response.content)

    def inference(self, h5ad_path, tissue_organ, output_dir=None, model=None, umap_exclude=False):
        assert h5ad_path.endswith(".h5ad")
        assert os.path.exists(h5ad_path)

        h5ad_file_name = re.match(".*\/(.+)\.h5ad", h5ad_path).group(1)

        job_id = self.upload_h5ad(h5ad_path, tissue_organ, model, umap_exclude)
        self.listen_job_status(job_id)
        self.download_job(job_id, h5ad_file_name, tissue_organ, output_dir)

    def get_upload_uuid(self, size, chunks, model):
        logger.info("Getting upload id")
        url = BACKEND_API_URI + "/start_upload"

        home = Path.home()
        path = os.path.join(home, ".pai/credentials")
        if os.path.exists(path):
            with open(path, "r") as fh:
                credentials = fh.read()
            api_key = re.match("(\[\w+\]\n)?(pai_api_key)(\s)?=(\s)?(\w+)(\n)?", credentials).group(5)
        else:
            api_key = None

        body = {"size": size, "chunk_count": chunks, "model": model, "api_key": api_key}
        response = requests.post(url, json=body)

        if response.ok:
            self.upload_uuid = json.loads(response.json())["uuid"]
            logger.info(f"Recieved uuid: {self.upload_uuid}")
        elif response.status_code == 401:
            raise Exception(response.status_code, response.reason)
        else:
            raise Exception("Upload uuid not recieved", response)

    def upload_chunks(self, chunks, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as file:
            for i in chunks:
                chunk = file.read(CHUNK_SIZE)
                hash_md5.update(chunk)
                response = requests.post(
                    BACKEND_API_URI + "/upload_chunk",
                    data={"chunk_id": i, "uuid": self.upload_uuid},
                    files={"file": chunk},
                )
        return hash_md5.hexdigest()

    def upload_h5ad(self, h5ad_path, tissue_organ, model, umap_exclude):
        logger.info("Checking destination folders...")

        zips_dir = os.path.join(self.tmp_dir, "zips")
        if not os.path.exists(zips_dir):
            os.mkdir(zips_dir)

        results_dir = os.path.join(self.tmp_dir, "results")
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)

        logger.info("Uploading h5ad file...")
        size = os.path.getsize(h5ad_path)
        chunks = math.ceil(size / CHUNK_SIZE)
        self.get_upload_uuid(size, chunks, model)

        check_h5ad_signature(h5ad_path)
        hash = self.upload_chunks(range(chunks), h5ad_path)
        job_data = {
            "uuid": self.upload_uuid,
            "hash": hash,
            "tissueOrgan": tissue_organ,
            "model": model,
            "umap_exclude": umap_exclude
        }
        response = requests.post(
            BACKEND_API_URI + "/upload_status",
            json=job_data,
        )

        if response.status_code == 200:
            job_id = json.loads(response.content)["id"]
            logger.info(f"Upload complete, job id: {job_id}")
            return job_id
        elif response.status_code == 201:
            # TODO Handle missing chunks
            pass
        else:
            raise Exception(response.status_code, response.reason)

    def get_job_status(self, job_id):
        url = BACKEND_API_URI + "/job"  # TODO
        params = {"job_id": job_id}

        response = requests.get(url, params=params)

        if response.status_code >= 200 and response.status_code < 300:
            response_content = json.loads(response.content)
            status = response_content["status"]
            logger.info(f"Job status: {status}")
            if status in ["VALIDATION ERROR", "ERROR"]:
                error = response_content["error"]
                logger.info(error)
            return status
        else:
            raise Exception(response.status_code, response.reason)

    def listen_job_status(self, job_id):
        logger.info("Listening for job status")
        while True:
            status = self.get_job_status(job_id)
            if status in ["SUBMITTED", "VALIDATING", "RUNNING"]:
                time.sleep(10)  # sleep 10s
                continue
            elif status in ["VALIDATION ERROR", "ERROR", "FAILED", "COMPLETED"]:
                break
            else:
                break  # belt and braces

    def download_job(self, job_id, h5ad_file_name, tissue_organ, output_dir):
        logger.info("Downloading job")
        url = BACKEND_API_URI + "/download"
        data = {"job_id": job_id}

        response = requests.post(url, json=data)

        zips_dir = os.path.join(self.tmp_dir, "zips")
        results_dir = os.path.join(self.tmp_dir, "results")

        if not output_dir:
            tissue_organ = tissue_organ.replace(" ", "-")
            datetime_ = datetime.datetime.now().strftime("%Y-%m-%d-T%H:%M:%S")
            output_dir = f"{h5ad_file_name}-{tissue_organ}-{datetime_}"

        zip_path = os.path.join(zips_dir, f"{output_dir}.zip")  # zip_file_name is equal to output_dir
        job_dir = os.path.join(results_dir, output_dir)

        with open(zip_path, "wb") as binary_file:
            binary_file.write(response.content)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(job_dir)


def check_h5ad_signature(file_path):
    with open(file_path, "rb") as file:
        signature = file.read(8)
        if signature != H5AD_SIGNATURE:
            logger.error("H5AD Signature mismatch")
            raise Exception("H5AD file does not match signature")

        # TODO consider option to cleanup zip file
