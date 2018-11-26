# ===============================================================================
# Copyright 2018 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
from traits.api import HasTraits, Str, Password, Instance

import pymssql


class MockConnection:
    def cursor(self):
        return MockCursor()

    def close(self):
        pass

    def commit(self):
        pass


class MockCursor:
    def execute(self, *args, **kw):
        pass

    def fetchall(self):
        return []

    def fetchone(self):
        pass


def get_connection(h, u, p, n, *args, **kw):
    try:
        conn = pymssql.connect(h, u, p, n, timeout=15, login_timeout=5, *args, **kw)
    except (pymssql.InterfaceError, pymssql.OperationalError):
        conn = MockConnection()

    return conn


class SessionCTX:
    def __init__(self, h, u, p, n, *args, **kw):
        conn = get_connection(h, u, p, n, *args, **kw)
        self._conn = conn

    def __enter__(self):
        return self._conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._conn.close()


class Credentials(HasTraits):
    username = Str
    password = Password
    host = Str
    database_name = Str


class DatabaseConnector(HasTraits):
    credentials = Instance(Credentials)

    def get_site(self, site_id):
        with self._get_session() as cursor:
            cmd = 'select * from dbo.Location where SiteID=%s'
            cursor.execute(cmd, site_id)
            return cursor.fetchone()

    def _credentials_default(self):
        cred = Credentials()
        return cred

    def _get_session(self):
        cred = self.credentials
        return SessionCTX(cred.host, cred.user, cred.password, cred.database_name)

# ============= EOF =============================================
