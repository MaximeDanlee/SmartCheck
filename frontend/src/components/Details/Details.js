import React from "react";
import {Tab, Tabs} from "react-bootstrap";
import DeviceInfo from "./DeviceInfo";
import Testing from "./Testing";
import "./Details.css"
import Result from "./Result";

function Details({name, deviceInfo, result, ip}) {
    return (
         <Tabs defaultActiveKey="result" className="mb-3" justify>
             <Tab eventKey="result" title={<span className="tab-title">Result</span>}>
                <Result result={result} />
            </Tab>
            <Tab eventKey="info" title={<span className="tab-title">Info</span>}>
                <DeviceInfo deviceInfo={deviceInfo} />
            </Tab>
            <Tab eventKey="testing" title={<span className="tab-title">Testing</span>}>
                <Testing name={name} ip={ip} />
            </Tab>
        </Tabs>
    )
}

export default Details;