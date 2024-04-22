import React, {useEffect, useState} from 'react';
import TestingDevice from "../Testing/TestingDevice";
import FastbootDevice from "../Fastboot/FastbootDevice";
import {io} from "socket.io-client";
import {Col, Row} from "react-bootstrap";
import ResultDevice from "../Result/ResultDevice";

function Section({section}) {
    const [devices, setDevices] = useState({});
    const [tests, setTests] = useState([]);
    const [fastbootDevices, setFastbootDevices] = useState( {});

    useEffect(() => {
        const socket = io('/');
        socket.on('devices', (data) => {
            if(data && data.success){
                // setDevices(data.data)
                if(section === "ready") {
                    setDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "ready" || value.state === "failed")));
                }

                if(section === "testing") {
                    setDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "testing")));
                }

                if(section === "result") {
                    setDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "done")));
                }
            }
        });

        socket.on('fastboot_devices', (data) => {
            if(data && data.success) {
                if(section === "ready") {
                    setFastbootDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "ready" || value.state === "failed")));
                }

                if(section === "testing") {
                    setFastbootDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "testing" || value.state === "flashing")));
                }
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
    }, [section]);

  return (
    <Row className="g-0">
        {Object.keys(devices).map((device) => (
            <Col key={device} style={{ maxWidth: '200px' }}>
                {devices[device].state === "testing" || devices[device].state === "ready" ?
                    <TestingDevice key={device} name={device} state={devices[device].state} tests={tests[device]} ip={devices[device].ip} />
                    : <ResultDevice key={device} name={device} result={devices[device].result} ip={devices[device].ip} />
                }

            </Col>
        ))}

        {Object.keys(fastbootDevices).map((device) => (
            <Col key={device} style={{ maxWidth: '200px' }}>
                <FastbootDevice key={device} name={device} state={fastbootDevices[device].state} result={fastbootDevices[device].result} />
            </Col>
        ))}
    </Row>
  );
}

export default Section;