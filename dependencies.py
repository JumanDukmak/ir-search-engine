import aiohttp
from fastapi import HTTPException


async def call_external_service(endpoint: str, params: dict):

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/"+endpoint, params=params) as response:
            if response.status == 200:
                data = await response.json()
                #print("from caller",data)
                return data  
            else:
                return {"error": f"Failed to retrieve data, status code: {response.status}"}
#-------------------------------------------------------------------------------------------------------#
async def call_post_external_service(endpoint: str, data):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/" + endpoint, json=data) as response:
            if response.status == 200:
                data = await response.json()
                #print("from caller",data)
                return data 
            else:
                return {"error": f"Failed to retrieve data, status code: {response.status}"}