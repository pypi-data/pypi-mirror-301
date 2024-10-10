from enum import Enum
import logging
import psycopg.rows
from pydantic import BaseModel, ConfigDict, computed_field, Field, field_serializer
from geovisio.utils.extent import TemporalExtent
from uuid import UUID
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from geovisio.utils import db, sequences
from geovisio import errors
from geovisio.utils.link import make_link, Link
import psycopg
from psycopg.types.json import Jsonb
from psycopg.sql import SQL
from psycopg.rows import class_row, dict_row
from flask import current_app
from flask_babel import gettext as _
from geopic_tag_reader import sequence as geopic_sequence, reader


class AggregatedStatus(BaseModel):
    """Aggregated status"""

    prepared: int
    """Number of pictures successfully processed"""
    preparing: Optional[int]
    """Number of pictures being processed"""
    broken: Optional[int]
    """Number of pictures that failed to be processed. It is likely a server problem."""
    rejected: Optional[int] = None
    """Number of pictures that were rejected by the server. It is likely a client problem."""
    not_processed: Optional[int]
    """Number of pictures that have not been processed yet"""

    model_config = ConfigDict(use_attribute_docstrings=True)


class AssociatedCollection(BaseModel):
    """Collection associated to an UploadSet"""

    id: UUID
    nb_items: int
    extent: Optional[TemporalExtent] = None
    title: Optional[str] = None
    items_status: Optional[AggregatedStatus] = None
    status: Optional[str] = Field(exclude=True, default=None)

    @computed_field
    @property
    def links(self) -> List[Link]:
        return [
            make_link(rel="self", route="stac_collections.getCollection", collectionId=self.id),
        ]

    @computed_field
    @property
    def ready(self) -> Optional[bool]:
        if self.items_status is None:
            return None
        return self.items_status.not_processed == 0 and self.status == "ready"


class UploadSet(BaseModel):
    """The UploadSet represent a group of files sent in one upload. Those files will be distributed among one or more collections."""

    id: UUID
    created_at: datetime
    completed: bool
    dispatched: bool
    account_id: UUID
    title: str
    estimated_nb_files: Optional[int] = None
    sort_method: geopic_sequence.SortMethod
    split_distance: int
    split_time: timedelta
    duplicate_distance: float
    duplicate_rotation: int
    metadata: Optional[Dict[str, Any]]
    user_agent: Optional[str] = Field(exclude=True)
    associated_collections: List[AssociatedCollection] = []
    nb_items: int = 0
    items_status: Optional[AggregatedStatus] = None

    @computed_field
    @property
    def links(self) -> List[Link]:
        return [
            make_link(rel="self", route="upload_set.getUploadSet", upload_set_id=self.id),
        ]

    @computed_field
    @property
    def ready(self) -> bool:
        return self.dispatched and all(c.ready for c in self.associated_collections)

    model_config = ConfigDict(use_enum_values=True, ser_json_timedelta="float", use_attribute_docstrings=True)


class UploadSets(BaseModel):
    upload_sets: List[UploadSet]


class FileType(Enum):
    """Type of uploadedfile"""

    picture = "picture"
    # Note: for the moment we only support pictures, but later we might accept more kind of files (like gpx traces, video, ...)


class FileRejectionStatusSeverity(Enum):
    error = "error"
    warning = "warning"
    info = "info"


class FileRejectionStatus(Enum):
    capture_duplicate = "capture_duplicate"
    """capture duplicate means there was another picture too near (in space and time)"""
    file_duplicate = "file_duplicate"
    """File duplicate means the same file was already uploaded"""
    invalid_file = "invalid_file"
    """invalid_file means the file is not a valid jpeg"""
    invalid_metadata = "invalid_metadata"
    """invalid_metadata means the file has invalid metadata"""
    other_error = "other_error"
    """other_error means there was an error that is not related to the picture itself"""


