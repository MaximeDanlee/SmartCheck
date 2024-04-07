import React from 'react';
import {Button, Card, Spinner} from "react-bootstrap";
import "./FastbootDevice.css"
import {io} from "socket.io-client";

function FastbootDevice({name, state, result}) {
    function flashDevice() {
        const socket = io('/');
        socket.emit('flash_pmos', name);
    }

  return (
     <Card className={state  === "done" && result.success ? "fastboot_card bg-success-subtle" : "fastboot_card fastboot_card"}>
        <Card.Body>
            <h4>{name}</h4>
            {state === "flashing" ?  <Spinner animation="grow" variant="info" />
                : <Button variant="info" onClick={flashDevice}>Run</Button>
            }

        </Card.Body>
     </Card>
  );
}

export default FastbootDevice;