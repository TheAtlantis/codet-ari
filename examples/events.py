#!/usr/bin/env python

"""Brief example of using the Events API.

This app will subscribe to all Asterisk event and bind each event to a method
"""

import ari

client = ari.connect('http://localhost:8088/', 'hey', 'peekaboo')




def on_DeviceStateChanged(event):    
    name = event.get("device_state").get("name")
    state = event.get("device_state").get("state")
    timestamp = event.get("timestamp")
    print("{} : Device {} is {}".format(timestamp, name, state))
    
def on_ContactStatusChange(event):      
    name = "{}/{}".format(event.get("endpoint").get("technology"), event.get("endpoint").get("resource"))
    contact_uri = event.get("contact_info").get("uri")
    contact_status = event.get("contact_info").get("contact_status")
    contact_roundtrip = event.get("contact_info").get("roundtrip_usec")
    timestamp = event.get("timestamp")
    
    print("{} : Last Contact {} is {} at {} with {} ms".format(timestamp, name, contact_status, contact_uri, contact_roundtrip))

def on_PeerStatusChange(event):
    name = "{}/{}".format(event.get("endpoint").get("technology"), event.get("endpoint").get("resource"))
    peer_status = event.get("peer").get("peer_status")
    timestamp = event.get("timestamp")
    
    print("{} : Peer {} is {}".format(timestamp, name, peer_status))

def on_ChannelDialplan(event):   
    if event.get("dialplan_app") == "AppDial" :
        timestamp = event.get("timestamp")
        number_from = event.get("channel").get("caller").get("number")
        number_to = event.get("channel").get("connected").get("number")
        state = event.get("channel").get("state")           
        
        print("{} : {} AppDial {} : {}".format(timestamp, number_from, number_to, state))

def on_Dial(event):
    timestamp = event.get("timestamp")
    number_from = event.get("caller").get("caller").get("number")
    number_to = event.get("peer").get("caller").get("number")
    state = event.get("dialstatus")          
    
    print("{} : {} Call {} : {}".format(timestamp, number_from, number_to, state))
    
def on_HangupRequest(event):
    timestamp = event.get("timestamp")
    number_from = event.get("channel").get("caller").get("number")
    number_to = event.get("channel").get("connected").get("number")
    
    print("{} : {} Hangup {}".format(timestamp, number_from, number_to))  


client.on_event("DeviceStateChanged", on_DeviceStateChanged)
client.on_event("PeerStatusChange", on_PeerStatusChange)
client.on_event("ContactStatusChange", on_ContactStatusChange)
client.on_event("ChannelDialplan", on_ChannelDialplan)
client.on_event("Dial", on_Dial)
client.on_event("ChannelHangupRequest", on_HangupRequest)



# Run the WebSocket
client.run(apps="hello", subscribeAll="true")
