def top_decode(raw_data):
    def join_int_with_float(a, b):
        """Joins two integers with a dot and returns the float representation.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            float: The float representation of the joined integers.
        """

        joined_string = str(a) + "." + str(b)
        float_number = float(joined_string)
        return float_number
    
    result = []
    parent_mac_address = ""

    for data in raw_data:
        if data.get('type') == 'Gateway':
            parent_mac_address = data.get('mac', "")
            
        payload_mac_address = data.get('mac', "")
        json_data = {
            "measurement": "temphumid",
            "tags": {
                "mac_address": payload_mac_address,
                "gateway": parent_mac_address
            }
        }
        
        if raw_code := data.get('rawData'):

            range_step_offset = [raw_code[i:i+2] for i in range(0,len(raw_code),2)]
            frame_version = range_step_offset[8]

            # frame_version => 00 is Static Frames => Battery Level
            if frame_version == "00":
                # mac_address = "".join(range_step_offset[9:15][::-1])
                battery_level = int(range_step_offset[15], base=16)

                json_data.update({
                    "fields": {
                        "battery_level": battery_level
                    }
                })


            # frame_version => 05 is Temperature and Humidity Frames
            elif frame_version == "05":
                # device_name = "".join(range_step_offset[16:24])

                temperature_int = int(range_step_offset[12], base=16)
                temperature_point = int(range_step_offset[13], base=16)
                temperature = join_int_with_float(temperature_int, temperature_point)

                humidity_int = int(range_step_offset[14], base=16)
                humidity__point = int(range_step_offset[15], base=16)
                humidity = join_int_with_float(humidity_int, humidity__point)

                json_data.update({
                    "fields": {
                        "temperature": temperature,
                        "humidity": humidity
                    }
                })
            
            if json_data.get('fields'):
                result.append(json_data)
    
    return result


if __name__ == "__main__":
    raw_data = [
        {
            "timestamp": "2023-07-17T03:12:05.578Z",
            "type": "Gateway",
            "mac": "AC233FC12D21",
            "gatewayFree": 94,
            "gatewayLoad": 0.14000000000000001
        },
        {
            "timestamp": "2023-07-17T03:12:05.578Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -65,
            "rawData": "0201061BFF3906CA050100001B1829D34D535430315F340000000070CCB755"
        },
        {
            "timestamp": "2023-07-17T03:12:06.162Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -60,
            "rawData": "0201061BFF3906CA050100001B73290F4D535430315F32000000007860EE9C"
        },
        {
            "timestamp": "2023-07-17T03:12:10.744Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -71,
            "rawData": "0201061BFF3906CA00A13CAF3F23AC6461004000000040000004002814D0F5"
        },
        {
            "timestamp": "2023-07-17T03:12:15.584Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -65,
            "rawData": "0201061BFF3906CA050100001B1829D24D535430315F3400000000396F9921"
        },
        {
            "timestamp": "2023-07-17T03:12:15.795Z",
            "type": "Unknown",
            "mac": "AC233FAF3C94",
            "bleNo": 0,
            "bleName": "",
            "rssi": -67,
            "rawData": "0201061BFF3906CA00943CAF3F23AC6461004000000040000004006C8BE5CB"
        },
        {
            "timestamp": "2023-07-17T03:12:18.745Z",
            "type": "Unknown",
            "mac": "AC233FAE3033",
            "bleNo": 0,
            "bleName": "",
            "rssi": -60,
            "rawData": "0201061BFF3906CA003330AE3F23AC64610040000000400000040079BFED9B"
        },
        {
            "timestamp": "2023-07-17T03:12:24.422Z",
            "type": "Unknown",
            "mac": "AC233FAE3033",
            "bleNo": 0,
            "bleName": "",
            "rssi": -60,
            "rawData": "0201061BFF3906CA050100001B8D323E4D535430315F3500000000F85F2D1B"
        },
        {
            "timestamp": "2023-07-17T03:12:25.724Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -64,
            "rawData": "0201061BFF3906CA00A13CAF3F23AC6461004000000040000004009B5E0E57"
        },
        {
            "timestamp": "2023-07-17T03:12:31.195Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -65,
            "rawData": "0201061BFF3906CA009E3CAF3F23AC646100400000004000000400A3932F48"
        },
        {
            "timestamp": "2023-07-17T03:12:35.604Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -63,
            "rawData": "0201061BFF3906CA050100001B1429AB4D535430315F3400000000D4323C27"
        },
        {
            "timestamp": "2023-07-17T03:12:36.166Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -61,
            "rawData": "0201061BFF3906CA050100001B7629044D535430315F32000000004C7BB131"
        },
        {
            "timestamp": "2023-07-17T03:12:36.168Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -64,
            "rawData": "0201061BFF3906CA009E3CAF3F23AC646100400000004000000400C2554F28"
        },
        {
            "timestamp": "2023-07-17T03:12:41.633Z",
            "type": "Unknown",
            "mac": "AC233FAF3C94",
            "bleNo": 0,
            "bleName": "",
            "rssi": -68,
            "rawData": "0201061BFF3906CA050100001B39292B4D535430315F3300000000E8CE0E01"
        },
        {
            "timestamp": "2023-07-17T03:12:45.757Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -63,
            "rawData": "0201061BFF3906CA00A13CAF3F23AC646100400000004000000400E7D2CA05"
        },
        {
            "timestamp": "2023-07-17T03:12:46.180Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -65,
            "rawData": "0201061BFF3906CA050100001B7A29004D535430315F32000000002158F84D"
        },
        {
            "timestamp": "2023-07-17T03:12:48.759Z",
            "type": "Unknown",
            "mac": "AC233FAE3033",
            "bleNo": 0,
            "bleName": "",
            "rssi": -65,
            "rawData": "0201061BFF3906CA003330AE3F23AC6461004000000040000004008B8E2108"
        },
        {
            "timestamp": "2023-07-17T03:12:50.829Z",
            "type": "Unknown",
            "mac": "AC233FAF3C94",
            "bleNo": 0,
            "bleName": "",
            "rssi": -76,
            "rawData": "0201061BFF3906CA00943CAF3F23AC646100400000004000000400630E3FCF"
        },
        {
            "timestamp": "2023-07-17T03:12:51.209Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -64,
            "rawData": "0201061BFF3906CA009E3CAF3F23AC64610040000000400000040054A9B788"
        },
        {
            "timestamp": "2023-07-17T03:12:54.231Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA9",
            "bleNo": 0,
            "bleName": "",
            "rssi": -62,
            "rawData": "0201061BFF3906CA050100001B5C29194D535430315F3100000000890DD20A"
        },
        {
            "timestamp": "2023-07-17T03:12:54.330Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA9",
            "bleNo": 0,
            "bleName": "",
            "rssi": -59,
            "rawData": "0201061BFF3906CA00A93CAF3F23AC646100400000004000000400CEEB58B5"
        },
        {
            "timestamp": "2023-07-17T03:13:00.776Z",
            "type": "Unknown",
            "mac": "AC233FAF3CA1",
            "bleNo": 0,
            "bleName": "",
            "rssi": -63,
            "rawData": "0201061BFF3906CA00A13CAF3F23AC6461004000000040000004000A04440D"
        },
        {
            "timestamp": "2023-07-17T03:13:01.226Z",
            "type": "Unknown",
            "mac": "AC233FAF3C9E",
            "bleNo": 0,
            "bleName": "",
            "rssi": -63,
            "rawData": "0201061BFF3906CA009E3CAF3F23AC6461004000000040000004004A9644D0"
        }
    ]

    result = top_decode(raw_data)
    print(result)