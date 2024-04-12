import React from 'react';

import "./Home.css"
import Fastboot from "../Fastboot/Fastboot";
import Testing from "../Testing/Testing";
import Result from "../Result/Result";

function Home() {
    return (
         <div className="container">
            <div className="section">
                <h2>1. Flashing</h2>
                <Fastboot />
            </div>
            <div className="divider"></div>
            <div className="section">
                <h2>2. Testing</h2>
                <Testing />
            </div>
            <div className="divider"></div>
            <div className="section">
                <h2>3. Result</h2>
                <Result />
            </div>
        </div>
    )
}


export default Home;