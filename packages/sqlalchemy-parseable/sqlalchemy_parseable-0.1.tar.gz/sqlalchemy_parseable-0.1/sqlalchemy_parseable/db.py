from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from pyarrow import flight

from sqlalchemy_parseable.exceptions import Error, NotSupportedError
from sqlalchemy_parseable.flight_middleware import CookieMiddlewareFactory
from sqlalchemy_parseable.query import execute

logger = logging.getLogger(__name__)

paramstyle = 'qmark'

def connect(c):
    return Connection(c)

def check_closed(f):
    """Decorator that checks if connection/cursor is closed."""

    def g(self, *args, **kwargs):
        if self.closed:
            raise Error(
                "{Class} already closed".format(Class=self.__class__.__name__)
            )
        return f(self,*args, **kwargs)
    
    return g

def check_result(f):
    """Decorator that checks if the cursor has results from `execute`."""

    def d(self, *args, **kwargs):
        if self._results is None:
            raise Error('Called before `execute`')
        return f(self, *args, **kwargs)

    return d

class Connection(object):

    def __init__(self, connection_string: str):
        # Build a map from the connection string supplied using the SQLAlchemy URI
        # and supplied properties. The format is generated from DremioDialect_flight.create_connect_args()
        # and is a semi-colon delimited string of key=value pairs. Note that the value itself can
        # contain equal signs.
        # parseable+flight://username:password@host:port
        properties = {}
        splits = connection_string.split("@")

        for i,value in enumerate(splits[0].split(":")):
            if i==0:
                # dialect+driver
                pass
            if i==1:
                # username, remove //
                value = value.replace("//","")
                properties["USERNAME"] = value
            if i==2:
                # password
                properties["PASSWORD"] = value

        for i,value in enumerate(splits[1].split(":")):
            if i==0:
                # host
                properties["HOST"] = value
            if i==1:
                # port
                properties["PORT"] = value

        connection_args = {}

        # # Connect to the server endpoint with an encrypted TLS connection by default.
        # protocol = 'tls'
        # if 'UseEncryption' in properties and properties['UseEncryption'].lower() == 'false':
        #     protocol = 'tcp'
        # else:
        #     # Specify the trusted certificates
        #     connection_args['disable_server_verification'] = False
        #     if 'TrustedCerts' in properties:
        #         with open(properties['TrustedCerts'] , "rb") as root_certs:
        #             connection_args["tls_root_certs"] = root_certs.read()
        #     # Or disable server verification entirely
        #     elif 'DisableCertificateVerification' in properties and properties['DisableCertificateVerification'].lower() == 'true':
        #         connection_args['disable_server_verification'] = True

        protocol = "tcp"

        # Enabling cookie middleware for stateful connectivity.
        client_cookie_middleware = CookieMiddlewareFactory()

        client = flight.FlightClient('grpc+{0}://{1}:{2}'.format(protocol, properties['HOST'], properties['PORT']),
            middleware=[client_cookie_middleware], **connection_args)
        
        
        # Authenticate using basic username/password
        headers = []
        bearer_token = client.authenticate_basic_token(properties['USERNAME'], properties['PASSWORD'])
        headers.append(bearer_token)

        self.flightclient = client
        self.options = flight.FlightCallOptions(headers=headers)

        self.closed = False
        self.cursors = []

    @check_closed
    def close(self):
        """Close the connection now."""
        self.closed = True
        for cursor in self.cursors:
            try:
                cursor.close()
            except Error:
                pass  # already closed

    @check_closed
    def cursor(self):
        """Return a new Cursor Object using the connection."""
        cursor = Cursor(self.flightclient, self.options)
        self.cursors.append(cursor)

        return cursor
    
    @check_closed
    def execute(self, query):
        cursor = self.cursor()
        return cursor.execute(query)
    
class Cursor(object):
    """Connection cursor."""

    def __init__(self, flightclient=None, options=None):
        self.flightclient = flightclient
        self.options = options

        # This read/write attribute specifies the number of rows to fetch at a
        # time with .fetchmany(). It defaults to 1 meaning to fetch a single
        # row at a time.
        self.arraysize = 1

        self.closed = False

        # this is updated only after a query
        self.description = None

        # this is set to a list of rows after a successful query
        self._results = None

    @property
    @check_result
    @check_closed
    def rowcount(self):
        return len(self._results)

    @check_closed
    def close(self):
        """Close the cursor."""
        self.closed = True

    @check_closed
    def execute(self, query, params=None):
        self.description = None
        self._results, self.description = execute(
            query, self.flightclient, self.options)
        return self

    @check_closed
    def executemany(self, query):
        raise NotSupportedError(
            '`executemany` is not supported, use `execute` instead')
    

    @check_result
    @check_closed
    def fetchone(self):
        """
        Fetch the next row of a query result set, returning a single sequence,
        or `None` when no more data is available.
        """
        try:
            return self._results.pop(0)
        except IndexError:
            return None

    @check_result
    @check_closed
    def fetchmany(self, size=None):
        """
        Fetch the next set of rows of a query result, returning a sequence of
        sequences (e.g. a list of tuples). An empty sequence is returned when
        no more rows are available.
        """
        size = size or self.arraysize
        out = self._results[:size]
        self._results = self._results[size:]
        return out

    @check_result
    @check_closed
    def fetchall(self):
        """
        Fetch all (remaining) rows of a query result, returning them as a
        sequence of sequences (e.g. a list of tuples). Note that the cursor's
        arraysize attribute can affect the performance of this operation.
        """
        out = self._results[:]
        self._results = []
        return out

    @check_closed
    def setinputsizes(self, sizes):
        # not supported
        pass

    @check_closed
    def setoutputsizes(self, sizes):
        # not supported
        pass

    @check_closed
    def __iter__(self):
        return iter(self._results)
