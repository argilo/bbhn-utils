import psycopg2
from datetime import *

class NodeDB:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=topology")
        self.cur = self.conn.cursor()

    def name(self, ip):
        self.cur.execute("""SELECT dest_name FROM last_seen
            WHERE dest_ip=%s""", (ip,))
        result = self.cur.fetchone()
        if result[0]:
            return result[0]
        else:
            return ip

    def last_seen(self, hours):
        self.cur.execute("""SELECT dest_ip, dest_name, ts,
            ts > NOW() - INTERVAL '%s hours'
            FROM last_seen
            ORDER BY dest_name""", (hours,))
        return self.cur.fetchall()

    def neighbours(self, ip, hours):
        self.cur.execute("""SELECT DISTINCT last_hop_ip FROM topology
            WHERE ts > NOW() - INTERVAL '%s hours'
            AND dest_ip=%s
            ORDER BY last_hop_ip""", (hours, ip))
        neighbours = self.cur.fetchall()
        for i, neighbour in enumerate(neighbours):
            neighbours[i] = (i,) + neighbour + (self.name(neighbour[0]),)
        return neighbours

    def cost_history(self, dest_ip, last_hop_ip, hours):
        now = datetime.now()
        self.cur.execute("""SELECT ts, lq * nlq FROM topology
            WHERE ts > NOW() - INTERVAL '%s hours'
            AND dest_ip=%s
            AND last_hop_ip=%s
            ORDER BY ts""", (hours, dest_ip, last_hop_ip))
        cost = []
        last_time = now - timedelta(hours=hours)
        for row in self.cur:
            interval_min = round((row[0] - last_time).total_seconds() / 60)
            if interval_min >= 2:
                cost.append((last_time + timedelta(minutes=1), 0))
            if interval_min >= 3:
                cost.append((row[0] - timedelta(minutes=1), 0))
            cost.append(row)
            last_time = row[0]
        interval_min = round((now - last_time).total_seconds() / 60)
        if interval_min >= 2:
            cost.append((last_time + timedelta(minutes=1), 0))
            cost.append((now, 0))
        return cost

    def close(self):
        self.cur.close()
        self.conn.close()
