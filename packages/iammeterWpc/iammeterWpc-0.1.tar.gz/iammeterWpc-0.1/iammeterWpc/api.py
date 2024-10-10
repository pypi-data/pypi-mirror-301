import aiohttp
import asyncio

class IammeterWpcAPI:
    timeout = aiohttp.ClientTimeout(total=5)
    def __init__(self, ip):
        self.base_url = f"http://{ip}"

    async def get_monitor_data(self):
        url = f"{self.base_url}/api/monitor"
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # 抛出HTTP错误
                    return await response.json()
        except aiohttp.ClientError as e:
            return {"error": f"Connection error: {str(e)}"}

    async def set_wpc_adv(self, run_mode=None, max_power=None, meter_address=None, meter_config=None, time_config=None,
                      threshold=None, hysteresis=None, tz_offset=None, start_hour=None, 
                      stop_hour=None, meter_type=None, restore_power=None, ntp_server=None):
        url = f"{self.base_url}/api/setwpcadv"
        data = {
            "runMode": run_mode,
            "maxPower": max_power,
            "meterAddress": meter_address,
            "meterConfig": meter_config,
            "timeConfig": time_config,
            "threshold": threshold,
            "hysteresis": hysteresis,
            "tzOffset": tz_offset,
            "startHour": start_hour,
            "stopHour": stop_hour,
            "meterType": meter_type,
            "restorePower": restore_power,
            "ntpServer": ntp_server
        }
        data = {key: value for key, value in data.items() if value is not None}
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=data) as response:
                    response.raise_for_status()  # 抛出HTTP错误
                    result = await response.json()
                    if result.get("successful") == 1:
                        return {"successful": True, "message": result.get("message")}
                    else:
                        return {"successful": False, "message": "Unknown response"}
        except aiohttp.ClientError as e:
            return {"error": f"Connection error: {str(e)}"}

    async def set_power(self, value):
        url = f"{self.base_url}/api/setpower?value={value}"
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # 抛出HTTP错误
                    result = await response.json()
                    return {"setpower": result.get("setpower")}
        except aiohttp.ClientError as e:
            return {"error": f"Connection error: {str(e)}"}


