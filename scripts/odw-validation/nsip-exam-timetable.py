import csv
from collections import defaultdict
import pprint
import model_nsip_exam_timetable
from pydantic import BaseModel, ValidationError

_event_fields = dict(model_nsip_exam_timetable.Event.__annotations__.items())
_event_dict = {k.lower(): v for k, v in _event_fields.items()}

_excluded_fields = [k.lower() for k, v in _event_dict.items()]

_file_name = r"C:\Users\ChrisTopping\Downloads\nsip-exam-timetable-sample.csv"

_data = []

with open(_file_name, encoding="utf-8-sig") as csvfile:
    _reader = csv.DictReader(csvfile)
    _data.extend(_reader)

_merged_data = defaultdict(dict)

for row in _data[:1]:
    _lowercase_row = {k.lower(): v for k, v in row.items()}
    _caseReference = _lowercase_row["casereference"]
    if _caseReference not in _merged_data:
        _merged_data[_caseReference] = {
            k: v for k, v in _lowercase_row.items() if k.lower() not in _excluded_fields
        }
        _merged_data[_caseReference]["events"] = []

    _events = _merged_data[_caseReference]["events"]
    _new_event = {k.lower(): _lowercase_row[k] for k, v in _event_dict.items()}
    if _new_event not in _events:
        _events.append(_new_event)

_final_data = list(_merged_data.values())


class ExaminationTimetableInstances(BaseModel):
    data: list[model_nsip_exam_timetable.ExaminationTimetable]


pprint.pprint(_final_data)

try:
    ExaminationTimetableInstances(data=_final_data)
except ValidationError as e:
    print(e)
    pprint.pprint(e.errors())
