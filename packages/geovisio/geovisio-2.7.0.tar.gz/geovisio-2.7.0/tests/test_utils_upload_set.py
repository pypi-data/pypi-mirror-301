from datetime import datetime, timezone
from flask import current_app
from geovisio.utils import db, sequences
from geovisio.utils import upload_set
from geovisio.utils.extent import TemporalExtent, Temporal


def test_get_upload_set(client, defaultAccountID):
    with db.cursor(current_app) as cur:
        upload_id = cur.execute(
            "INSERT INTO upload_sets (title, account_id) VALUES (%s, %s) RETURNING id", ["some title", defaultAccountID]
        ).fetchone()[0]
        pic_id = cur.execute(
            """INSERT INTO pictures (ts, geom, account_id, upload_set_id)
VALUES (%s, ST_SetSRID(ST_MakePoint(0, 0), 4326), %s, %s)
RETURNING id""",
            [datetime(year=2024, month=7, day=21, hour=10).isoformat(), defaultAccountID, upload_id],
        ).fetchone()[0]

        u = upload_set.get_upload_set(upload_id)
        assert u

        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 1
        assert u.associated_collections == []
        assert u.items_status == upload_set.AggregatedStatus(prepared=0, preparing=0, broken=0, not_processed=1, rejected=0)

        # we add the picture in a collection
        seq_id = sequences.createSequence({"title": "plop"}, defaultAccountID)
        cur.execute("INSERT INTO sequences_pictures (seq_id, pic_id, rank) VALUES (%s, %s, 1)", [seq_id, pic_id])

        u = upload_set.get_upload_set(upload_id)
        assert u
        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 1
        assert u.associated_collections == [
            upload_set.AssociatedCollection(
                id=seq_id,
                nb_items=1,
                status="waiting-for-process",
                extent=TemporalExtent(
                    temporal=Temporal(
                        interval=[
                            [
                                datetime(2024, 7, 21, 10, 0, tzinfo=timezone.utc),
                                datetime(2024, 7, 21, 10, 0, tzinfo=timezone.utc),
                            ]
                        ]
                    ),
                ),
                title="plop",
                items_status=upload_set.AggregatedStatus(prepared=0, preparing=0, broken=0, not_processed=1),
            )
        ]
        assert u.items_status == upload_set.AggregatedStatus(prepared=0, preparing=0, broken=0, not_processed=1, rejected=0)


def test_get_upload_set_status(client, defaultAccountID):
    """Add 5 pictures to an upload set, and check that the status is correct during different stages of the upload"""
    with db.cursor(current_app) as cur:
        upload_id = cur.execute(
            "INSERT INTO upload_sets (title, account_id) VALUES (%s, %s) RETURNING id", ["some title", defaultAccountID]
        ).fetchone()[0]

        # at first, empty upload set
        u = upload_set.get_upload_set(upload_id)
        assert u
        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 0
        assert u.associated_collections == []
        assert u.items_status == upload_set.AggregatedStatus(prepared=0, preparing=0, broken=0, not_processed=0, rejected=0)

        pics_id = []
        for i in range(5):
            pic_id = cur.execute(
                """INSERT INTO pictures (ts, geom, account_id, upload_set_id)
    VALUES (%(ts)s, ST_SetSRID(ST_MakePoint(0, %(lon)s), 4326), %(account_id)s, %(upload_set_id)s)
    RETURNING id""",
                {
                    "ts": datetime(year=2024, month=7, day=21, hour=10 + i).isoformat(),
                    "account_id": defaultAccountID,
                    "upload_set_id": upload_id,
                    "lon": i,
                },
            ).fetchone()[0]
            pics_id.append(pic_id)

        u = upload_set.get_upload_set(upload_id)
        assert u

        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 5
        assert u.associated_collections == []
        assert u.items_status == upload_set.AggregatedStatus(prepared=0, preparing=0, broken=0, not_processed=5, rejected=0)

        # We mark 1 picture as broken, 2 as processed, and we add one non terminated job in job_history (and one pic is not processed)
        cur.execute("UPDATE pictures SET preparing_status = 'broken' WHERE id = %s", [pics_id[0]])
        cur.execute("UPDATE pictures SET preparing_status = 'prepared' WHERE id in (%s, %s)", [pics_id[1], pics_id[2]])
        history = [
            {
                "pic_id": pics_id[0],
                "started_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "finished_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "error": "ho no something went wrong",
            },
            {
                "pic_id": pics_id[1],
                "started_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "finished_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "error": None,
            },
            {
                "pic_id": pics_id[2],
                "started_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "finished_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "error": None,
            },
            {
                "pic_id": pics_id[3],
                "started_at": datetime(year=2024, month=7, day=21, hour=10).isoformat(),
                "finished_at": None,
                "error": None,
            },
        ]
        for h in history:
            cur.execute(
                "INSERT INTO job_history (job_task, picture_id, started_at, finished_at, error) VALUES ('prepare', %(pic_id)s, %(started_at)s, %(finished_at)s, %(error)s)",
                h,
            )

        u = upload_set.get_upload_set(upload_id)
        assert u

        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 5
        assert u.associated_collections == []
        # Note: the picture being processed is counted in the 'preparing' and in the 'not-processed'
        assert u.items_status == upload_set.AggregatedStatus(prepared=2, preparing=1, broken=1, not_processed=2, rejected=0)

        # we add the pictures in 2 different collections,
        seq1_id = sequences.createSequence({"title": "plop"}, defaultAccountID)
        seq2_id = sequences.createSequence({"title": "plop2"}, defaultAccountID)
        for i, p in enumerate(pics_id):
            col = seq1_id if i < 3 else seq2_id
            cur.execute("INSERT INTO sequences_pictures (seq_id, pic_id, rank) VALUES (%s, %s, %s)", [col, p, i])

        u = upload_set.get_upload_set(upload_id)
        assert u
        assert u.id == upload_id
        assert u.title == "some title"
        assert u.account_id == defaultAccountID
        assert u.estimated_nb_files is None
        assert u.nb_items == 5

        assert len(u.associated_collections) == 2
        assert sorted(u.associated_collections, key=lambda x: x.id) == sorted(
            [
                upload_set.AssociatedCollection(
                    id=seq1_id,
                    nb_items=3,
                    status="waiting-for-process",
                    extent=TemporalExtent(
                        temporal=Temporal(
                            interval=[
                                [
                                    datetime(2024, 7, 21, 10, 0, tzinfo=timezone.utc),
                                    datetime(2024, 7, 21, 12, 0, tzinfo=timezone.utc),
                                ]
                            ]
                        ),
                    ),
                    title="plop",
                    items_status=upload_set.AggregatedStatus(prepared=2, preparing=0, broken=1, not_processed=0),
                ),
                upload_set.AssociatedCollection(
                    id=seq2_id,
                    nb_items=2,
                    status="waiting-for-process",
                    extent=TemporalExtent(
                        temporal=Temporal(
                            interval=[
                                [
                                    datetime(2024, 7, 21, 13, 0, tzinfo=timezone.utc),
                                    datetime(2024, 7, 21, 14, 0, tzinfo=timezone.utc),
                                ]
                            ]
                        ),
                    ),
                    title="plop2",
                    items_status=upload_set.AggregatedStatus(prepared=0, preparing=1, broken=0, not_processed=2),
                ),
            ],
            key=lambda x: x.id,
        )
        assert u.items_status == upload_set.AggregatedStatus(prepared=2, preparing=1, broken=1, not_processed=2, rejected=0)
