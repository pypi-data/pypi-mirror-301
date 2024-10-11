import base64
from moapy.auto_convert import auto_schema
from moapy.data_post import ResultMD
from moapy.data_pre import UnitLoads
from moapy.rc_pre import SlabSection, GirderLength
from moapy.steel_pre import SteelMember_EC, ShearConnector
from moapy.dgnengine.base import load_dll, generate_report_xls, read_file_as_binary
from moapy.data_post import ResultBytes

@auto_schema
def report_ec4_composited_beam(steel: SteelMember_EC, shearconn: ShearConnector, slab: SlabSection, leng: GirderLength, load: UnitLoads) -> ResultMD:
    dll = load_dll()
    json_data_list = [steel.json(), shearconn.json(), slab.json(), leng.json(), load.json()]
    file_path = generate_report_xls(dll, 'Report_EC4_CompositedBeam', json_data_list)
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

# res = report_ec4_composited_beam(SteelMember_EC(), ShearConnector(), SlabSection(), GirderLength(), UnitLoads())
# print(res)