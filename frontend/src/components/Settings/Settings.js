import React, {useEffect} from 'react';
import axios from "axios";

function Settings() {
    function getData(){
        console.log("Getting data")
        axios({
          method: "GET",
          url:"/api/",
        })
        .then((response) => {
            console.log(response.data)
        }).catch((error) => {
          if (error.response) {
            console.log(error.response)
            console.log(error.response.status)
            console.log(error.response.headers)
            }
        })
    }

    useEffect(() => {
        getData();
    }, []);

    return (
        <div>
            <h1>Settings</h1>
            <p>Settings page</p>
        </div>
    )
}

export default Settings;