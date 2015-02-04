import sys
import os
import csv
import json

def build_feature(row):
  feature = {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [row['stop_lon'], row['stop_lat']]
    },
    "properties": {k: v for k, v in row.items() if k not in ['stop_lon', 'stop_lat']}
  }
  return feature

if __name__ == "__main__":
  gtfs_file = sys.argv[1]
  outfile = None

  if len(sys.argv) == 3:
    outfile = sys.argv[2]

  # skeleton json object
  geojson_out = {
    "type": "FeatureCollection",
    "features": []
  };

  if not os.path.exists(gtfs_file):
    print "usage: gtfs-to-geojson <file.txt> <outfile>"
    sys.exit(1)

   # read in the gtfs/csv
  with open(gtfs_file, "r") as gtfs:
    for row in csv.DictReader(gtfs):
      geojson_out['features'].append(build_feature(row))

    # write the json file
    try:
      if not outfile:
        outfile = gtfs_file.split('.')
        outfile = outfile[0] + '.json'

      json_data = json.dumps(geojson_out, indent=2)
      fd = open(outfile, 'w')
      fd.write(json_data)
      fd.close()
    except Exception, e:
      raise