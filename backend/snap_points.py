import pg8000.native

try:
    con = pg8000.native.Connection('postgres', password='Kiendang2207@', database='railway_db')
    
    sql_stations = """
    UPDATE stations
    SET geom = (
        SELECT ST_ClosestPoint(r.geom, stations.geom)
        FROM railways r
        ORDER BY ST_Distance(r.geom, stations.geom)
        LIMIT 1
    );
    """
    
    sql_devices = """
    UPDATE warning_devices
    SET geom = (
        SELECT ST_ClosestPoint(r.geom, warning_devices.geom)
        FROM railways r
        ORDER BY ST_Distance(r.geom, warning_devices.geom)
        LIMIT 1
    );
    """
    
    con.run(sql_stations)
    con.run(sql_devices)
    con.close()
    print("Snapped successfully!")
except Exception as e:
    print("Error:", e)
