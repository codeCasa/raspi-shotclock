import json
from models.drill_results import DrillResults

class DrillResultsRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS drill_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drill_name TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            elapsed_time INTEGER NOT NULL,
            shots_fired INTEGER NOT NULL,
            splits TEXT NOT NULL,
            average_split_time REAL,
            fastest_split_time REAL,
            slowest_split_time REAL,
            score REAL,
            notes TEXT
        )
        '''
        self.db_manager.execute_query(create_table_query)

    def upsert(self, drill_results):
        if drill_results.id is None:
            # Insert new record
            insert_query = '''
            INSERT INTO drill_results (
                drill_name, start_time, end_time, elapsed_time, shots_fired, splits, 
                average_split_time, fastest_split_time, slowest_split_time, score, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                drill_results.drill_name,
                drill_results.start_time,
                drill_results.end_time,
                drill_results.elapsed_time,
                drill_results.shots_fired,
                json.dumps(drill_results.splits),  # Store splits as JSON
                drill_results.average_split_time,
                drill_results.fastest_split_time,
                drill_results.slowest_split_time,
                drill_results.score,
                drill_results.notes
            )
            self.db_manager.execute_query(insert_query, params)
            
            # Retrieve the last inserted ID and set it in the drill_results object
            drill_results.id = self.db_manager.execute_query("SELECT last_insert_rowid()")[0][0]
        else:
            # Update existing record
            update_query = '''
            UPDATE drill_results
            SET drill_name = ?, start_time = ?, end_time = ?, elapsed_time = ?, shots_fired = ?, 
                splits = ?, average_split_time = ?, fastest_split_time = ?, slowest_split_time = ?, 
                score = ?, notes = ?
            WHERE id = ?
            '''
            params = (
                drill_results.drill_name,
                drill_results.start_time,
                drill_results.end_time,
                drill_results.elapsed_time,
                drill_results.shots_fired,
                json.dumps(drill_results.splits),  # Store splits as JSON
                drill_results.average_split_time,
                drill_results.fastest_split_time,
                drill_results.slowest_split_time,
                drill_results.score,
                drill_results.notes,
                drill_results.id
            )
            self.db_manager.execute_query(update_query, params)

    def delete(self, drill_results_id):
        delete_query = 'DELETE FROM drill_results WHERE id = ?'
        self.db_manager.execute_query(delete_query, (drill_results_id,))

    def select(self, drill_results_id):
        select_query = 'SELECT * FROM drill_results WHERE id = ?'
        result = self.db_manager.execute_query(select_query, (drill_results_id,))
        if result:
            row = result[0]
            return DrillResults(
                id=row[0],
                drill_name=row[1],
                start_time=row[2],
                end_time=row[3],
                elapsed_time=row[4],
                shots_fired=row[5],
                splits=json.loads(row[6]),
                average_split_time=row[7],
                fastest_split_time=row[8],
                slowest_split_time=row[9],
                score=row[10],
                notes=row[11]
            )
        return None

    def count(self):
        count_query = 'SELECT COUNT(*) FROM drill_results'
        result = self.db_manager.execute_query(count_query)
        return result[0][0] if result else 0
    
    def get_results_for_drill(self, drill, offset=0, limit=25):
        """
        Fetches a paginated list of results for a specific drill.

        :param drill: The drill for which results are fetched.
        :param offset: The offset from where to start fetching results.
        :param limit: The maximum number of results to fetch.
        :return: A list of drill results.
        """
        query = """
        SELECT *
        FROM drill_results
        WHERE drill_name = ?
        ORDER BY end_time DESC
        LIMIT ? OFFSET ?
        """
        cursor = self.db_manager.cursor()
        rows = []
        try:
            cursor.execute(query, (drill.name, limit, offset))
            rows = cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()

        results = []
        for row in rows:
            result = DrillResults(
                id=row[0],
                drill_name=row[1],
                start_time=row[2],
                end_time=row[3],
                elapsed_time=row[4],
                shots_fired=row[5],
                splits=json.loads(row[6]),
                average_split_time=row[7],
                fastest_split_time=row[8],
                slowest_split_time=row[9],
                score=row[10],
                notes=row[11]
            )
            results.append(result)
        return results
    
    def get_results_for_drill_name(self, name, between=None):
        query = """
        SELECT *
        FROM drill_results
        WHERE drill_name = ?
        ORDER BY end_time
        """ if between is None else """
        SELECT *
        FROM drill_results
        WHERE drill_name = ?
        AND start_time >= ?
        AND end_time <= ?
        ORDER BY end_time DESC
        """
        cursor = self.db_manager.cursor()
        rows = []
        try:
            if between is None:
                cursor.execute(query, (name,))
            else:
                cursor.execute(query, (name, between[0], between[1]))
            rows = cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()

        results = []
        for row in rows:
            result = DrillResults(
                id=row[0],
                drill_name=row[1],
                start_time=row[2],
                end_time=row[3],
                elapsed_time=row[4],
                shots_fired=row[5],
                splits=json.loads(row[6]),
                average_split_time=row[7],
                fastest_split_time=row[8],
                slowest_split_time=row[9],
                score=row[10],
                notes=row[11]
            )
            results.append(result)
        return results
