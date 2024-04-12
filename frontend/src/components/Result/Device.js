import React, {useEffect, useState} from 'react';
import {Button, Card} from "react-bootstrap";
import "./Device.css"
import {io} from "socket.io-client";
import axios from "axios";

function Device({name, state, result, ip}) {
    const [colorState, setColorState] = useState("device_card");

    function launchTests() {
        const socket = io('/');
        socket.emit('launch_all_test', name, ip);
    }

    useEffect(() => {
        axios.get('/api/test')
            .then((response) => {
                let numberOfTests= response.data.length;

                // set colorState
                let numberOfTestsSuccess = 0;
                for(const test in result){
                    if(result[test].success){
                        numberOfTestsSuccess++;
                    }
                }

                if(numberOfTestsSuccess === numberOfTests){
                    setColorState("bg-success-subtle");
                } else if(numberOfTestsSuccess >= numberOfTests / 2){
                    setColorState("bg-warning-subtle");
                } else {
                    setColorState("bg-danger-subtle");
                }
            })
            .catch((error) => {
                console.log(error);
            });

    }, [name, result]);

    return (
     <Card className={"device_card " +  colorState}>
        <Card.Body>
            <h4>{name}</h4>
            <Button variant="info" onClick={launchTests}>Run</Button>
        </Card.Body>
     </Card>
    );
}

export default Device;