import datetime
import unittest

from influxobject.influxpoint import InfluxPoint


class TestSimple(unittest.TestCase):

    # def test_add(self):
    #     self.assertEqual((InfluxObject(5) + InfluxObject(6)).value, 11)

    # def test_create(self):
    #     influx_object = InfluxObject(5)
    #     self.assertEqual(InfluxObject(5).value, 5)

    def test_init(self):
        influx_point = InfluxPoint()
        influx_point.set_measurement("measurement")
        self.assertEqual(influx_point.measurement, "measurement")

    def test_invalid_tags(self):
        influx_point = InfluxPoint()
        with self.assertRaises(TypeError):
            influx_point.set_tags({"tag1": 1})

    def test_invalid_fields(self):
        influx_point = InfluxPoint()
        with self.assertRaises(TypeError):
            influx_point.set_fields({"field1": {"":""}})

    def test_tags(self):
        influx_point = InfluxPoint()
        influx_point.tags = {"tag1": "value1"}
        self.assertEqual(influx_point.tags, {"tag1": "value1"})

        influx_point.add_tag("tag2", "value2")
        self.assertEqual(influx_point.tags, {"tag1": "value1", "tag2": "value2"})

        influx_point.remove_tag("tag1")
        self.assertEqual(influx_point.tags, {"tag2": "value2"})

    def test_fields(self):
        influx_point = InfluxPoint()
        influx_point.fields = {"field1": 1}
        self.assertEqual(influx_point.fields, {"field1": 1})

        influx_point.add_field("field2", 2)
        self.assertEqual(influx_point.fields, {"field1": 1, "field2": 2})

        influx_point.remove_field("field1")
        self.assertEqual(influx_point.fields, {"field2": 2})

    def test_timestamp(self):
        influx_point = InfluxPoint()
        influx_point.timestamp = "2021-01-01T00:00:00Z"
        self.assertEqual(influx_point.timestamp, "2021-01-01T00:00:00Z")

    def test_line_protocol(self):
        influx_point = InfluxPoint()
        influx_point.set_measurement("measurement")
        influx_point.set_tags({"tag1": "value1"})
        influx_point.set_fields({"field1": 1, "field2": 2})
        influx_point.set_timestamp(datetime.datetime(2021, 1, 1))
        self.assertEqual(
            influx_point.to_line_protocol(),
            "measurement,tag1=value1 field1=1,field2=2 1609455600",
        )

    def test_json(self):
        influx_point = InfluxPoint()
        influx_point.set_measurement("measurement")
        influx_point.set_tags({"tag1": "value1"})
        influx_point.set_fields({"field1": 1, "field2": 2})
        influx_point.set_timestamp(datetime.datetime(2021, 1, 1))
        self.assertEqual(
            influx_point.to_json(),
            {
                "measurement": "measurement",
                "tags": {"tag1": "value1"},
                "fields": {"field1": 1, "field2": 2},
                "timestamp": 1609455600,
            },
        )

        self.assertEqual(
            influx_point.to_line_protocol(),
            "measurement,tag1=value1 field1=1,field2=2 1609455600",
        )

    def test_empty(self):
        influx_point = InfluxPoint()

        # Validate the iflux_point and ensure it raises a ValueError
        with self.assertRaises(ValueError):
            influx_point.to_line_protocol()

        # Validate the ValueError message
        try:
            influx_point.to_line_protocol()
        except ValueError as e:
            self.assertEqual(str(e), "Measurement is not set, Fields are not set, Tags are not set")

        # Set the measurement
        influx_point.set_measurement("measurement")
        try:
            influx_point.to_line_protocol()
        except ValueError as e:
            self.assertEqual(str(e), "Fields are not set, Tags are not set")

        # Set the timestamp
        influx_point.set_timestamp(datetime.datetime(2021, 1, 1))

        # Validate the line protocol
        try:
            influx_point.to_line_protocol()
        except ValueError as e:
            self.assertEqual(str(e), "Fields are not set, Tags are not set")

        # Set the fields
        influx_point.set_fields({"field1": 1, "field2": 2})

        # Validate the line protocol
        try:
            influx_point.to_line_protocol()
        except ValueError as e:
            self.assertEqual(str(e), "Tags are not set")

        # Set the tags
        influx_point.set_tags({"tag1": "value1"})

        # Validate the line protocol
        self.assertEqual(
            influx_point.to_line_protocol(),
            "measurement,tag1=value1 field1=1,field2=2 1609455600",
        )

    def test_json_to_influxobject(self):
      json_object = {
          "measurement": "measurement",
          "tags": {"tag1": "value1"},
          "fields": {"field1": 1, "field2": 2},
          "timestamp": 1609455600,
      }

      influx_point = InfluxPoint()
      influx_point.from_json(json_object)
      self.assertEqual(influx_point.to_json(), json_object)
      self.assertEqual(influx_point.to_line_protocol(), "measurement,tag1=value1 field1=1,field2=2 1609455600")

    def test_line_protocol_to_influxobject(self):
      line_protocol = "measurement,tag1=value1 field1=1,field2=2 1609455600"
      influx_point = InfluxPoint()
      influx_point.parse_line_protocol(line_protocol)
      self.assertEqual(influx_point.to_line_protocol(), line_protocol)
      self.assertEqual(influx_point.to_json(), {
          "measurement": "measurement",
          "tags": {"tag1": "value1"},
          "fields": {"field1": 1, "field2": 2},
          "timestamp": 1609455600,
      })

    def test_complex_line_protocol(self):
        line_protocol = "co2\ mfc\ sp,department=mbp,device=R2,institute=unlock,reactor=R2,study=Stability-1,topic=unlock/mbp/R2/co2\ mfc\ sp co2\ mfc\ sp=0 1709975216000000000"
        InfluxPoint().parse_line_protocol(line_protocol)
        self.assertEqual(True, True)

    def test_complex_json(self):
        json = {
            "measurement": "co2 mfs sp",
            "tags": {"department": "mbp", "batch_id": 6.0, "topic": "bioind4/wur/ssb/indepensim/batch_id_6/acid_flow_rate"},
            "fields": {"Acid flow rate": 0.0},
            "timestamp": 1700000000,
        }
        influx_point = InfluxPoint()
        influx_point.from_json(json)
        self.assertEqual(influx_point.to_json(), json)
        self.assertEqual(influx_point.to_line_protocol(), "co2 mfs sp,department=mbp,batch_id=6.0,topic=bioind4/wur/ssb/indepensim/batch_id_6/acid_flow_rate Acid flow rate=0.0 1700000000")
        with open("test.txt", "w") as f:
            f.write(influx_point.to_line_protocol())


    def test_set_timepoint(self):
        influx = InfluxPoint()
        influx.add_field("co2 mfc sp", 0)
        influx.add_tag("department", "mbp")
        influx.set_measurement("co2 mfc sp")
        influx.set_timestamp(1465839830100400200)
        print(influx)

if __name__ == "__main__":
    unittest.main()
