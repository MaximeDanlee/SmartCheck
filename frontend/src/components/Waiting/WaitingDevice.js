import React, {useEffect, useRef, useState} from 'react';
import {Button, Card, ProgressBar} from "react-bootstrap";
import "./WaitingDevice.css"
import {io} from "socket.io-client";

function WaitingDevice({name, ip, test}) {

    function answerTest(answer) {
        const socket = io('/');
        socket.emit('waiting_test', name, ip, answer, test.test_name);
    }

    useEffect(() => {
       console.log(test)
    }, [test]);

    return (
      <Card className={"device_card"}>
        <Card.Body className="d-flex flex-column justify-content-between">
            <h4>{name}</h4>
            <h5>{test.message}</h5>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Button variant="success" onClick={() => answerTest(true)}>yes</Button>
                <Button variant="danger" onClick={() => answerTest(false)}>No</Button>
            </div>
        </Card.Body>
     </Card>
    );
}

export default WaitingDevice;