class UploadSetFile(BaseModel):
    """File uploaded in an UploadSet"""

    picture_id: Optional[UUID] = None
    file_name: str
    content_md5: Optional[UUID] = None
    inserted_at: datetime
    upload_set_id: UUID = Field(..., exclude=True)
    rejection_status: Optional[FileRejectionStatus] = Field(None, exclude=True)
    rejection_message: Optional[str] = Field(None, exclude=True)
    file_type: Optional[FileType] = None
    size: Optional[int] = None

    @computed_field
    @property
    def links(self) -> List[Link]:
        return [
            make_link(rel="parent", route="upload_set.getUploadSet", upload_set_id=self.upload_set_id),
        ]

    @computed_field
    @property
    def rejected(self) -> Optional[Dict[str, Any]]:
        if self.rejection_status is None:
            return None
        msg = None
        severity = FileRejectionStatusSeverity.error
        if self.rejection_message is None:
            if self.rejection_status == FileRejectionStatus.capture_duplicate.value:
                msg = _("The picture is too similar to another one (nearby and taken almost at the same time)")
                severity = FileRejectionStatusSeverity.info
            if self.rejection_status == FileRejectionStatus.invalid_file.value:
                msg = _("The sent file is not a valid JPEG")
                severity = FileRejectionStatusSeverity.error
            if self.rejection_status == FileRejectionStatus.invalid_metadata.value:
                msg = _("The picture has invalid EXIF or XMP metadata, making it impossible to use")
                severity = FileRejectionStatusSeverity.error
            if self.rejection_status == FileRejectionStatus.other_error.value:
                msg = _("Something went very wrong, but not due to the picture itself")
                severity = FileRejectionStatusSeverity.error
        else:
            msg = self.rejection_message
        return {
            "reason": self.rejection_status,
            "severity": severity,
            "message": msg,
        }

    @field_serializer("content_md5")
    def serialize_md5(self, md5: UUID, _info):
        return md5.hex

    model_config = ConfigDict(use_enum_values=True, use_attribute_docstrings=True)


class UploadSetFiles(BaseModel):
    """List of files uploaded in an UploadSet"""

    files: List[UploadSetFile]
    upload_set_id: UUID = Field(..., exclude=True)

    @computed_field
    @property
    def links(self) -> List[Link]:
        return [
            make_link(rel="self", route="upload_set.getUploadSet", upload_set_id=self.upload_set_id),
        ]


def get_simple_upload_set(id: UUID) -> Optional[UploadSet]:
    """Get the DB representation of an UploadSet, without associated collections and statuses"""
    u = db.fetchone(
        current_app,
        SQL("SELECT * FROM upload_sets WHERE id = %(id)s AND not deleted"),
        {"id": id},
        row_factory=class_row(UploadSet),
    )

    return u


def get_upload_set(id: UUID) -> Optional[UploadSet]:
    """Get the UploadSet corresponding to the ID"""
    db_upload_set = db.fetchone(
        current_app,
        SQL(
            """WITH picture_last_job AS (
    SELECT p.id as picture_id,
        -- Note: to know if a picture is beeing processed, check the latest job_history entry for this picture
        -- If there is no finished_at, the picture is still beeing processed
        (MAX(ARRAY [started_at, finished_at])) AS last_job,
        p.preparing_status,
        p.status,
        p.upload_set_id
    FROM pictures p
        LEFT JOIN job_history ON p.id = job_history.picture_id
    WHERE p.upload_set_id = %(id)s
    GROUP BY p.id
),
picture_statuses AS (
    SELECT 
        *,
        (last_job[1] IS NOT NULL AND last_job[2] IS NULL) AS is_job_running
        FROM picture_last_job psj
),
associated_collections AS (
    SELECT 
        ps.upload_set_id,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'broken') AS nb_broken,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'prepared') AS nb_prepared,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'not-processed') AS nb_not_processed,
        COUNT(ps.picture_id) FILTER (WHERE ps.is_job_running AND ps.status != 'waiting-for-delete') AS nb_preparing,
        s.id as collection_id,
        s.nb_pictures AS nb_items,
        s.min_picture_ts AS mints,
        s.max_picture_ts AS maxts,
        s.metadata->>'title' AS title,
        s.status AS status
    FROM picture_statuses ps
        JOIN sequences_pictures sp ON sp.pic_id = ps.picture_id
        JOIN sequences s ON s.id = sp.seq_id
    WHERE ps.upload_set_id = %(id)s AND s.status != 'deleted'
    GROUP BY ps.upload_set_id,
        s.id
),
upload_set_statuses AS (
    SELECT ps.upload_set_id,
        COUNT(ps.picture_id) AS nb_items,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'broken') AS nb_broken,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'prepared') AS nb_prepared,
        COUNT(ps.picture_id) FILTER (WHERE ps.preparing_status = 'not-processed') AS nb_not_processed,
        COUNT(ps.picture_id) FILTER (WHERE ps.is_job_running) AS nb_preparing
    FROM picture_statuses ps
    GROUP BY ps.upload_set_id
)
SELECT u.*,
    COALESCE(us.nb_items, 0) AS nb_items,
    json_build_object(
        'broken', COALESCE(us.nb_broken, 0),
        'prepared', COALESCE(us.nb_prepared, 0),
        'not_processed', COALESCE(us.nb_not_processed, 0),
        'preparing', COALESCE(us.nb_preparing, 0),
        'rejected', (
            SELECT count(*) FROM files 
            WHERE upload_set_id = %(id)s AND rejection_status IS NOT NULL
        )
    ) AS items_status,
    COALESCE(
        (
            SELECT json_agg(
                    json_build_object(
                        'id',
                        ac.collection_id,
                        'title',
                        ac.title,
                        'nb_items',
                        ac.nb_items,
                        'status',
                        ac.status,
                        'extent',
                        json_build_object(
                            'temporal',
                            json_build_object(
                                'interval',
                                json_build_array(
                                    json_build_array(ac.mints, ac.maxts)
                                )
                            )
                        ),
                        'items_status',
                        json_build_object(
                            'broken', ac.nb_broken,
                            'prepared', ac.nb_prepared,
                            'not_processed', ac.nb_not_processed,
                            'preparing', ac.nb_preparing
                        )
                    )
                )
            FROM associated_collections ac
        ),
        '[]'::json
    ) AS associated_collections
FROM upload_sets u
LEFT JOIN upload_set_statuses us on us.upload_set_id = u.id
WHERE u.id = %(id)s AND not deleted"""
        ),
        {"id": id},
        row_factory=class_row(UploadSet),
    )

    return db_upload_set


