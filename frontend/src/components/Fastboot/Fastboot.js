import React, {useEffect, useState} from 'react';
import FastbootDevice from "./FastbootDevice";
import {io} from "socket.io-client";
import {Col, Row} from "react-bootstrap";

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
    <Row className="g-0">
        {Object.keys(fastbootDevices).map((device) => (
            <Col key={device} style={{ maxWidth: '200px' }}>
                <FastbootDevice key={device} name={device} state={fastbootDevices[device].state} result={fastbootDevices[device].result} />
            </Col>
        ))}
    </Row>
  );
}

export default Fastboot;