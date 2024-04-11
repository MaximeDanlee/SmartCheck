import React, {useEffect, useRef, useState} from 'react';
import {Button, Card, ProgressBar} from "react-bootstrap";
import "./Device.css"
import {io} from "socket.io-client";
import axios from "axios";

function Device({name, state, result, ip}) {
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


        const socket = io('/');
        socket.on('testing', (data) => {
            if(data && data.success && data.data[name]){
                setNow(Math.round(Object.keys(data.data[name]).length * 100 / testsRef.current.length));
            }
        });

        return () => {
            socket.disconnect();
        }
    }, [name]);



    return (
     <Card className={state === "done" ? "device_card bg-success-subtle" : "device_card device_card"}>
        <Card.Body>
            <h4>{name}</h4>
            {state === "testing" ? <ProgressBar variant="info" now={now} label={`${now}%`} />
                : <Button variant="info" onClick={launchTests}>Run</Button>
            }
        </Card.Body>
     </Card>
    );
}

export default Device;