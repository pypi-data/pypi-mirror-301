from PIL import Image, ImageChops, ImageStat
import pytest
import psycopg
from psycopg.sql import SQL
import os
import re
import time
import typing
from typing import Dict, List, Any
from pathlib import Path
import shutil
from dataclasses import dataclass, field
from contextlib import contextmanager
import functools
from geovisio import create_app, db_migrations, tokens
from geovisio.utils import filesystems
from geovisio.workers import runner_pictures


@pytest.fixture(scope="session")
def dburl():
    # load test.env file if available
    import dotenv

    dotenv.load_dotenv("test.env")

    db = os.environ["DB_URL"]

    db_migrations.update_db_schema(db, force=True)
    return db


def prepare_fs(base_dir):
    fstmp = base_dir / "tmp"
    fstmp.mkdir()
    fspermanent = base_dir / "permanent"
    fspermanent.mkdir()
    fsderivates = base_dir / "derivates"
    fsderivates.mkdir()
    return filesystems.FilesystemsURL(
        tmp="osfs://" + str(fstmp), permanent="osfs://" + str(fspermanent), derivates="osfs://" + str(fsderivates)
    )


@pytest.fixture
def fsesUrl(tmp_path):
    return prepare_fs(tmp_path)


@contextmanager
def create_test_app(config):
    app = create_app(config)
    with app.app_context():
        yield app

    app.pool.close()


@pytest.fixture
def app(dburl, tmp_path, fsesUrl):
    with create_test_app(
        {
            "TESTING": True,
            "DB_URL": dburl,
            "FS_URL": None,
            "FS_TMP_URL": fsesUrl.tmp,
            "FS_PERMANENT_URL": fsesUrl.permanent,
            "FS_DERIVATES_URL": fsesUrl.derivates,
            "SERVER_NAME": "localhost:5000",
            "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
            "SECRET_KEY": "a very secret key",
            "API_PICTURES_LICENSE_SPDX_ID": "etalab-2.0",
            "API_PICTURES_LICENSE_URL": "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/LICENSE",
        }
    ) as app:
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# Code for having at least one sequence in tests
FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

SEQ_IMG = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
SEQ_IMG_FLAT = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "c1.jpg"))
SEQ_IMG_ARTIST = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "e1_artist.jpg"))
SEQ_IMG_CROP = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "crop.jpg"))

SEQ_IMGS = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "1.jpg"),
    os.path.join(FIXTURE_DIR, "2.jpg"),
    os.path.join(FIXTURE_DIR, "3.jpg"),
    os.path.join(FIXTURE_DIR, "4.jpg"),
    os.path.join(FIXTURE_DIR, "5.jpg"),
)

SEQ_IMGS_FLAT = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"), os.path.join(FIXTURE_DIR, "b2.jpg"))

SEQ_IMGS_NOHEADING = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "e4.jpg"),
    os.path.join(FIXTURE_DIR, "e5.jpg"),
)

SEQ_IMG_BLURRED = pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1_blurred.jpg"))
MOCK_BLUR_API = "https://geovisio-blurring.net"


def app_with_data(app, sequences: Dict[str, List[Path]], jwtToken=None):
    with app.app_context():
        with app.test_client() as client:
            for title, pics_path in sequences.items():
                uploadSequenceFromPics(test_client=client, title=title, wait=True, jwtToken=jwtToken, pics=pics_path)

            return client


