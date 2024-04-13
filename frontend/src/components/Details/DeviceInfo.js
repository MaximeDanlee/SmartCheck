import React from 'react';
import {Table} from "react-bootstrap";
import "./DeviceInfo.css"

function DeviceInfo({deviceInfo}) {
    return (
        <div className="scrollable-div">
        <Table responsive bordered style={{textAlign: "left"}}>
            <tbody>
                {Object.keys(deviceInfo).map((key, index) => (
                    Object.keys(deviceInfo[key]).map((subKey, subIndex) => (
                        <tr key={subIndex}>
                            {subIndex === 0 && (
                                <td rowSpan={Object.keys(deviceInfo[key]).length}>{key}</td>
                            )}
                            <td>{subKey}</td>
                            <td>{deviceInfo[key][subKey]}</td>
                        </tr>
                    ))
                ))}
            </tbody>
        </Table>
        </div>
    )
}

export default DeviceInfo;