
import { useState } from 'react'
import './App.css'

function App() {

  const [userQuery, setUserQuery] = useState("")


  return (
    <>


<div className="container-fluid">
  <div className="row" style={{minHeight:'100vh'}}>
    <div className="col-2">
    Hello
    </div>
    <div className="col-10" style={{backgroundColor:"red"}}>

<div>
<select className="form-select" aria-label="Default select example">
  <option selected>Select the model</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>


<select className="form-select" aria-label="Default select example">
  <option selected>Select the word Embedding</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>



<select className="form-select" aria-label="Default select example">
  <option selected>Select the source</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>

</div>

<div>
    <input type="text" className="form-control" id="validationCustom01" value={userQuery} 
           onChange={(e)=> setUserQuery(e.target.value)}/>

      <button type="button" className="btn btn-info">Submit</button>
      </div>
    </div>
  </div>
</div>




    </>
  )
}

export default App
