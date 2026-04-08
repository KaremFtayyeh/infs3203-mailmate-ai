from db import init_db, save_reply, get_all_replies


def test_init_db():
    init_db()
    assert True


def test_save_reply():
    init_db()
    save_reply("Test email", "formal", "short", "Test reply")
    rows = get_all_replies()
    assert len(rows) >= 1


def test_saved_reply_has_tone():
    init_db()
    save_reply("Email 1", "friendly", "medium", "Reply 1")
    rows = get_all_replies()
    assert rows[0]["tone"] is not None


def test_saved_reply_has_length():
    init_db()
    save_reply("Email 2", "formal", "detailed", "Reply 2")
    rows = get_all_replies()
    assert rows[0]["reply_length"] is not None