@pytest.fixture
def initSequenceApp(tmp_path, dburl, fsesUrl, bobAccountToken):
    seqPath = tmp_path / "seq1"
    seqPath.mkdir()

    @contextmanager
    def fct(datafiles, preprocess=True, blur=False, withBob=False):
        twoSeqs = os.path.isfile(datafiles / "1.jpg") and os.path.isfile(datafiles / "b1.jpg")

        if twoSeqs:
            seq2Path = tmp_path / "seq2"
            seq2Path.mkdir()
            for f in os.listdir(datafiles):
                if f not in ["seq1", "seq2", "1_blurred.jpg", "tmp", "derivates", "permanent"]:
                    os.rename(datafiles / f, (seq2Path if f[0:1] == "b" else seqPath) / re.sub("^[a-z]+", "", f))
        else:
            for f in os.listdir(datafiles):
                if f not in ["seq1", "1_blurred.jpg", "tmp", "derivates", "permanent"]:
                    os.rename(datafiles / f, seqPath / re.sub("^[a-z]+", "", f))
        with create_test_app(
            {
                "TESTING": True,
                "API_BLUR_URL": MOCK_BLUR_API if blur else "",
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "PREPROCESS" if preprocess else "ON_DEMAND",
                "DB_URL": dburl,
                "FS_URL": None,
                "FS_TMP_URL": fsesUrl.tmp,
                "FS_PERMANENT_URL": fsesUrl.permanent,
                "FS_DERIVATES_URL": fsesUrl.derivates,
                "SECRET_KEY": "cest beau la vie",
                "SERVER_NAME": "localhost:5000",
                "API_FORCE_AUTH_ON_UPLOAD": "true" if withBob else None,
            }
        ) as app:
            with app.test_client() as client:
                jwtToken = None
                if withBob:
                    jwtToken = bobAccountToken()

                uploadSequence(client, tmp_path / "seq1", jwtToken=jwtToken)
                if twoSeqs:
                    uploadSequence(client, tmp_path / "seq2", jwtToken=jwtToken)

                yield client

    return fct


def createSequence(test_client, title, jwtToken=None) -> str:
    headers = {}
    if jwtToken:
        headers["Authorization"] = "Bearer " + jwtToken

    seq = test_client.post(
        "/api/collections",
        headers=headers,
        data={
            "title": title,
        },
    )
    assert seq.status_code < 400
    return seq.headers["Location"]


def uploadPicture(test_client, sequence_location, pic, filename, position, isBlurred=False, jwtToken=None, overrides=None) -> str:
    postData = {"position": position, "picture": (pic, filename)}

    if isBlurred:
        postData["isBlurred"] = "true"

    if overrides:
        postData.update(overrides)

    headers = {}
    if jwtToken:
        headers["Authorization"] = "Bearer " + jwtToken

    picture_response = test_client.post(f"{sequence_location}/items", headers=headers, data=postData, content_type="multipart/form-data")
    assert picture_response.status_code < 400, picture_response.text
    return picture_response.json["id"]


def uploadSequenceFromPics(test_client, title: str, pics: List[Path], wait=True, jwtToken=None):
    seq_location = createSequence(test_client, title, jwtToken=jwtToken)

    for i, p in enumerate(pics):
        uploadPicture(test_client, seq_location, open(p, "rb"), p.name, i + 1, jwtToken=jwtToken)

    if wait:
        waitForSequence(test_client, seq_location)


def uploadSequence(test_client, directory, wait=True, jwtToken=None):
    seq_location = createSequence(test_client, os.path.basename(directory), jwtToken=jwtToken)

    pictures_filenames = sorted([f for f in os.listdir(directory) if re.search(r"\.jpe?g$", f, re.IGNORECASE)])

    for i, p in enumerate(pictures_filenames):
        uploadPicture(test_client, seq_location, open(directory / p, "rb"), p, i + 1, jwtToken=jwtToken)

    if wait:
        waitForSequence(test_client, seq_location)


def waitForSequence(test_client, seq_location):
    return waitForSequenceState(
        test_client,
        seq_location,
        wanted_state=lambda s: all(p["status"] == "ready" for p in s.json["items"]) and s.json["status"] == "ready",
    )


def waitForSequenceState(test_client, seq_location, wanted_state) -> Dict[str, Any]:
    """
    Wait for a sequence to have a given state
    `wanted_state` should be a function returning true when the sequence state is the one wanted
    """

    def _call_seq_status(test_client, seq_location, wanted_state):
        s = test_client.get(f"{seq_location}/geovisio_status")
        assert s.status_code < 400

        final_state = {p["rank"]: p["status"] for p in s.json["items"]} | {"sequence_status": s.json["status"]}

        return wanted_state(s), final_state

    return waitFor(lambda: _call_seq_status(test_client, seq_location, wanted_state), timeout=10)


