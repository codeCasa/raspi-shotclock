import json

class DrillResults:
    def __init__(self, drill_name, start_time, end_time, elapsed_time, shots_fired, splits, average_split_time=None, fastest_split_time=None, slowest_split_time=None, score=None, notes=None, id=None):
        self.id = id  # ID is None by default, will be set after insertion into the database
        self.drill_name = drill_name
        self.start_time = start_time
        self.end_time = end_time
        self.elapsed_time = elapsed_time
        self.shots_fired = shots_fired
        self.splits = splits
        self.average_split_time = average_split_time
        self.fastest_split_time = fastest_split_time
        self.slowest_split_time = slowest_split_time
        self.score = score
        self.notes = notes

    def to_json(self):
        return json.dumps({
            'id': self.id,
            'drill_name': self.drill_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'elapsed_time': self.elapsed_time,
            'shots_fired': self.shots_fired,
            'splits': self.splits,
            'average_split_time': self.average_split_time,
            'fastest_split_time': self.fastest_split_time,
            'slowest_split_time': self.slowest_split_time,
            'score': self.score,
            'notes': self.notes
        })

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return DrillResults(
            id=data.get('id'),
            drill_name=data['drill_name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            elapsed_time=data['elapsed_time'],
            shots_fired=data['shots_fired'],
            splits=data['splits'],
            average_split_time=data.get('average_split_time'),
            fastest_split_time=data.get('fastest_split_time'),
            slowest_split_time=data.get('slowest_split_time'),
            score=data.get('score'),
            notes=data.get('notes')
        )
