def createDB(conn, cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups (
      id integer PRIMARY KEY,
      link text NOT NULL,
      name text NOT NULL,
      cnt_posts integer NOT NULL,
      cnt_likes integer NOT NULL
    );
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id integer PRIMARY KEY,
      link text NOT NULL,
      date date NOT NULL,
      text text NOT NULL,
      cnt_comments integer NOT NULL,
      cnt_media integer NOT NULL,
      cnt_likes integer NOT NULL,
      id_group integer NOT NULL,
      FOREIGN KEY (id_group) REFERENCES groups (id)
    );
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id integer PRIMARY KEY,
      link text NOT NULL,
      name text NOT NULL,
      cnt_comments integer NOT NULL
    );
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS comments (
      id integer PRIMARY KEY,
      date date NOT NULL,
      id_post integer NOT NULL,
      id_user integer NOT NULL,
      text text NOT NULL,
      cnt_media integer NOT NULL,
      FOREIGN KEY (id_post) REFERENCES posts (id),
      FOREIGN KEY (id_user) REFERENCES users (id)
    );
    """)
    conn.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS media (
      id integer PRIMARY KEY,
      id_pc integer NOT NULL,
      pc_type text NOT NULL,
      file_link text NOT NULL,
      file_type text NOT NULL,
      FOREIGN KEY (id_pc) REFERENCES posts (id),
      FOREIGN KEY (id_pc) REFERENCES comments (id)
    );
    """)
    conn.commit()


def insertGroup(conn, cur, id, link, name, cnt_posts, cnt_likes):
    cur.execute("INSERT INTO groups VALUES (?, ?, ?, ?, ?)", (id, link, name, cnt_posts, cnt_likes))
    conn.commit()


def insertPost(conn, cur, id, link, date, text, cnt_comments, cnt_media, cnt_likes, id_group):
    cur.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?,?,?)",
                (id, link, date, text, cnt_comments, cnt_media, cnt_likes, id_group))
    conn.commit()


def insertUser(conn, cur, id, link, name, cnt_comments):
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (id, link, name, cnt_comments))
    conn.commit()


def insertComment(conn, cur, id, date, id_post, id_user, text, cnt_media):
    cur.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?)", (id, date, id_post, id_user, text, cnt_media))
    conn.commit()


def insertMedia(conn, cur, id, id_pc, pc_type, file_link, file_type):
    cur.execute("INSERT INTO media VALUES (?, ?, ?, ?, ?)", (id, id_pc, pc_type, file_link, file_type))
    conn.commit()


def updateGroup(conn, cur, id, likes):
    new_posts = int(cur.execute("SELECT cnt_posts FROM groups WHERE id=?", (id,)).fetchone()[0]) + 1
    new_likes = int(cur.execute("SELECT cnt_likes FROM groups WHERE id=?", (id,)).fetchone()[0]) + likes
    cur.execute("UPDATE groups SET cnt_posts=? WHERE id=?", (new_posts, id))
    cur.execute("UPDATE groups SET cnt_likes=? WHERE id=?", (new_likes, id))
    conn.commit()


def updateUser(conn, cur, id):
    new_comments = cur.execute("SELECT cnt_comments FROM users WHERE id=?", (id,)).fetchone()[0] + 1
    cur.execute("UPDATE users SET cnt_comments=? WHERE id=?", (new_comments, id))
    conn.commit()


def findUserByName(cur, name):
    try:
        id_user = cur.execute("SELECT id FROM users WHERE name=?", (name,)).fetchone()[0]
        return id_user
    except:
        return 0