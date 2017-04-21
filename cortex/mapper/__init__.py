import os

import numpy as np

from .. import dataset
from mapper import Mapper

def get_mapper(subject, xfmname, type='nearest', recache=False, **kwargs):
    from ..database import db
    from . import point, patch, volume, line

    mapcls = dict(
        nearest=point.PointNN,
        trilinear=point.PointTrilin,
        gaussian=point.PointGauss,
        lanczos=point.PointLanczos,
        const_patch_nn=patch.ConstPatchNN,
        const_patch_trilin=patch.ConstPatchTrilin,
        const_patch_lanczos=patch.ConstPatchLanczos,
        line_nearest=line.LineNN,
        line_trilinear=line.LineTrilin)
    Map = mapcls[type]
    ptype = Map.__name__.lower()
    kwds ='_'.join(['%s%s'%(k,str(v)) for k, v in list(kwargs.items())])
    if len(kwds) > 0:
        ptype += '_'+kwds

    fname = "{xfmname}_{projection}.npz".format(xfmname=xfmname, projection=ptype)

    xfmfile = db.get_paths(subject)['xfmdir'].format(xfmname=xfmname)
    cachefile = os.path.join(db.get_cache(subject), fname)

    try:
        if not recache and (xfmname == "identity" or os.stat(cachefile).st_mtime > os.stat(xfmfile).st_mtime):
           return mapcls[type].from_cache(cachefile)
        raise Exception
    except Exception as e:
        return mapcls[type]._cache(cachefile, subject, xfmname, **kwargs)
