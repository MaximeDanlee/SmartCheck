import React from 'react';

import "./Home.css"
import Section from "../Section/Section";

function Home() {
    return (
         <div className="container">
            <div className="section" aria-label='Section 1 : Ready'>
                <h2 aria-label='Section 1 : Ready' tabIndex="0">1. Ready</h2>
                <Section section={"ready"} />
            </div>
            <div className="divider"></div>
            <div className="section" aria-label='Section 2 : Running'>
                <h2 aria-label='Section 2 : Running' tabIndex="0">2. Running</h2>
                <Section section={"testing"} />
            </div>
            <div className="divider"></div>
            <div className="section" aria-label='Section 3 : Result'>
                <h2 aria-label='Section 3 : Result' tabIndex="0">3. Result</h2>
                <Section section={"result"} />
            </div>
        </div>
    )
}


export default Home;