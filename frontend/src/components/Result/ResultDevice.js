import React, {useEffect, useState} from 'react';
import {Button, Card, Modal} from "react-bootstrap";
import "./Device.css"
import {io} from "socket.io-client";
import axios from "axios";
import Details from "../Details/Details";

function ResultDevice({name, result, ip}) {
    const [colorState, setColorState] = useState("device_card");
    const [showDetails, setShowDetails] = useState(false);
    const [deviceInfo, setDeviceInfo] = useState({});

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

          axios
            .get(`/api/device_info/${ip}`)
            .then((response) => {
                if(response.data && response.data.data){
                    setDeviceInfo(response.data.data);
                }
            })
            .catch((error) => {
                console.log(error);
            });

    }, [name, result, ip]);

    return (
        <>
           <Card className={"device_card " +  colorState}>
                <Card.Body className="d-flex flex-column justify-content-between">
                    <div>
                        <h4>{name}</h4>
                        <Button variant="secondary"className="w-100"  onClick={() => setShowDetails(true)}>Details</Button>
                    </div>
                    <Button variant="info" onClick={launchTests}>Run</Button>
                </Card.Body>
            </Card>


            <Modal
                size="lg"
                show={showDetails}
                onHide={() => setShowDetails(false)}
                aria-labelledby="details"
            >
            <Modal.Header closeButton>
              <Modal.Title id="details">
                  {name} details
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Details name={name} deviceInfo={deviceInfo} result={result} ip={ip} />
            </Modal.Body>
          </Modal>
        </>
    );
}

export default ResultDevice;