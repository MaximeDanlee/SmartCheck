import React, {useEffect, useState} from 'react';
import Device from "./Device";
import {io} from "socket.io-client";
import {Col, Row} from "react-bootstrap";

function Testing() {
    const [devices, setDevices] = useState({});
    const [tests, setTests] = useState([]);

    useEffect(() => {
        const socket = io('/');
        socket.on('devices', (data) => {
            if(data && data.success){
                // setDevices(data.data)
                setDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state !== "done")));
            }
        });

        socket.on('testing', (data) => {
            if(data && data.success){
                setTests(data.data);
            }
        });

        return () => {
            socket.disconnect();
        }
    }, []);

  return (
    <Row className="g-0">
        {Object.keys(devices).map((device) => (
            <Col key={device} style={{ maxWidth: '200px' }}>
                <Device key={device} name={device} state={devices[device].state} tests={tests[device]} ip={devices[device].ip} />
            </Col>
        ))}
    </Row>
  );
}

export default Testing;