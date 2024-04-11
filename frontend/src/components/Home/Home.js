import React from 'react';

import "./Home.css"
import Fastboot from "../Fastboot/Fastboot";
import Testing from "../Testing/Testing";

function Home() {
    return (
         <div className="container">
            <div className="section">
                <Fastboot />
            </div>
            <div className="divider"></div>
            <div className="section">
                <Testing />
            </div>
            <div className="divider"></div>
            <div className="section"></div>
        </div>
    )
}


export default Home;