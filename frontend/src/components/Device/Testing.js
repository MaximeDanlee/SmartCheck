import React, {useEffect, useState} from "react";
import {IconContext} from "react-icons";
import {FaPlayCircle} from "react-icons/fa";
import {Button, Spinner, Table} from "react-bootstrap";
import axios from "axios";
import "./Testing.css"
import {io} from "socket.io-client";



function Testing() {
    const [tests, setTests] = useState({})
    const [testIsLoading, setTestIsLoading] = useState({})

    function testAll() {
        Object.keys(tests).forEach((test) => {
            launchTest(test)
        })
    }

    function launchTest(testName) {
        setTestIsLoading(testIsLoading => ({
            ...testIsLoading,
            [testName]: true
        }))

        const socket = io('/');
        socket.emit('launch_test', testName);
    }

    function getTests() {
        axios.get('/api/test')
            .then((response) => {
                response.data.forEach((test) => {
                    setTests(tests => ({
                        ...tests,
                        [test]: {}
                    }))

                    setTestIsLoading(testIsLoading => ({
                        ...testIsLoading,
                        [test]: false
                    }))
                })

            })
            .catch((error) => {
                console.error('Error API request failed:', error);
            });
    }

    useEffect(() => {
        // Get tests names
        getTests()

        const socket = io('/');

        // Listen for the 'test_result' event, which will be emitted by the server
        socket.on('test_result', (data) => {
            console.log(data);
            setTests(tests => ({
                ...tests,
                [data.test_name]: {
                    success: data.success,
                    message: data.message,
                    data: data.data ? data.data : {}
                }
            }));

            setTestIsLoading(testIsLoading => ({
                ...testIsLoading,
                [data.test_name]: false
            }))
        });

        return () => {
            // Disconnect the socket when the component is unmounted
            socket.disconnect();
        };
    }, []);

    return (
        <IconContext.Provider value={{ color: "green", className: "global-class-name" }}>
            <div className="fs-5 row row-cols-1">
                <Button variant="success" className="margin-12px width-150px" onClick={testAll}>Run All Test</Button>{' '}<br />
                <Table responsive bordered style={{textAlign: "left"}}>
                    <tbody>
                        {Object.keys(tests).map((test, index) => (
                            <tr key={index}>
                                <td className="w-50">
                                    {test}
                                    {testIsLoading[test] ? <Spinner animation="border" variant="success" className="float-end m-2 size-20" />
                                    :<FaPlayCircle onClick={() => launchTest(test)} className="float-end m-2" style={{ cursor: 'pointer' }} />}
                                </td>
                                <td className={tests[test].success !== undefined ? (tests[test].success ? "bg-success-subtle fs-6" : "bg-danger-subtle fs-6") : "fs-6"}>
                                    <b>{tests[test].message}</b>
                                    {tests[test].data && Object.keys(tests[test].data).map((key, index) => (
                                        <div key={index}>
                                            <span>{key}: {tests[test].data[key].toString()}</span>
                                        </div>
                                    ))}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </div>
        </IconContext.Provider>
    )
}

export default Testing;