FIELD_TO_SQL_FILTER = {
    "completed": "completed",
    "dispatched": "dispatched",
}


def _parse_filter(filter: Optional[str]) -> SQL:
    """
    Parse a filter string and return a SQL expression

    >>> _parse_filter('')
    SQL('TRUE')
    >>> _parse_filter(None)
    SQL('TRUE')
    >>> _parse_filter('completed = TRUE')
    SQL('(completed = True)')
    >>> _parse_filter('completed = TRUE AND dispatched = FALSE')
    SQL('((completed = True) AND (dispatched = False))')
    """
    if not filter:
        return SQL("TRUE")
    from pygeofilter.backends.sql import to_sql_where
    from pygeofilter.parsers.cql2_text import parse as cql_parser

    try:
        filterAst = cql_parser(filter)
        f = to_sql_where(filterAst, FIELD_TO_SQL_FILTER).replace('"', "")  # type: ignore
        return SQL(f)  # type: ignore
    except Exception:
        logging.error(f"Unsupported filter parameter: {filter}")
        raise errors.InvalidAPIUsage(_("Unsupported filter parameter"), status_code=400)


def list_upload_sets(account_id: UUID, limit: int = 100, filter: Optional[str] = None) -> UploadSets:
    filter_sql = _parse_filter(filter)
    l = db.fetchall(
        current_app,
        SQL(
            """SELECT 
            u.*,
            COALESCE(
                (
                    SELECT 
                        json_agg(json_build_object(
                            'id', ac.collection_id,
                            'nb_items', ac.nb_items
                        ))
                    FROM (
                        SELECT 
                            sp.seq_id as collection_id,
                            count(sp.pic_id) AS nb_items
                        FROM pictures p 
                        JOIN sequences_pictures sp ON sp.pic_id = p.id
                        WHERE p.upload_set_id = u.id
                        GROUP BY sp.seq_id
                    ) ac
                ),
                '[]'::json
            ) AS associated_collections,
            (
                SELECT count(*) AS nb
                FROM pictures p 
                WHERE p.upload_set_id = u.id
            ) AS nb_items
        FROM upload_sets u
        WHERE account_id = %(account_id)s AND not deleted AND {filter}
        ORDER BY created_at ASC
        LIMIT %(limit)s
        """
        ).format(filter=filter_sql),
        {"account_id": account_id, "limit": limit},
        row_factory=class_row(UploadSet),
    )

    return UploadSets(upload_sets=l)


def ask_for_dispatch(upload_set_id: UUID):
    """Add a dispatch task to the job queue for the upload set. If there is already a task, postpone it."""
    with db.conn(current_app) as conn:
        conn.execute(
            """INSERT INTO 
            job_queue(sequence_id, task)
            VALUES (%(upload_set_id)s, 'dispatch')
            ON CONFLICT (upload_set_id) DO UPDATE SET ts = CURRENT_TIMESTAMP""",
            {"upload_set_id": upload_set_id},
        )


