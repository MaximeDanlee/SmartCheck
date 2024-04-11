import React from 'react';
import {Button, Card, Spinner} from "react-bootstrap";
import "./Device.css"
import {io} from "socket.io-client";

function Device({name, state, result}) {

  return (
     <Card className={state  === "done" && result.success ? "device_card bg-success-subtle" : "device_card device_card"}>
        <Card.Body>
            <h4>{name}</h4>
            {state === "testing" ?  <Spinner animation="grow" variant="info" />
                : <Button variant="info">Run</Button>
            }
        </Card.Body>
     </Card>
  );
}

export default Device;