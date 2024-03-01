import React, {useState} from 'react';

import {Button, Spinner} from 'react-bootstrap';
import "./Home.css"
import axios from "axios";
import Device from "../Device/Device";

function Home() {
    const [loading, setLoading] = useState(false)
    const [deviceInfo, setDeviceInfo] = useState(
        {
        "cpu": {
            "Architecture": "armv7l",
            "BogoMIPS": "38.40",
            "Byte Order": "Little Endian",
            "CPU(s)": "0-3",
            "Core(s) per socket": "4",
            "Model": "1",
            "Model name": "Krait",
            "On-line CPU(s) list": "0-3",
            "Socket(s)": "1",
            "Stepping": "0x2",
            "Thread(s) per core": "1",
            "Vendor ID": "Qualcomm"
        },
        "device": {
            "arch": "armv7",
            "codename": "fairphone-fp2",
            "external_storage": "true",
            "keyboard": "false",
            "mac_address": "96:c5:0b:b9:0c:b2",
            "manufacturer": "Fairphone",
            "name": "Fairphone 2",
            "screen_height": "1920",
            "screen_width": "1080",
            "year": "2015"
        },
        "memory": {
            "available": "1.5G",
            "buff/cache": "118.1M",
            "free": "1.5G",
            "shared": "4.1M",
            "swap_free": "0",
            "swap_total": "0",
            "swap_used": "0",
            "total": "1.8G",
            "used": "238.8M"
        },
        "modem": {
            "apn": "--",
            "device-identifier": "ed481d276b85b32c55669b4dd6cd871f53970088",
            "ip-type": "--",
            "manufacturer": "QUALCOMM INCORPORATED",
            "model": "0",
            "modem.generic.state": "sim-missing",
            "operator-name": "--",
            "password": "--",
            "primary-port": "wwan0qmi0",
            "state-failed-reason": "sim-missing",
            "supported-ip-families.value": "ipv4v6",
            "user": "--"
        },
        "storage": {
            "Available": "21.5G",
            "Mounted": "/",
            "Size": "24.3G",
            "Use%": "7%",
            "Used": "1.6G"
        },
        "wifi": true
    }
    )
    const [error, setError] = useState("")

    function searchDevices(){
        setLoading(true)
        setError("")
        axios({
            method: "GET",
            url:"/api/search",
        })
        .then((response) => {
            setLoading(false)
            if(response.data.success){
                setDeviceInfo(response.data.data)
            }else {
                setError("No devices found")
            }
        }).catch((error) => {
            setLoading(false)
            setError(error)

            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
            }
        })
    }

    return (
        <div className="container">
            {Object.keys(deviceInfo).length > 0 ? // If devices are found then display the devices
                <Device deviceInfo={deviceInfo} />
            :
                loading ? // If no devices are found then display the search button
                    <Spinner className="center-spinner" animation="grow" variant="info" />
                    :
                    <Button className="w-25 p-4 center fw-bold" variant="info" style={{ fontSize: '3rem', color:"white" }} onClick={searchDevices}>Search</Button>
            }
            {error && <h4 style={{color:"red", margin:20}}>{error}</h4>}
        </div>
    )
}


export default Home;