import React from 'react';

import "./Home.css"
import Section from "../Section/Section";

function Home() {
    return (
         <div className="container">
            <div className="section">
                <h2>1. Ready</h2>
                <Section section={"ready"} />
            </div>
            <div className="divider"></div>
            <div className="section">
                <h2>2. Running</h2>
                <Section section={"testing"} />
            </div>
            <div className="divider"></div>
            <div className="section">
                <h2>3. Result</h2>
                <Section section={"result"} />
            </div>
        </div>
    )
}


export default Home;