import React, {useEffect} from 'react';
import {Button, Card} from "react-bootstrap";
import "./WaitingDevice.css"
import {io} from "socket.io-client";

function WaitingDevice({name, ip, test}) {

    function answerTest(answer) {
        const socket = io('/');
        socket.emit('waiting_test', name, ip, answer, test.test_name);
    }

    useEffect(() => {
       console.log(test)
        console.log("wtf")
    }, [test]);

    return (
      <Card className={"device_card"} tabIndex="0">
        <Card.Body className="d-flex flex-column justify-content-between">
            <h4>{name}</h4>
            <h5>{test.message}</h5>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Button variant="success" onClick={() => answerTest(true)} aria-label="Yes" tabIndex="0">yes</Button>
                <Button variant="danger" onClick={() => answerTest(false)} aria-label="No" tabIndex="0">No</Button>
            </div>
        </Card.Body>
     </Card>
    );
}

export default WaitingDevice;