import spark_sdk as ss
import os
try:
    from PIL import Image
except:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 Pillow")
    from PIL import Image
    pass


try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

from cads_sdk.nosql.etl import read_mp3,read_pcm

import base64
import io

from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    overload,
    TYPE_CHECKING,
)
from pyspark.sql.column import Column
from pyspark.sql.functions import input_file_name

import pandas as pd
pd.options.display.width = 200


def cvtColor(binary):
    b,g,r = Image.open(io.BytesIO(binary)).split()
    return Image.merge("RGB", (r, g, b))

def openImage(binary):
    return Image.open(io.BytesIO(binary))

def get_thumbnail(i):
    width = pd.options.display.width
    i.thumbnail((width, width), Image.LANCZOS)
    return i

def image_base64(im):
    # if isinstance(im, str):
    #     im = get_thumbnail(im)
    im = get_thumbnail(im)    
    with io.BytesIO() as buffer:
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'
    # return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'

def read_pdf_pq(parquet_file, contract):
    import os
    import subprocess
    from pyarrow import fs
    import pyarrow.parquet as pq
    import pyarrow as pa
    import pandas as pd

    os.environ['HADOOP_CONF_DIR'] = "/etc/hadoop/conf/"
    os.environ['JAVA_HOME'] = "/usr/jdk64/jdk1.8.0_112"
    os.environ['HADOOP_HOME'] = "/usr/hdp/3.1.0.0-78/hadoop"
    os.environ['ARROW_LIBHDFS_DIR'] = "/usr/hdp/3.1.0.0-78/usr/lib/"
    os.environ['CLASSPATH'] = subprocess.check_output("$HADOOP_HOME/bin/hadoop classpath --glob", shell=True).decode('utf-8')

    hdfs = fs.HadoopFileSystem(host="hdfs://hdfs-cluster.datalake.bigdata.local", port=8020)
    
    pdf_all = pd.DataFrame()
    for r in parquet_file:
        p = r.file_name.replace("hdfs://hdfs-cluster.datalake.bigdata.local:8020", "")
        df_pq = pq.read_table(p, filesystem = hdfs, filters=[('contract', '=', contract)])
        pdf = df_pq.to_pandas()
        pdf_all = pd.concat([pdf_all, pdf])
    return pdf_all


def read_img_id_card(contract, limit:int = 100, mode='RGB'):
    """
    Function to display image in parquet as a DataFrame
    Parameters
    ----------
    limit : int
        Default: 100
        Limit number of display image at the same time
        Maxium is 100
    mode : str
        Color mode 
        Default: 'RGB'
        RGB or BGR
        
    """
    if limit > 100:
        limit = 100
    import spark_sdk as ss
    import pandas as pd
    
    
    df = ss.sql(f"""select contract, file_name from ftel_dwh_isc.img_id_card_metadata where contract = "{contract}" """)
    pdf = read_pdf_pq(df.select('file_name').distinct().collect(), contract)
    
    
    need_convert_dict = {}
    for c in pdf.columns:
        if c == "image":
            if mode=='BGR':
                pdf[c] = pdf[c].apply(cvtColor)
            else:
                pdf[c] = pdf[c].apply(openImage)
            need_convert_dict[c] = image_formatter
    from pandas import DataFrame
    DataFrame.need_convert_dict = need_convert_dict
    pdf.need_convert_dict = need_convert_dict
    return pdf

from pandas._config import get_option
from io import StringIO
from pandas.io.formats import format as fmt
from typing import Optional

def _repr_html_(self) -> Optional[str]:
    """
    Function display Image with pandas
    Return a html representation for a particular DataFrame.
    Mainly for IPython notebook.
    """
    if self._info_repr():
        buf = StringIO()
        self.info(buf=buf)
        # need to escape the <class>, should be the first line.
        val = buf.getvalue().replace("<", r"&lt;", 1)
        val = val.replace(">", r"&gt;", 1)
        return f"<pre>{val}</pre>"

    if get_option("display.notebook_repr_html"):
        max_rows = get_option("display.max_rows")
        min_rows = get_option("display.min_rows")
        max_cols = get_option("display.max_columns")
        show_dimensions = get_option("display.show_dimensions")
        
        if 'need_convert_dict' not in self.__dict__:
            if self._is_copy:
                pass
            else:
                self.need_convert_dict = {}
                
        formatter = fmt.DataFrameFormatter(
            self,
            columns=None,
            col_space=None,
            na_rep="NaN",
            formatters=self.need_convert_dict,
            float_format=None,
            sparsify=None,
            justify=None,
            index_names=True,
            header=True,
            index=True,
            bold_rows=True,
            escape=False,
            max_rows=max_rows,
            min_rows=min_rows,
            max_cols=max_cols,
            show_dimensions=show_dimensions,
            decimal=".",
        )
        
        return fmt.DataFrameRenderer(formatter).to_html()
    else:
        return None

from pandas import DataFrame
DataFrame._repr_html_ = _repr_html_