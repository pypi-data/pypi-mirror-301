import base64
from moapy.auto_convert import auto_schema
from moapy.data_pre import MemberForce, EffectiveLength
from moapy.steel_pre import SteelSection, SteelLength
from moapy.alu_pre import AluMaterial, AluMomentModificationFactor
from moapy.dgnengine.base import generate_report_xls, load_dll, read_file_as_binary
from moapy.data_post import ResultBytes

@auto_schema
def report_aluminum_beam_column(matl: AluMaterial, sect: SteelSection, load: MemberForce, length: SteelLength, eff_len: EffectiveLength, factor: AluMomentModificationFactor) -> ResultBytes:
    dll = load_dll()
    json_data_list = [matl.json(), sect.json(), load.json(), length.json(), eff_len.json(), factor.json()]
    file_path = generate_report_xls(dll, 'Report_Aluminum_BeamColumn', json_data_list)
    return ResultBytes(type="xlsx", result=base64.b64encode(read_file_as_binary(file_path)).decode('utf-8'))

# data = {
#   "matl": {
#     "code": "AA(A)",
#     "matl": "2014-T6",
#     "product": "Extrusions"
#   },
#   "sect": {
#     "shape": "H",
#     "name": "H 400x200x8/13"
#   },
#   "load": {
#     "Nz": {
#       "value": 0,
#       "unit": "kN"
#     },
#     "Mx": {
#       "value": 0,
#       "unit": "kN.m"
#     },
#     "My": {
#       "value": 0,
#       "unit": "kN.m"
#     },
#     "Vx": {
#       "value": 0,
#       "unit": "kN"
#     },
#     "Vy": {
#       "value": 0,
#       "unit": "kN"
#     }
#   },
#   "length": {
#     "l_x": {
#       "value": 3000,
#       "unit": "mm"
#     },
#     "l_y": {
#       "value": 3000,
#       "unit": "mm"
#     },
#     "l_b": {
#       "value": 3000,
#       "unit": "mm"
#     }
#   },
#   "eff_len": {
#     "kx": 1,
#     "ky": 1
#   },
#   "factor": {
#     "c_mx": 1,
#     "c_my": 1,
#     "cb": 1,
#     "m": 1
#   }
# }
# res = report_aluminum_beam_column(**data)
# res.dict()
# print(res)
