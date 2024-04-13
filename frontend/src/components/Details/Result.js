import {Table} from "react-bootstrap";
import React from "react";


function Result({result}) {
    return (
        <div className="fs-5 row row-cols-1">
            <Table responsive bordered style={{textAlign: "left"}}>
                <tbody>
                    {Object.keys(result).map((name, index) => (
                        <tr key={index}>
                            <td className="w-50">
                                {name}
                            </td>
                            <td className={result[name].success !== undefined ? (result[name].success ? "bg-success-subtle fs-6" : "bg-danger-subtle fs-6") : "fs-6"}>
                                <b>{result[name].message}</b>
                                {result[name].data && Object.keys(result[name].data).map((key, index) => (
                                    <div key={index}>
                                        <span>{key}: {result[name].data[key].toString()}</span>
                                    </div>
                                ))}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
}

export default Result;