def dispatch(upload_set_id: UUID):
    """Finalize an upload set.

    For the moment we only create a collection around all the items of the upload set, but later we'll split the items into several collections

    Note: even if all pictures are not prepared, it's not a problem as we only need the pictures metadata for distributing them in collections
    """

    db_upload_set = get_simple_upload_set(upload_set_id)
    if not db_upload_set:
        raise Exception(f"Upload set {upload_set_id} not found")

    with db.conn(current_app) as conn:
        with conn.transaction(), conn.cursor(row_factory=dict_row) as cursor:

            # get all the pictures of the upload set
            db_pics = cursor.execute(
                SQL(
                    """SELECT 
    p.id,
    p.ts,
    ST_X(p.geom) as lon,
    ST_Y(p.geom) as lat,
    p.heading as heading,
    p.metadata->>'originalFileName' as file_name,
    p.metadata,
    s.id as sequence_id
FROM pictures p
LEFT JOIN sequences_pictures sp ON sp.pic_id = p.id
LEFT JOIN sequences s ON s.id = sp.seq_id
WHERE p.upload_set_id = %(upload_set_id)s"""
                ),
                {"upload_set_id": upload_set_id},
            ).fetchall()

            pics_by_filename = {p["file_name"]: p for p in db_pics}
            pics = [
                geopic_sequence.Picture(
                    p["file_name"],
                    reader.GeoPicTags(
                        lon=p["lon"],
                        lat=p["lat"],
                        ts=p["ts"],
                        type=p["metadata"]["type"],
                        heading=p["heading"],
                        make=p["metadata"]["make"],
                        model=p["metadata"]["model"],
                        focal_length=p["metadata"]["focal_length"],
                        crop=p["metadata"]["crop"],
                        exif={},
                    ),
                )
                for p in db_pics
            ]

            report = geopic_sequence.dispatch_pictures(
                pics,
                mergeParams=geopic_sequence.MergeParams(
                    maxDistance=db_upload_set.duplicate_distance, maxRotationAngle=db_upload_set.duplicate_rotation
                ),
                sortMethod=db_upload_set.sort_method,
                splitParams=geopic_sequence.SplitParams(maxDistance=db_upload_set.split_distance, maxTime=db_upload_set.split_time.seconds),
            )
            reused_sequence = set()

            pics_to_delete = [pics_by_filename[p.filename]["id"] for p in report.duplicate_pictures or []]
            if pics_to_delete:
                logging.debug(f"For uploadset '{upload_set_id}', nb duplicate pictures {len(pics_to_delete)}")
                logging.debug(
                    f"For uploadset '{upload_set_id}', duplicate pictures {[p.filename for p in report.duplicate_pictures or []]}"
                )

                cursor.execute(SQL("CREATE TEMPORARY TABLE tmp_duplicates(picture_id UUID) ON COMMIT DROP"))
                with cursor.copy("COPY tmp_duplicates(picture_id) FROM stdin;") as copy:
                    for p in pics_to_delete:
                        copy.write_row((p,))

                cursor.execute(
                    SQL(
                        "UPDATE files SET rejection_status = 'capture_duplicate' WHERE picture_id IN (select picture_id from tmp_duplicates)"
                    )
                )
                cursor.execute(
                    SQL(
                        """INSERT INTO job_queue (picture_id, task)
SELECT picture_id, 'delete'
FROM tmp_duplicates
ON CONFLICT(picture_id) DO UPDATE SET task = 'delete'"""
                    )
                )

                # ask for deletion of the pictures

            for s in report.sequences:
                existing_sequence = next(
                    (seq for p in s.pictures if (seq := pics_by_filename[p.filename]["sequence_id"]) not in reused_sequence),
                    None,
                )
                # if some of the pictures were already in a sequence, we should not create a new one
                if existing_sequence:
                    logging.info(
                        f"For uploadset '{upload_set_id}', sequence {existing_sequence} already contains pictures, we will not create a new one"
                    )
                    # we should wipe the sequences_pictures though
                    seq_id = existing_sequence
                    cursor.execute(
                        SQL("DELETE FROM sequences_pictures WHERE seq_id = %(seq_id)s"),
                        {"seq_id": seq_id},
                    )
                    reused_sequence.add(seq_id)
                else:
                    seq_id = cursor.execute(
                        SQL(
                            """INSERT INTO sequences(account_id, metadata, user_agent)
VALUES (%(account_id)s, %(metadata)s, %(user_agent)s)
RETURNING id"""
                        ),
                        {
                            "account_id": db_upload_set.account_id,
                            "metadata": Jsonb({"title": db_upload_set.title}),
                            "user_agent": db_upload_set.user_agent,
                        },
                    ).fetchone()
                    seq_id = seq_id["id"]

                with cursor.copy("COPY sequences_pictures(seq_id, pic_id, rank) FROM stdin;") as copy:
                    for i, p in enumerate(s.pictures, 1):
                        copy.write_row(
                            (seq_id, pics_by_filename[p.filename]["id"], i),
                        )

                sequences.add_finalization_job(cursor=cursor, seqId=seq_id)

            for s in report.sequences_splits or []:
                logging.debug(f"For uploadset '{upload_set_id}', split = {s.prevPic.filename} -> {s.nextPic.filename} : {s.reason}")
            conn.execute(SQL("UPDATE upload_sets SET dispatched = true WHERE id = %(upload_set_id)s"), {"upload_set_id": db_upload_set.id})


