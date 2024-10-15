from typing import List, Dict, Optional
from dcentrapi.requests_dappi import requests_post
from dcentrapi.Base import Base


class EventPoller(Base):
    def register_user(self, user_name: str, collection_name: str):
        url = self.url + "event_poller/user/register"
        data = {
            "user_name": user_name,
            "collection_name": collection_name,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def subscribe_contract(
        self,
        contract_address: str,
        contract_name: str,
        abi: List[dict],
        chain_id: str,
        deployment_block_number: int,
        webhook_url: Optional[str] = None,
        webhook_subscribed_events: Optional[List[str]] = None,
    ):
        url = self.url + "event_poller/contract/subscribe"
        data = {
            "contract_name": contract_name,
            "contract_address": contract_address,
            "abi": abi,
            "chain_id": chain_id,
            "deployment_block_number": deployment_block_number,
            "webhook_url": webhook_url,
            "webhook_subscribed_events": webhook_subscribed_events,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()

    def get_events(
        self,
        chain_contract_map: Optional[Dict[str, Optional[List[str]]]] = None,
        event_args: Optional[Dict[str, Optional[List[str]]]] = None,
        event_names: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        user_web3_addresses: Optional[List[str]] = None,
        block_number: Optional[int] = None,
    ):
        url = self.url + "event_poller/events"
        data = {
            "chain_contract_map": chain_contract_map,
            "event_args": event_args,
            "event_names": event_names,
            "start_time": start_time,
            "end_time": end_time,
            "user_web3_addresses": user_web3_addresses,
            "block_number": block_number,
        }
        response = requests_post(url=url, json=data, headers=self.headers)
        return response.json()
