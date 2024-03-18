import React from "react";
import {Card, Tab, Tabs} from "react-bootstrap";
import DeviceInfo from "./DeviceInfo";
import Testing from "./Testing";
import "./Device.css"

function Device({deviceInfo}) {
    return (
        <Card className="card center-horizontal">
            <Card.Body>
                <h4>{deviceInfo.device.name}</h4>
                 <Tabs defaultActiveKey="info" className="mb-3" justify>
                    <Tab eventKey="info" title="Info">
                        <DeviceInfo deviceInfo={deviceInfo} />
                    </Tab>
                    <Tab eventKey="testing" title="Testing">
                        <Testing />
                    </Tab>
                </Tabs>
            </Card.Body>
        </Card>
    )
}

export default Device;