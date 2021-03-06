import React, {useState, useEffect} from 'react'
import './App.css'

export default function Dataset(props) {
    const {
        data,
        header,
        classer
    } = props

    // const [flip, setFlip] = useState(false)
    
    // useEffect(setFlip(!flip),[])
    // if(data !== undefined){
        // setFlip(!flip)
        // const flip = true
    // }
    return (
        <div>
                <table border="1" className={classer}
                >
                    {header}
                    {data.map(user => {
                        return <tr>{
                            user.map(element => {
                                return <td>{typeof element === 'number'?Math.round(element*1000)/1000:element}</td>
                            })
                            }</tr>
                    })}
                </table>
        </div>
    )
}