def insertFileInDatabase(
    *,
    cursor: psycopg.Cursor[psycopg.rows.DictRow],
    upload_set_id: UUID,
    file_name: str,
    content_md5: Optional[str] = None,
    size: Optional[int] = None,
    file_type: Optional[FileType] = None,
    picture_id: Optional[UUID] = None,
    rejection_status: Optional[FileRejectionStatus] = None,
    rejection_message: Optional[str] = None,
) -> UploadSetFile:
    """Insert a file linked to an UploadSet into the database"""

    f = cursor.execute(
        SQL(
            """
    INSERT INTO files(
        upload_set_id, picture_id, file_type, file_name,
        size, content_md5, rejection_status, rejection_message)
    VALUES (
        %(upload_set_id)s, %(picture_id)s, %(type)s, %(file_name)s,
        %(size)s, %(content_md5)s, %(rejection_status)s, %(rejection_message)s)
    ON CONFLICT (upload_set_id, file_name)
    DO UPDATE SET picture_id = %(picture_id)s, size = %(size)s, content_md5 = %(content_md5)s,
        rejection_status = %(rejection_status)s, rejection_message = %(rejection_message)s
    RETURNING *
    """
        ),
        params={
            "upload_set_id": upload_set_id,
            "type": file_type,
            "picture_id": picture_id,
            "file_name": file_name,
            "size": size,
            "content_md5": content_md5,
            "rejection_status": rejection_status,
            "rejection_message": rejection_message,
        },
    )
    return UploadSetFile(**f.fetchone())


def get_upload_set_files(upload_set_id: UUID) -> UploadSetFiles:
    """Get the files of an UploadSet"""
    files = db.fetchall(
        current_app,
        SQL(
            """SELECT
    upload_set_id, 
    file_type, 
    file_name, 
    size, 
    content_md5, 
    rejection_status,
    rejection_message,
    picture_id, 
    inserted_at
FROM files
WHERE upload_set_id = %(upload_set_id)s
ORDER BY inserted_at"""
        ),
        {"upload_set_id": upload_set_id},
        row_factory=dict_row,
    )
    return UploadSetFiles(files=files, upload_set_id=upload_set_id)


def delete(upload_set: UploadSet):
    """Delete an UploadSet"""
    logging.info(f"Asking for deletion of uploadset {upload_set.id}")
    with db.conn(current_app) as conn:
        with conn.transaction(), conn.cursor() as cursor:
            for c in upload_set.associated_collections:
                # Mark all collections as deleted, but do not delete them
                # Note: we do not use utils.sequences.delete_collection here, since we also want to remove the pictures not associated to any collection
                cursor.execute(SQL("DELETE FROM job_queue WHERE sequence_id = %s"), [c.id])
                cursor.execute(SQL("UPDATE sequences SET status = 'deleted' WHERE id = %s"), [c.id])

            # check utils.sequences.delete_collection to see why picture removal is done in 2 steps
            cursor.execute(
                """
INSERT INTO job_queue(picture_id, task)
    SELECT id, 'delete'
    FROM pictures
    WHERE upload_set_id = %(upload_set_id)s
ON CONFLICT (picture_id) DO UPDATE SET task = 'delete'""",
                {"upload_set_id": upload_set.id},
            )

            # after the task have been added to the queue, we mark all picture for deletion
            cursor.execute(
                SQL(
                    "UPDATE pictures SET status = 'waiting-for-delete' WHERE id IN (SELECT id FROM pictures WHERE upload_set_id = %(upload_set_id)s)"
                ),
                {"upload_set_id": upload_set.id},
            )
            # we insert the upload set deletion task in the queue after the rest, it will be done once all pictures are deleted
            cursor.execute(
                """INSERT INTO job_queue(upload_set_id, task) VALUES (%(upload_set_id)s, 'delete') 
ON CONFLICT (upload_set_id) DO UPDATE SET task = 'delete'""",
                {"upload_set_id": upload_set.id},
            )

            # and we mark it as deleted so it will disapear from the responses even if all the pictures are not yet deleted
            cursor.execute("UPDATE upload_sets SET deleted = true WHERE id = %(upload_set_id)s", {"upload_set_id": upload_set.id})
