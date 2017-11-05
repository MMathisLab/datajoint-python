"""
a schema for testing external attributes
"""

import datajoint as dj

from . import PREFIX, CONN_INFO
import numpy as np

schema = dj.schema(PREFIX + '_extern', locals(), connection=dj.conn(**CONN_INFO))


dj.config['external'] = {
    'protocol': 'file',
    'location': 'dj-store/external'}

dj.config['external-raw'] = {
    'protocol': 'file',
    'location': 'dj-store/raw'}

dj.config['external-compute'] = {
    'protocol': 's3',
    'location': '/datajoint-projects/test',
    'user': 'djtest',
    'token': '2e05709792545ce'}

dj.config['cache'] = {
    'protocol': 'file',
    'location': '/media/dimitri/ExtraDrive1/dj-store/cache'}



@schema
class Seed(dj.Lookup):
    definition = """
    seed :  int 
    """
    contents = zip(range(4))


@schema
class Dimension(dj.Lookup):
    definition = """
    dim  : int
    ---
    dimensions  : blob  
    """
    contents = (
        [0, [100, 50]],
        [1, [3, 4, 8, 6]])


@schema
class Image(dj.Manual):
    definition = """
    # table for storing
    -> Seed
    -> Dimension
    ----
    img  : external-raw    #  objects are stored as specified by dj.config['external-raw']
    """

    def make(self, key):
        np.random.seed(key['seed'])
        self.insert1(dict(key, img=np.random.rand(*(Dimension() & key).fetch1('dimensions'))))
