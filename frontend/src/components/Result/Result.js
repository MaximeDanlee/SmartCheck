import React, {useEffect, useState} from 'react';
import {Col, Row} from "react-bootstrap";
import Device from "./Device";
import {io} from "socket.io-client";

function Result() {
    const [resultdevices, setResultdevices] = useState({});

    useEffect(() => {
        const socket = io('/');
        socket.on('devices', (data) => {
            if(data && data.success){
                // setResultdevices(data.data)
                // filter devices that are done
                setResultdevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "done")));
            }
        });

        return () => {
            socket.disconnect();
        }
    }, []);

  return (
    <Row className="g-0">
        {Object.keys(resultdevices).map((device) => (
            <Col key={device} style={{ maxWidth: '200px' }}>
                <Device key={device} name={device} state={resultdevices[device].state} result={resultdevices[device].result} ip={resultdevices[device].ip} />
            </Col>
        ))}
    </Row>
  );
}

export default Result;