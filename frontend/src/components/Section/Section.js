import React, {useEffect, useState} from 'react';
import RunningDevice from "../Running/RunningDevice";
import ReadyDevice from "../Ready/ReadyDevice";
import {io} from "socket.io-client";
import {Col, Row} from "react-bootstrap";
import ResultDevice from "../Result/ResultDevice";
import "./Section.css"
import WaitingDevice from "../Waiting/WaitingDevice";

function Section({section}) {
    const [devices, setDevices] = useState({});
    const [tests, setTests] = useState([]);
    const [fastbootDevices, setFastbootDevices] = useState( {});
    const [waitingDevices, setWaitingDevices] = useState({});

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
                    setWaitingDevices(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "waiting")));
                    console.log(Object.fromEntries(Object.entries(data.data).filter(([key, value]) => value.state === "waiting")));
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
                console.log(data.data);
                setTests(data.data);

            }
        });

        return () => {
            socket.disconnect();
        }
    }, [section]);

  return (
      <>
        <Row className="g-0 h-50">
            {Object.keys(devices).map((device) => (
                <Col key={device} style={{ maxWidth: '200px' }}>
                    {devices[device].state === "testing" || devices[device].state === "ready" ?
                        <RunningDevice key={device} name={device} state={devices[device].state} tests={tests[device]} ip={devices[device].ip} />
                        : <ResultDevice key={device} name={device} result={devices[device].result} ip={devices[device].ip} />
                    }

                </Col>
            ))}

            {Object.keys(fastbootDevices).map((device) => (
                <Col key={device} style={{ maxWidth: '200px' }}>
                    <ReadyDevice key={device} name={device} state={fastbootDevices[device].state} result={fastbootDevices[device].result} />
                </Col>
            ))}
        </Row>

        {section === "testing" ?
            <>
            <hr/>
                <Row className="g-0 h-50">
            {Object.keys(waitingDevices).map((device) => (
                <>
                    {tests[device] ?
                        <Col key={device} style={{ maxWidth: '200px' }}>
                            <WaitingDevice key={device} name={device} ip={waitingDevices[device].ip} test={tests[device].waiting} />
                        </Col>
                        : null}
                </>
            ))}
                    </Row>
            </>
            : null
        }

        </>

  );
}

export default Section;