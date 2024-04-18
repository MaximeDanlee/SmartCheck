import React, {useEffect, useState} from 'react';
import {Button, Card, ProgressBar} from "react-bootstrap";
import "./FastbootDevice.css"
import {io} from "socket.io-client";

function FastbootDevice({name, state, result}) {
    const [now, setNow] = useState(0);

    function flashDevice() {
        const socket = io('/');
        socket.emit('flash_pmos', name);
    }

    useEffect(() => {
        console.log(result)
        if(state === "done" && result.success){
            setNow(100);
        }
    }, [result, state]);

  return (
     <Card className={state  === "done" && result.success ? "fastboot_card bg-success-subtle" : "fastboot_card fastboot_card"}>
        <Card.Body className="d-flex flex-column justify-content-between">
            <h4>{name}</h4>
            {state === "flashing" ?  <ProgressBar variant="info" now={now} label={`${now}%`} />
                : <Button variant="info" onClick={flashDevice}>Run</Button>
            }
        </Card.Body>
     </Card>
  );
}

export default FastbootDevice;