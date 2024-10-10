
import asyncio
from api import IammeterWpcAPI

async def main():
    device = IammeterWpcAPI('194.36.24.125')
    monitor_data = await device.get_monitor_data()
    print(monitor_data)

    result = await device.set_wpc_adv(
        #run_mode=1,
        max_power=2000,
        #meter_address="100.10.30.135",
        meter_config="1,1,1",
        threshold=0,
        hysteresis=0,
        tz_offset=0,
        start_hour=0,
        stop_hour=0,
        meter_type=0,
        restore_power=0,
        ntp_server="ntp1.aliyun.com"
    )
    print(result)

    power_result = await device.set_power(5000)  # set power to 5000
    print(power_result)

if __name__ == "__main__":
    asyncio.run(main())