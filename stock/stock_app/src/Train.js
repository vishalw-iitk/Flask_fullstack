import React from 'react'
import './App.css'

export default function Train(props) {
    const {
        t_res,
        result_class
    } = props
    const keys = [];
    for(var k in t_res) keys.push(k);
    
    return (
        <div className={result_class}>
            <table border="1">
                <tr>
                    <td>{keys[0]}</td>
                    <td>{t_res['Model']}</td>
                </tr>
                {/* <tr>
                    <td>{keys[1]}</td>
                    <td>{t_res.training_loss}</td>
                </tr>
                <tr>
                    <td>{keys[2]}</td>
                    <td>{t_res.validation_loss}</td>
                </tr> */}
            </table>
            {/* <img src={imgsrc} alt=""></img> */}
        </div>
    )
}
