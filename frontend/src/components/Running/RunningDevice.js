import React, {useEffect, useRef, useState} from 'react';
import {Button, Card, ProgressBar} from "react-bootstrap";
import "./RunningDevice.css"
import {io} from "socket.io-client";
import axios from "axios";

function RunningDevice({name, state, tests, ip}) {
    const [now, setNow] = useState(0);
    const testsRef = useRef(null);

    function launchTests() {
        const socket = io('/');
        socket.emit('launch_all_test', name, ip);
    }

    useEffect(() => {
        axios.get('/api/test')
            .then((response) => {
                testsRef.current = response.data;
            })
            .catch((error) => {
                console.log(error);
            });

        if(tests && testsRef.current){
            setNow(Math.round(Object.keys(tests).length * 100 / testsRef.current.length))
        }
    }, [name, tests]);

    return (
     <Card className={"device_card"} tabIndex="0">
        <Card.Body className="d-flex flex-column justify-content-between">
            <h4>{name}</h4>
            {state === "testing" ? <ProgressBar variant="info" now={now} label={`${now}%`} />
                : <Button variant="info" onClick={launchTests}>Run</Button>
            }
        </Card.Body>
     </Card>
    );
}

export default RunningDevice;