def waitForUploadSetState(test_client, upload_set_id, wanted_state, timeout=5) -> Dict[str, Any]:
    """
    Wait for an upload_set to have a given state
    `wanted_state` should be a function returning true when the sequence state is the one wanted
    """

    def _call_upload_set(test_client, upload_set_id, wanted_state):
        s = test_client.get(f"/api/upload_sets/{upload_set_id}")
        assert s.status_code < 400

        return wanted_state(s), s.json

    return waitFor(lambda: _call_upload_set(test_client, upload_set_id, wanted_state), timeout=timeout)


def waitForUploadSetStateReady(test_client, upload_set_id, timeout=5) -> Dict[str, Any]:
    """
    Wait for an upload_set to be ready (dispatched, and all pictures prepared)
    """
    return waitForUploadSetState(test_client, upload_set_id, wanted_state=lambda x: x.json["ready"] is True, timeout=timeout)


def waitFor(function, *, timeout=5) -> Dict[str, Any]:
    """
    Wait for an upload_set to have a given state
    `wanted_state` should be a function returning true when the sequence state is the one wanted
    """
    waiting_time = 0.1
    total_time = 0
    state = {}
    while total_time < timeout:
        stop, state = function()
        if stop:
            return state
        time.sleep(waiting_time)
        total_time += waiting_time
    assert False, f"Wait for has not reached wanted state, final state = {state}"


def waitForAllJobsDone(app, timeout=5):
    def _all_jobs_done():
        from geovisio.utils import db

        jobs = db.fetchall(app, SQL("SELECT * FROM job_queue"))
        return jobs == [], jobs

    waitFor(_all_jobs_done, timeout=timeout)


def start_background_worker(dburl, tmp_path, config, wait=True):
    import threading

    def pic_background_process():
        with create_test_app(config) as worker_app:
            import logging

            logging.info("Running picture worker in test")
            worker = runner_pictures.PictureProcessor(app=worker_app, stop=True)
            worker.process_jobs()
            return

    t = threading.Thread(target=pic_background_process, daemon=True)

    t.start()

    if wait:
        t.join()
    else:
        return t


@pytest.fixture(autouse=True)
def dbCleanup(dburl):
    with psycopg.connect(dburl, options="-c statement_timeout=5000") as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """TRUNCATE TABLE sequences, sequences_pictures, pictures, job_queue, pictures_changes, sequences_changes, upload_sets, excluded_areas CASCADE;"""
            )


@pytest.fixture(autouse=True)
def wait_for_jobs_completion(dburl):
    """At end of test, wait a bit for all background jobs to be processed
    We do this by removing all rows from the job queue, and that will be possible only if no worker has locked a given job
    """
    yield
    with psycopg.connect(dburl, options="-c statement_timeout=2000") as conn:
        conn.execute("DELETE FROM job_queue")


