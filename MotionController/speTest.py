"""Test module for exporting multi-frame spectral data into a
single grid. A spe file is input and a .xlsx Excel worksheet is
output to the present working directory.

If the spe data contains a wavelength calibration,
it will be extracted from the `SpeReference` object and used as
column headers in the exported spreadsheet.

The frame data in the spe file must be spectral -- i.e. 1 row only.

Uses numpy, openpyxl, and pandas external libraries.
"""

import numpy as np
from pandas import DataFrame as df
from read_spe import SpeReference

if __name__ == '__main__':
    #TODO: Replace 'Sample1.spe' with a path to your spe file.
    spe_ref = SpeReference(r'C:\Users\MoodyLab3\Documents\LightField\PLmap_demo_PL 2024-02-16 17_24_40 36.spe')
    data = spe_ref.get_data(rois=[0], frames=[0,2])
    print(data)