import './App.css';
import axios from 'axios'
import React, {useState, useEffect, useRef} from 'react';
import Dataset from './Dataset'
import Train from './Train'
import imgsrc from './output.png'

function App() {
  const [data, setdata] = useState([])
  const [classer, setclass] = useState("")
  const [header, setheader] = useState(<></>)
  const [bt, setbt] = useState(<></>)
  const [msg, setmsg] = useState(<></>)
  const [t_res, set_tres] = useState([])
  const [result_class, set_res_class] = useState("")
  const [imgtg, set_imgsrc] = useState(<></>)
  function Getdata(e){
    e.preventDefault()
    console.log("ggg")
    axios
      .get('http://127.0.0.1:5000/users')
      .then(res => {
        console.log(res)
        setheader(<tr>
          <th>Index</th>
          <th>Date</th>
          <th>Open</th>
          <th>High</th>
          <th>Low</th>
          <th>Close</th>
          <th>Adj Close</th>
          <th>Volume</th>
          </tr>)
        setdata(res.data.data)
        setbt(<button>Forecast</button>)
        setclass("tabledata")
        
        return res
      })
  }

  function TrainData(e){
    e.preventDefault()
    console.log("mmmmmmmmmmm")
    setmsg(<span className="waitmsg">Results in 1:30 mins</span>)
    axios
      .get('http://127.0.0.1:5000/process')
      .then(res => {
        console.log(res)
        set_tres(res.data)
        set_imgsrc(<img src={imgsrc} alt="Forecast image" width="400" height="400"/>)
        set_res_class("trainblock")
        
      })
  }

  return (
  <>
  <div className="container">
  <div className="intro"><div className="myname">Vishal Waghmare</div><br></br><div className="stocktitle"><b>Opening</b> price forecasting platform</div></div>
  <form className="getdata" onSubmit={Getdata}>
    <button>Get the dataset</button>
  </form>
  <div className="dataset-container">
  <Dataset 
  data={data}
  header={header}
  classer={classer} 
  />
  </div>
  <form className="train" onSubmit={TrainData}>
    {bt}
    {msg}
  </form>
  <div className="trainresult">
  <Train 
  t_res={t_res}
  result_class={result_class}
  ></Train>
  </div>
  {imgtg}
  </div>
  </>
  )
}

export default App;