@pytest.fixture(autouse=True)
def datafilesCleanup(datafiles):
    yield
    for filename in os.listdir(datafiles):
        file_path = os.path.join(datafiles, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            pass


@pytest.fixture()
def defaultAccountID(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("SELECT id from accounts where is_default = true").fetchone()
            assert accountID
            accountID = accountID[0]
    return accountID


@pytest.fixture()
def bobAccountID(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("SELECT id from accounts WHERE name = 'bob'").fetchone()
            if accountID:
                return accountID[0]
            accountID = cursor.execute("INSERT INTO accounts (name) VALUES ('bob') RETURNING id").fetchone()
            assert accountID
            accountID = accountID[0]
    return accountID


@pytest.fixture()
def camilleAccountID(dburl):
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            accountID = cursor.execute("SELECT id from accounts WHERE name = 'camille'").fetchone()
            if accountID:
                return accountID[0]
            accountID = cursor.execute("INSERT INTO accounts (name) VALUES ('camille') RETURNING id").fetchone()
            assert accountID
            accountID = accountID[0]
    return accountID


def _getToken(accountID, dburl):
    with psycopg.connect(dburl) as conn, conn.cursor() as cursor:
        accountToken = cursor.execute("SELECT id FROM tokens WHERE account_id = %s", [accountID]).fetchone()
        assert accountToken
        accountToken = accountToken[0]
        return tokens._generate_jwt_token(accountToken)


@pytest.fixture()
def bobAccountToken(bobAccountID, dburl):
    @functools.cache
    def f():
        return _getToken(bobAccountID, dburl)

    return f


@pytest.fixture()
def camilleAccountToken(camilleAccountID, dburl):
    @functools.cache
    def f():
        return _getToken(camilleAccountID, dburl)

    return f


@pytest.fixture()
def defaultAccountToken(defaultAccountID, dburl):
    @functools.cache
    def f():
        return _getToken(defaultAccountID, dburl)

    return f


def getFirstPictureIds(dburl) -> typing.Tuple[str, str]:
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            p = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures WHERE rank = 1").fetchone()
            assert p is not None
            return (p[0], p[1])


@dataclass
class Picture(object):
    id: str

    def get_derivate_dir(self, datafiles):
        return os.path.join(datafiles, "derivates", self.id[0:2], self.id[2:4], self.id[4:6], self.id[6:8], self.id[9:])

    def get_permanent_file(self, datafiles):
        return os.path.join(datafiles, "permanent", self.id[0:2], self.id[2:4], self.id[4:6], self.id[6:8], f"{self.id[9:]}.jpg")


@dataclass
class Sequence(object):
    id: str
    pictures: typing.List[Picture] = field(default_factory=lambda: [])


def getPictureIds(dburl) -> typing.List[Sequence]:
    with psycopg.connect(dburl) as conn:
        with conn.cursor() as cursor:
            pics = cursor.execute("SELECT seq_id, pic_id FROM sequences_pictures ORDER BY rank").fetchall()
            assert pics is not None

            sequences = []
            for seq_id, pic_id in pics:
                s = next((s for s in sequences if s.id == str(seq_id)), None)
                if s is None:
                    s = Sequence(id=str(seq_id))
                    sequences.append(s)
                s.pictures.append(Picture(id=str(pic_id)))

            return sequences


def mockCreateBlurredHDPictureFactory(datafiles):
    """Mock function for pictures.createBlurredHDPicture"""

    def mockCreateBlurredHDPicture(fs, blurApi, pictureBytes, outputFilename):
        with open(datafiles + "/1_blurred.jpg", "rb") as f:
            fs.writebytes(outputFilename, f.read())
            return Image.open(str(datafiles + "/1_blurred.jpg"))

    return mockCreateBlurredHDPicture


def mockBlurringAPIPost(datafiles, requests_mock):
    with open(datafiles + "/1_blurred.jpg", "rb") as mask:
        requests_mock.post(MOCK_BLUR_API + "/blur/", headers={"Content-Type": "image/jpeg"}, content=mask.read())


def arePicturesSimilar(pic1, pic2, limit=1):
    """Checks if two images have less than limit % of differences"""
    diff = ImageChops.difference(pic1.convert("RGB"), pic2.convert("RGB"))
    stat = ImageStat.Stat(diff)
    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255) * 100
    return diff_ratio <= limit


STAC_VERSION = "1.0.0"


@pytest.fixture
def no_license_app_client(dburl, fsesUrl):
    with (
        create_test_app(
            {
                "TESTING": True,
                "DB_URL": dburl,
                "FS_URL": None,
                "FS_TMP_URL": fsesUrl.tmp,
                "FS_PERMANENT_URL": fsesUrl.permanent,
                "FS_DERIVATES_URL": fsesUrl.derivates,
                "SERVER_NAME": "localhost:5000",
                "PICTURE_PROCESS_DERIVATES_STRATEGY": "ON_DEMAND",
                "SECRET_KEY": "a very secret key",
            }
        ) as app,
        app.test_client() as client,
    ):
        yield client
