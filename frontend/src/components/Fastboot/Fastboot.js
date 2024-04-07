import React, {useEffect, useState} from 'react';
import FastbootDevice from "./FastbootDevice";
import {io} from "socket.io-client";

function Fastboot() {
    const [fastbootDevices, setFastbootDevices] = useState( {});

    useEffect(() => {
        const socket = io('/');
        socket.on('fastboot_devices', (data) => {
            setFastbootDevices(data.data);
        });

        return () => {
            socket.disconnect();
        }
    }, []);

  return (
    <div>
        {Object.keys(fastbootDevices).map((device) => (
            <FastbootDevice key={device} name={device} state={fastbootDevices[device].state} result={fastbootDevices[device].result} />
        ))}
    </div>
  );
}

export default Fastboot;