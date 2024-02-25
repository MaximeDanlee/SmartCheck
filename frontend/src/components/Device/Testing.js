import React, {useState} from "react";
import {IconContext} from "react-icons";
import {FiCpu} from "react-icons/fi";
import {FaPlayCircle, FaUsb} from "react-icons/fa";
import {GrSatellite} from "react-icons/gr";
import {Button, Spinner, Table} from "react-bootstrap";
import axios from "axios";
import "./Testing.css"



function Testing() {
    const [cpuIsLoading, setCpuIsLoading] = useState(false)
    const [usbIsLoading, setUsbIsLoading] = useState(false)
    const [modemIsLoading, setModemIsLoading] = useState(false)

    const [cpu, setCpu] = useState({})
    const [usb, setUsb] = useState({})
    const [modem, setModem] = useState({})

    function testAll() {
        testProcessor()
        testUSB()
        testModem()
    }

    function testProcessor() {
        setCpuIsLoading(true)
        axios.get('/api/test/cpu')
            .then((response) => {
                console.log(response.data)
                setCpu(response.data)
                setCpuIsLoading(false)
            })
            .catch((error) => {
                const data = {
                    "success": false,
                    "message": "Error API request failed : " + error
                }
                setCpu(data)
                setCpuIsLoading(false)
            });
    }

    function testUSB() {
        setUsbIsLoading(true)
        axios.get('/api/test/usb_port')
            .then((response) => {
                console.log(response.data)
                setUsb(response.data)
                setUsbIsLoading(false)
            })
            .catch((error) => {
                const data = {
                    "success": false,
                    "message": "Error API request failed : " + error
                }
                setUsb(data)
                setUsbIsLoading(false)
            });

    }

    function testModem() {
        setModemIsLoading(true)
        axios.get('/api/test/4g')
            .then((response) => {
                console.log(response.data);
                setModem(response.data)
                setModemIsLoading(false)
            })
            .catch((error) => {
                const data = {
                    "success": false,
                    "message": "Error API request failed : " + error
                }
                setModem(data)
                setModemIsLoading(false)
            });
    }

    useState(() => {
        console.log(modem)
        console.log(modem.success)
    })

    return (
        <IconContext.Provider value={{ color: "green", className: "global-class-name" }}>
            <div className="fs-5 row row-cols-1">
                <Button variant="success" className="margin-12px width-150px" onClick={testAll}>Run All Test</Button>{' '}<br />
                <Table responsive bordered style={{textAlign: "left"}}>
                    <tbody>
                        <tr>
                            <td className="w-50">
                                <FiCpu /> Processor
                                {cpuIsLoading ? <Spinner animation="border" variant="success" className="float-end m-2 size-20" />
                                :<FaPlayCircle onClick={testProcessor} className="float-end m-2" style={{ cursor: 'pointer' }} />}
                            </td>
                            <td className={cpu.success !== undefined ? (cpu.success ? "bg-success-subtle fs-6" : "bg-danger-subtle fs-6") : "fs-6"}>
                                {cpu.message}
                            </td>
                        </tr>
                        <tr>
                            <td className="width-50">
                                <FaUsb/> USB Ports
                                {usbIsLoading ? <Spinner animation="border" variant="success" className="float-end m-2 size-20" />
                                :<FaPlayCircle onClick={testUSB}  className="float-end m-2" style={{ cursor: 'pointer' }} />}
                            </td>
                            <td className={usb.success !== undefined ? (usb.success ? "bg-success-subtle  fs-6" : "bg-danger-subtle  fs-6") : "fs-6"}>
                                {usb.message}
                            </td>
                        </tr>
                        <tr>
                            <td className="width-50">
                                <GrSatellite /> Modem
                                {modemIsLoading ? <Spinner animation="border" variant="success" className="float-end m-2 size-20"  />
                                :<FaPlayCircle onClick={testModem} className="float-end m-2" style={{ cursor: 'pointer' }} />}
                            </td>
                            <td className={modem.success !== undefined ? (modem.success ? "bg-success-subtle fs-6" : "bg-danger-subtle fs-6") : "fs-6"}>
                                {modem.message}
                            </td>
                        </tr>
                    </tbody>
                </Table>
            </div>
        </IconContext.Provider>
    )
}

export default Testing;